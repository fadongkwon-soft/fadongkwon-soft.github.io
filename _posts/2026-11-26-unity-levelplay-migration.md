---
title: "AdMob 종료 일주일 뒤: Unity LevelPlay + Unity Ads로 갈아탄 실전 이관기"
description: "구글 게시자 계정 이의신청이 기각된 지 일주일 만에 Android 래퍼를 Unity LevelPlay 미디에이션 + Unity Ads로 전환했습니다. 시범 2종(벽돌깨기·고누)에서 미출시 신작 7종, 기존 앱 20종 순차 전환까지 SDK 분리·R8 검증·app-ads.txt·데이터 보안 CSV 정비 기록을 정리했습니다."
date: 2026-11-26 01:05:00 +0900
categories: [Devlog, Retrospective]
tags: [유니티애즈, 레벨플레이, 광고전환, 안드로이드, 미디에이션, 1인개발자, 개발일지]
pin: false
image:
  path: /assets/img/20261126_unity-levelplay-migration/cover.png
alt_url: /posts/unity-levelplay-migration/
---

11월 19일 [구글 게시자 계정 이의신청이 기각](/ko/posts/google-ads-appeal-rejected/)된 뒤, Google Play에 올라가 있는 100여 개 앱의 광고 수익화가 한꺼번에 멈췄습니다. 선택지는 단순했습니다. 구글 광고와는 완전히 선을 긋고, 새 광고 네트워크로 갈아타는 것입니다.

지난 일주일 동안 **Unity LevelPlay(구 ironSource) 미디에이션 + Unity Ads**를 선택해 시범 2종(`벽돌깨기`, `고누`)부터 시작했고, 미출시 신작 7종 선제 심사 제출과 기존 라이브 앱 20종(1·2차) 순차 전환까지 밀어붙였습니다. 한꺼번에 100개 앱을 바꾸다 사고를 내지 않기 위해 세운 구조와 체크리스트를 기록해 둡니다.

## 1. 설정 파일 하나로 네트워크를 갈아끼우는 구조

모노레포(`apps-in-toss-games/android/app`)에는 120개가 넘는 product flavor가 들어 있습니다. 이걸 일일이 분기 코드로 나누면 유지보수가 불가능해집니다. 그래서 **설정 파일 존재 자체를 스위치**로 삼았습니다.

- `android/levelplay-<id>.properties` 파일이 있으면 해당 flavor를 자동으로 `adsLevelPlay` 소스셋으로 배정합니다.
- 이 파일은 `.gitignore`에 넣어 키가 저장소에 올라가지 않게 막습니다.
- `AdManager.kt`와 `ConsentManager.kt`의 **공개 계약(메서드 시그니처)**을 기존 `adsReal`과 똑같이 맞췄습니다. 덕분에 `MainActivity.kt`, `MiniBridge.kt`, 그리고 100여 개 웹 게임 소스는 광고 네트워크가 바뀌었다는 사실조차 모른 채 그대로 동작합니다.

토스(앱인토스) 쪽은 토스 자체 IAA를 쓰기 때문에 한 줄도 건드리지 않았습니다.

## 2. Google Mobile Ads·UMP 완전 제거와 R8 검증

AdMob 계정이 종료된 상태에서 Google Mobile Ads SDK나 `com.google.android.gms.ads.APPLICATION_ID` 메타데이터가 매니페스트에 남아 있으면 혼선과 불필요한 용량만 늘어납니다.

- 기존 UMP 기반 `ConsentManager.kt`는 `src/adsUmp/`로 분리해 기존 flavor에만 남겼습니다.
- `adsLevelPlay` 전용 `AndroidManifest.xml`을 두고, `APPLICATION_ID` 없이 targetSdk 33+ 필수 권한인 `com.google.android.gms.permission.AD_ID`만 선언했습니다.
- 의존성은 `mediation-sdk:9.8.0`과 `unityads-adapter:5.17.0`(Unity Ads SDK 4.22.0 포함)으로 묶었습니다.

말로만 "분리했다"고 끝내지 않고, 릴리즈 빌드 후 **R8 `mapping.txt`**에서 클래스 개수를 직접 셌습니다.

| 빌드 대상 | Google Mobile Ads (identifier 제외) | UMP | LevelPlay | Unity Ads | Manifest `APPLICATION_ID` |
|---|---:|---:|---:|---:|---|
| `breakoutRelease` (시범) | 0 | 0 | 27 | 870 | 없음 |
| `gonuRelease` (시범) | 0 | 0 | 27 | 873 | 없음 |
| `reactionRelease` (기존 대조) | 376 | 6 | 0 | 0 | 있음 |
| `mathMonstersRelease` (아동 `adsStub`) | 0 | 0 | 0 | 0 | 없음 |

아동 대상 앱(`adsStub`)은 여전히 모든 광고 SDK가 0개입니다.

## 3. 새 계정을 지키기 위해 추가한 7가지 안전장치

광고 네트워크를 바꿨다고 무효 트래픽 위험이 사라지지는 않습니다. 오히려 새 계정은 초기 신뢰도가 낮아 더 조심해야 합니다. 시범 연동 단계에서 래퍼에 아래 7가지를 기본 탑재했습니다.

1. **비신뢰 환경 차단 (`AdSafety`)**: 디버거블·에뮬레이터·루팅·`com.android.vending` 외 출처 설치에서는 `LevelPlay.init()` 자체를 호출하지 않고 광고 요청을 0건으로 막습니다.
2. **광고 예열 시간 (`AdWarmupStore`)**: 설치 후 첫 실행에서 누적 포그라운드 3분(`180,000ms`)을 채우고 2회차 실행 또는 1판 완료 조건을 넘기기 전까지는 초기화를 보류하고 배너 자리도 접어 둡니다.
3. **비동기 보상형 판정 게이트 (`RewardedOutcomeGate`)**: `onAdRewarded`와 `onAdClosed`가 역순으로 도착해도 `onAdClosed` 뒤 600ms 유예 구간을 두고 `"earned"` 또는 `"dismissed"`를 정확히 한 번만 확정합니다.
4. **배너 자동 새로고침 제어 + 지수 백오프**: 하루 20회 상한 차단, 게임 중 숨김, 백그라운드 전환 시 `pauseAutoRefresh()`를 부르고, 로드 실패 시 최대 64초 지수 백오프를 적용합니다.
5. **동의·규정 플래그**: `LevelPlay.init()` 직전에 GDPR·CCPA·COPPA 플래그를 명시적으로 설정합니다.
6. **로컬 자체 집계 (`AdLocalStats`)**: 형식별(배너·전면·보상형) 로드·표시·클릭을 날짜 단위로 30일간 로컬에 쌓아 디버깅과 이상 징후 확인에 씁니다.
7. **출시 게이트 (`checkAdIds`)**: `LEVELPLAY_APP_KEY`나 광고 단위 ID가 비어 있거나, 구글 테스트 ID·AdMob ID가 섞여 들어가면 릴리즈 빌드 단계에서 즉시 실패시킵니다.

## 4. 실기기 검증에서 잡은 버그와 실광고 대처

Galaxy S23 Ultra 실기기 무선 디버깅으로 `breakout` 디버그 테스트 빌드를 띄워 `IntegrationHelper`에서 `IronSource 9.8.0 VERIFIED`, `UnityAds 4.22.0 / Adapter 5.17.0 VERIFIED`를 확인했습니다.

이 과정에서 **Play Games Services(PGS) 로그인 팝업이 뜬 상태에서 앱으로 복귀할 때 배너 부착이 누락되는 엣지 케이스**를 잡아 `onHostResume()` 지연 부착 로직을 바로 보완했습니다. 또한 테스트 화면 하단에 실제 광고가 내려온 것을 확인하자마자 클릭하지 않고 게임 중 배너 숨김만 확인한 뒤 즉시 앱을 강제 종료·삭제해 실광고 오노출을 막았습니다.

## 5. 코드 밖에서 챙긴 3가지 정책·운영 항목

SDK만 바꾼다고 끝이 아닙니다. Play 콘솔과 사이트 쪽도 함께 맞춰야 합니다.

- **`app-ads.txt`**: Unity Cloud Monetization에서 내려받은 Authorized Sellers **162줄**과 `ownerdomain=fadongkwon.com`을 사이트 루트 `app-ads.txt`에 반영했습니다.
- **개인정보처리방침**: `https://fadongkwon.com/privacy/`에 Unity 개인정보처리방침 링크를 추가했습니다.
- **Play 데이터 보안 CSV**: 기존 3종(대략적 위치·앱 상호작용·기기 ID)에 애널리틱스·사기 예방 목적을 추가하고, `앱 활동 > 기타 작업`과 `앱 정보 및 성능 > 진단` 2종을 신규 선언했습니다.

## 6. 전환 순서 전략: 신작 선제 → 기존 앱 묶음 전환

시범 2종(`breakout v1.2.2`, `gonu v1.0.4`)을 먼저 올린 뒤, 기존 100여 개 앱을 한꺼번에 건드리는 대신 순서를 바꿨습니다.

1. **미출시 신작 7종 선제 심사 제출**: 어차피 첫 심사를 받아야 하는 앱들이니 처음부터 LevelPlay를 넣어 제출했습니다(이 중 6종은 11월 24일 승인 완료).
2. **기존 라이브 앱 순차 전환**: 10종씩 묶어 P2 1차 10종, P2 2차 10종을 LevelPlay + Firebase Analytics 구성으로 전환하고 있습니다.

아직 전체 앱 이관이 끝난 것은 아니지만, `levelplay-<id>.properties` 파일만 추가하면 같은 파이프라인으로 안전하게 넘어갈 수 있는 틀은 완성됐습니다. 나머지 앱 전환과 실트래픽 체결 결과는 데이터가 쌓이는 대로 이어서 기록하겠습니다.
