---
title: "매일 밤 혼자 일하는 에이전트 3개: 토스 후기·구글 색인·Threads 자동화"
description: "1인 개발자가 매일 반복하던 토스 후기 수집, fadongkwon.com 구글 색인 생성 요청, Threads 앱 홍보를 Antigravity 예약 자동화(sidecar) 3종으로 무인화한 구조와 최소 권한 격리 방식을 정리했습니다."
date: 2026-11-26 01:20:00 +0900
categories: [Devlog, Retrospective]
tags: [자동화, AI에이전트, 안티그래비티, 스레드, 서치콘솔, 1인개발자, 개발일지]
pin: false
image:
  path: /assets/img/20261126_midnight-automation-agents/cover.png
alt_url: /posts/midnight-automation-agents/
---

앱이 100개를 넘어가면 개발보다 운영이 먼저 사람을 지치게 합니다. 매일 토스 콘솔에 들어가 새 별점과 후기가 달렸는지 훑고, Search Console에서 색인 안 된 블로그 URL을 일일 한도만큼 눌러 넣고, 아직 홍보하지 않은 앱을 골라 SNS에 올리는 일은 하나하나가 10~20분씩 잡아먹습니다.

그래서 11월 중순부터 이 세 가지 루틴을 **Antigravity 예약 자동화(sidecar)**로 묶어 매일 혼자 돌아가게 만들었습니다. 설치 스크립트(`install_automations.py`)와 프롬프트 3개로 관리하는 구조를 기록해 둡니다.

## 1. 매일 돌아가는 예약 에이전트 3종

세 작업은 모두 `Asia/Seoul` 시간대 cron으로 `~/.gemini/config/sidecars/<id>/sidecar.json`에 등록해 두었습니다.

| ID | 실행 시각 | 역할 | 주요 도구 |
|---|---|---|---|
| `daily-threads-posts` | 매일 00:00 | 수익 상위 앱 중 Threads 미게시 앱을 골라 준비된 동영상·이미지로 `@fadongkwon.soft` 자동 게시 | `threads_picker.py`, `threads_post.py` |
| `daily-toss-reviews` | 매일 00:03 | 앱인토스 콘솔 전 앱 별점·후기 수집 → `revenue-ledger` 후기 장부 및 대시보드 갱신 | `chrome-devtools` MCP, `toss_reviews.py`, `dashboard.py` |
| `gsc-daily-index-requests` | 매일 18:11 | `fadongkwon.com` 미색인 대기열을 Search Console '색인 생성 요청'으로 일일 한도까지 제출 | `chrome-devtools` MCP, `gsc_rec.py`, `tools/gsc.py` |

중요한 전제는 **예약 실행 대화에는 이전 기억이 전혀 없다**는 점입니다. 그래서 `prompts/<id>.md` 파일 안에 실행 순서, 실패 시 중단 조건, 결과 저장 경로까지 처음부터 끝까지 자급자족할 수 있게 적어 두었습니다.

## 2. 왜 단순 크론 스크립트가 아니라 에이전트인가

파이썬 스크립트만으로 끝낼 수 있는 일은 당연히 파이썬으로 짭니다. 실제로 후기 파싱(`toss_reviews.py`), Threads 후보 선정(`threads_picker.py`), 색인 상태 기록(`gsc_rec.py`)은 모두 일반 스크립트입니다.

에이전트가 끼어드는 지점은 **API가 없거나 UI가 자주 바뀌는 웹 콘솔 구간**입니다.

- 토스 콘솔 후기 페이지와 Google Search Console의 '색인 생성 요청' 버튼은 공식 API가 없거나 로그인 세션이 필요합니다.
- 에이전트가 `chrome-devtools` MCP로 전용 크롬 프로필에 붙어 스냅샷을 읽고, 버튼 위치나 팝업 문구가 조금 바뀌어도 맥락을 보고 처리한 뒤 결과를 로컬 스크립트에 넘깁니다.
- 반대로 Threads 게시는 후보 선정과 본문 초안 작성은 에이전트가 맡고, 실제 업로드는 `threads_post.py`로 실행해 안정성을 높였습니다.

## 3. 최소 권한 원칙: `sidecar.json`의 `access_grants`

무인 자동화에서 가장 신경 쓴 부분은 **권한 격리**입니다. 에이전트가 자는 동안 엉뚱한 저장소를 건드리거나 원치 않는 명령을 실행하지 않도록 `install_automations.py`에서 작업마다 `workspace_uris`와 `access_grants`를 화이트리스트로 고정했습니다.

- **`daily-toss-reviews`**: `revenue-ledger` 읽기·쓰기, `apps-in-toss.toss.im` 접속, 지정된 파이썬 3개(`toss_reviews.py`, `reviews_report.py`, `dashboard.py`)만 허용.
- **`gsc-daily-index-requests`**: `fadongkwon-soft.github.io` 읽기, `tools/out`만 쓰기, `search.google.com`·`fadongkwon.com` 접속만 허용.
- **`daily-threads-posts`**: `antigravity-automations` 쓰기와 `threads_picker.py`·`threads_post.py` 실행만 허용.

설치 스크립트도 기본 실행은 드라이런(미리 보기)이고, `--write` 옵션을 줘야 `sidecar.json`을 생성합니다. 생성 후에도 자동으로 켜지지 않고 Antigravity Automations 대시보드에서 사람이 직접 스위치를 켜야 돕니다.

## 4. 실제로 돌려 본 효과

가장 체감이 큰 건 **후기 수집과 실제 패치의 연결**입니다. 자정 3분에 자동으로 긁어 온 토스 별점·후기가 아침 대시보드에 바로 올라오니, 별점 4점짜리 짧은 피드백도 놓치지 않고 [오목 AI 난이도 개편](/ko/posts/gomoku-beginner-ai-from-review/) 같은 업데이트로 바로 이어질 수 있었습니다.

1인 개발자에게 자동화의 목적은 거창한 자율 시스템이 아니라, **매일 30분씩 새어 나가는 반복 업무를 잠자는 시간으로 치워 두고 낮에는 제품 개선에 집중하는 것**입니다.
