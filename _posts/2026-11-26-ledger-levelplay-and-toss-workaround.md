---
title: "수익 장부에 LevelPlay API 붙이고, 토스 IAA 전체 리포트 타임아웃 우회하기"
description: "Unity LevelPlay v6 리포트 API를 revenue-ledger에 연동해 USD→KRW 일일 환율 캐시와 앱 이름 정규화를 구현하고, 앱 수가 늘며 타임아웃이 나던 토스 IAA 수집을 앱별 조회로 전환한 기록입니다."
date: 2026-11-26 01:28:00 +0900
categories: [Devlog, Retrospective]
tags: [자동화, API, 파이썬, 앱인토스, 레벨플레이, 1인개발자, 개발일지]
pin: false
image:
  path: /assets/img/20261126_ledger-levelplay-and-toss-workaround/cover.png
alt_url: /posts/ledger-levelplay-and-toss-workaround/
---

11월 18일 [헤드리스 AI 없이 파이썬이 토스 MCP에 직접 붙도록 장부를 바꾼](/ko/posts/ledger-without-headless-ai/) 지 며칠 만에, 수익 장부(`revenue-ledger`)에 두 가지 큰 손질이 더 필요해졌습니다.

하나는 **새 광고 네트워크인 Unity LevelPlay 리포트 API를 장부에 붙이는 일**, 다른 하나는 **토스 앱 수가 늘어나면서 워크스페이스 전체 리포트가 매번 타임아웃으로 실패하는 문제**를 정리하는 일이었습니다. *(기존 원칙대로 구체적인 수익 금액은 적지 않고 구조와 구현만 다룹니다.)*

## 1. `levelplay_fetch.py`: LevelPlay v6 리포트를 원화 장부에 합치기

Unity LevelPlay(ironSource) 리포팅 API는 OAuth 방식의 토스·구글과 인증 흐름이 다릅니다.

1. **Bearer 토큰 발급**: 대시보드(`Account → API`)에서 발급받은 `Secret Key`와 `Refresh Token`을 로컬 `levelplay_api.json`(.gitignore)에 두고, `https://platform.ironsrc.com/partners/publisher/auth`로 요청해 토큰을 받습니다.
2. **일자 × 앱 리포트 조회**: `.../mediation/applications/v6/stats`에서 기본 최근 14일~어제까지 데이터를 가져옵니다. 토스 장부와 마감일 기준을 맞추기 위해 어제까지만 `ledger.csv`에 적재하고, UTC 진행 중인 오늘 수치는 콘솔 참고용으로만 출력합니다(`--today` 옵션으로 선택 가능).
3. **USD → KRW 일일 환율 캐시**: LevelPlay 금액은 달러(USD)로 내려오는데, 대시보드는 전 플랫폼을 원화(KRW)로 합산합니다. `open.er-api.com/v6/latest/USD`에서 당일 환율을 받아 `fx_usd_krw.json`에 하루 한 번만 캐시하고, 네트워크가 실패하면 직전 캐시 → 기본값(`1400.0`) 순으로 폴백합니다.
4. **앱 이름 정규화**: `android/levelplay-<id>.properties`의 `appKey`와 Play 패키지(`bundleId`)를 `apps.json`·`registry/apps.csv` 표시명과 매핑해, 토스와 Play 실적이 같은 앱 이름으로 깔끔하게 합쳐지도록 만들었습니다.

## 2. 토스 IAA 전체 리포트 실패 → 앱별 조회(`fetch_per_app`) 기본화

토스 미니앱 수가 늘어나면서 `iaa_workspace_dashboard_report_v2`(워크스페이스 전체 리포트)를 호출할 때마다 60초를 넘겨 타임아웃이 나거나 오류가 떨어졌습니다. 예전 `toss_fetch.py`는 전체 리포트를 먼저 시도해 1~2분을 버린 뒤에야 `fetch_per_app`으로 폴백하는 구조였습니다.

11월 21일(`b61159e`) 이 우회를 아예 **기본 동작**으로 바꿨습니다.

- `toss_fetch.py`가 처음부터 앱별 `iaa_dashboard_report_v2`를 호출하도록 단순화했습니다.
- 앱별로 여러 요청을 보내다 보면 토스 쪽 rate limit에 걸릴 수 있어, `toss_mcp.py`의 동시 요청 수(`TOSS_MCP_PARALLEL`) 기본값을 **4 → 2**로 낮췄습니다.
- JSON-RPC 오류 메시지에 `'요청이 너무 많습니다'`, `'Too Many Requests'`, `'rate limit'`, `'잠시 후 다시'` 같은 문구가 들어 있으면 치명적 오류(`RpcError`) 대신 일시 오류(`TransientError`)로 분류하고, 재시도 횟수를 **3회 → 4회**, 대기 백오프를 `(2, 5, 10)`초로 늘렸습니다.

## 3. `update.cmd` 한 번으로 전 플랫폼 대시보드 갱신

이제 로컬에서 `update.cmd`를 실행하면:

1. 토스 IAA 앱별 수집 (`toss_fetch.py`)
2. Unity LevelPlay 일자×앱 수집 (`levelplay_fetch.py`)
3. 프로모션·후기 장부 갱신 및 대시보드 HTML 재생성 (`dashboard.py`)

이 한 번에 끝납니다. 광고 네트워크가 바뀌어도 장부 파이프라인을 깨뜨리지 않고 어댑터 하나만 갈아끼우면 이어서 돌아가게 만든 덕분에, 전환 직후부터 데이터 공백 없이 모니터링을 이어갈 수 있었습니다.
