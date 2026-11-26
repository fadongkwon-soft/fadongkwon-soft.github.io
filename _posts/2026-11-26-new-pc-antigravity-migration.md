---
title: "1인 개발사 통째로 이사하기: 새 PC + Antigravity 이관 핸드오프 기록"
description: "저장소 7곳, 120여 개 앱 설정과 서명 키, 예약 자동화 3종, 운영 수칙까지 새 PC의 Antigravity 환경으로 통째로 이관하면서 만든 핸드오프 문서와 점검 체크리스트를 공유합니다."
date: 2026-11-26 01:24:00 +0900
categories: [Devlog, Retrospective]
tags: [개발환경, 안티그래비티, 마이그레이션, 안드로이드, 워크플로우, 1인개발자, 개발일지]
pin: false
image:
  path: /assets/img/20261126_new-pc-antigravity-migration/cover.png
alt_url: /posts/new-pc-antigravity-migration/
---

1인 개발사로 앱을 100개 넘게 굴리다 보면 PC를 한 번 바꿀 때마다 식은땀이 납니다. 코드 저장소만 `git clone`해서 끝나는 게 아니라, 서명 키스토어, `.gitignore`된 120여 개 광고 설정 파일, 서비스 계정 JSON, ADB 키, 예약 자동화, 그리고 그동안 쌓아 둔 운영 수칙까지 빠짐없이 옮겨야 하기 때문입니다.

11월 20일 기존 PC에서 Claude Code와 병행하던 개발·출시·자동화 환경을 새 PC의 **Antigravity**로 통째로 이관하면서, 아예 `antigravity-handoff-new-pc-2026-11-20.md`라는 이관 지시서를 만들어 진행했습니다. 막상 옮겨 보니 어디서 발목이 잡히는지 정리해 둡니다.

## 1. 복원 직후 가장 먼저 돌린 '읽기 전용 점검 표'

새 PC에 백업을 풀고 바로 빌드를 돌리지 않고, 에이전트에게 **읽기 전용 점검 프롬프트**부터 던져 누락된 것을 표로 뽑게 했습니다.

1. **주요 저장소 7곳 존재 여부**: `.claude`, `apps-in-toss`, `apps-in-toss-games`, `quiz-apps`, `revenue-ledger`, `tarot-content`, `Github\fadongkwon-soft.github.io` (+ `saju_lotto_android`).
2. **비밀값·서명 키 유무 (값 출력 금지)**: 키스토어(`.jks`), `keystore.properties`, `admob-*.properties`(121개), `play_service_account.json`, `token.json`, `toss_mcp_token.json`, `.env`, 그리고 각 저장소 `.git/hooks` 비밀값 검사 훅 설치 여부.
3. **도구·의존성 동작 확인**: `git`, `node 24 + pnpm`, `python 3.14`, `ffmpeg`, `adb`, `checklist_state.py`, `play.py`, Gradle 동기화.
4. **자동화·MCP 연결**: `~/.gemini/config/sidecars/` 예약 작업 3종과 `apps-in-toss-console` MCP.

비밀 파일은 **내용이나 값을 절대 출력하지 말고 파일 존재 여부만 확인**하도록 프롬프트에 못 박아 두었습니다.

## 2. 새 PC에서 가장 자주 터지는 빌드 함정 3가지

- **Gradle 8.11.1 + JBR 25 충돌**: Android Studio 최신판에 딸려 오는 JBR 25로 Gradle 8.11.1을 돌리면 바로 실패합니다. `JAVA_HOME`을 JDK 18 경로로 고정해야 빌드가 통과합니다.
- **Android SDK 경로 불일치**: 이전 PC의 스토어판 샌드박스 경로(`LocalCache\Local\Android\Sdk`)가 `local.properties`에 남아 있으면 새 PC에서 빌드가 깨집니다. 정식 실경로(`D:\Android\sdk` 등)로 맞추고 `ANDROID_AVD_HOME`도 함께 잡았습니다.
- **Windows PowerShell 5.1 UTF-8 인코딩**: `Set-Content` 기본 BOM이나 CP949 때문에 토스 래퍼 빌드나 Jekyll 페이지 front matter가 깨지는 사고를 이미 겪었기 때문에, 파이썬 실행은 항상 `-X utf8`을 붙이고 래퍼 빌드 규칙을 핸드오프에 명시했습니다.

## 3. 에이전트가 반드시 승계해야 할 운영 수칙 명문화

환경이 바뀌면 에이전트도 과거의 시행착오를 잊습니다. 그래서 기존 메모리에 흩어져 있던 핵심 수칙을 핸드오프 문서 2장에 압축해 승계했습니다.

- **언어·문구**: 보고·커밋·문서는 한국어, JSON/코드에 `\uXXXX` 이스케이프 금지, 새 블로그 글에 구체적 수익 금액 비공개.
- **Git·보안**: `git add -A` / `git add .` 금지(파일 명시 + `git diff --cached --stat` 확인), 커밋 지시 시 푸시까지 완료, `--no-verify` 금지.
- **빌드·출시**: 토스 래퍼 빌드가 `dist-hub`를 덮어쓰므로 Play 허브 AAB 빌드 전 반드시 `hub-build` 재실행, Play 개인정보처리방침은 `https://fadongkwon.com/...` 정본만 사용.
- **실행 경계**: 에이전트는 빌드·검증·제출까지, 사용자는 실기기 확인·토스 콘솔 웹 '출시하기'·외부 서비스 가입/결제 담당.

## 4. 이관 뒤 작업 우선순위를 P0~P3로 고정

이관이 끝나자마자 무엇부터 손댈지 헤매지 않도록 지시서에 우선순위를 미리 적어 두었습니다.

- **P0**: 미커밋 정리 → 마감 임박 정책 조치 → 114개 재출시 승인 확인 → 토스 콘솔 대기 건 조회
- **P1**: Unity LevelPlay + Unity Ads 시범 연동 및 확대 전환
- **P2**: Play 미출시 잔여 7개 앱 생성·제출
- **P3**: `fadongkwon.com` 웹 게임 제공 및 트래픽 로드맵

덕분에 새 PC로 이사한 다음 날부터 곧바로 LevelPlay 시범 연동과 신작 7종 제출까지 끊김 없이 이어갈 수 있었습니다. PC를 옮길 때 파일 백업만큼 중요한 건 **"지금 어디까지 했고, 무엇을 절대 하면 안 되는지"를 한 장의 핸드오프 문서로 묶어 두는 것**이었습니다.
