---
title: "광고만 바꾸지 않았다: Firebase Analytics를 AAID 끄고 아동 앱 빼고 붙인 이유"
description: "AdMob 정지 당일 리포트 API가 401로 닫히며 게시자 손에 남은 차원은 날짜와 앱뿐이었습니다. 같은 상황을 다시 겪지 않기 위해 Firebase Analytics를 선택적 통합하되, AAID·SSAID·광고 개인맞춤 신호를 끄고 아동 대상 앱은 완전히 배제한 설계를 기록합니다."
date: 2026-11-26 01:10:00 +0900
categories: [Devlog, Retrospective]
tags: [파이어베이스, 애널리틱스, 개인정보, 안드로이드, 아동앱, 1인개발자, 개발일지]
pin: false
image:
  path: /assets/img/20261126_firebase-analytics-opt-in/cover.png
alt_url: /posts/firebase-analytics-opt-in/
---

11월 18일 AdMob 계정이 멈춘 날 가장 답답했던 점은 [이의신청 기각 글](/ko/posts/google-ads-appeal-rejected/)에도 적었듯 **"책임은 게시자가 지는데, 정작 트래픽의 생김새를 볼 데이터가 내 손에 없다"**는 사실이었습니다. 정지 당일 AdMob 리포트 API는 401을 돌려줬고, 콘솔 세부 화면도 닫혔습니다. 제가 가진 장부에는 날짜와 앱별 합계뿐이었습니다.

Unity LevelPlay로 광고 네트워크를 옮기면서 같은 실수를 되풀이하지 않기로 했습니다. 광고 플랫폼 대시보드만 바라보지 않고, **최소한의 자체 트래픽·광고 이벤트 관측망**을 따로 두는 것입니다. 그래서 11월 23일 `apps-in-toss-games` Android 래퍼에 **Firebase Analytics 선택적 통합**을 넣었습니다. 다만, 아무 앱에나 기본 설정 그대로 붙이지는 않았습니다.

## 1. 원칙 세 가지: 선택적·비식별·아동 배제

Firebase Analytics를 붙일 때 가장 먼저 정한 제약은 세 가지였습니다.

1. **아동 대상 앱 완전 배제**: `math-monsters`, `hangul-monsters`, `english-monsters`, `hub-monsters`, `korean-history` 등 아동·가족 정책 대상(`adsStub`) 앱에는 Firebase SDK 자체를 넣지 않고, 초기화 경로에도 태우지 않습니다.
2. **광고 식별자·개인맞춤 신호 차단**: 우리가 필요한 건 "어느 앱에서 갑자기 비정상적인 노출·클릭·세션이 튀었는가"이지, 사용자 프로파일링이나 리타게팅이 아닙니다.
3. **flavor 단위 선택적 활성화**: `adsLevelPlay` 전환 대상 앱에만 `AnalyticsTracker.kt`를 연결하고, 나머지 flavor에는 빈 스텁(`no-op`)을 둬서 빌드와 동작에 영향이 없게 분리했습니다.

## 2. 매니페스트에서 광고 신호 4종을 명시적으로 껐다

`android/app/src/adsLevelPlay/AndroidManifest.xml`과 가로 전용 `adsLevelPlayLandscape/AndroidManifest.xml`에 아래 메타데이터 4개를 박아 넣었습니다.

```xml
<meta-data
    android:name="google_analytics_adid_collection_enabled"
    android:value="false" />
<meta-data
    android:name="google_analytics_ssaid_collection_enabled"
    android:value="false" />
<meta-data
    android:name="google_analytics_default_allow_ad_personalization_signals"
    android:value="false" />
<meta-data
    android:name="google_analytics_default_allow_ad_user_data"
    android:value="false" />
```

- **AAID 수집 비활성화**: Firebase Analytics가 Google 광고 ID를 읽지 않습니다.
- **SSAID 수집 비활성화**: Android ID 기반 기기 식별도 끕니다.
- **광고 개인맞춤·광고 사용자 데이터 기본 비활성화**: 수집된 이벤트가 광고 타게팅 신호로 흘러 들어가지 않게 막습니다.

이렇게 해 두면 Play 데이터 보안 양식과 개인정보처리방침을 설명할 때도 "광고 타게팅용 식별자가 아니라 앱 진단·이벤트 집계용"이라는 경계가 코드 수준에서 명확해집니다.

## 3. 소스셋 분리: 본체 코드는 Firebase를 모른다

`adsLevelPlay` 소스셋에 실제 `AnalyticsTracker.kt`(82줄)를 두고, 기본 `main`(또는 비대상 소스셋)에는 14줄짜리 빈 스텁 `AnalyticsTracker.kt`를 뒀습니다.

- `MainActivity.kt`와 `AdManager.kt`는 `AnalyticsTracker`의 얇은 메서드만 호출합니다.
- Firebase `google-services.json`도 `.gitignore`로 관리하고, Gradle 설정(`build.gradle.kts`)에서 대상 flavor에만 선택적으로 플러그인과 의존성을 적용합니다.
- 덕분에 아동 앱이나 미전환 앱을 빌드할 때 Firebase 클래스나 초기화가 섞여 들어갈 틈이 없습니다.

## 4. 지금 적용 범위

11월 23~25일 사이 아래 앱들에 LevelPlay 전환과 함께 Firebase Analytics를 차례로 반영했습니다.

- 시범 2종(`벽돌깨기`, `고누`)
- 11월 24일 Play 신규 승인 6종(`나사 퍼즐 블록`, `분식집 머지`, `번호 낚시`, `파동권 공성전`, `철퇴 공성전`, `당구 공성전`)
- 기존 라이브 앱 P2 1차 10종 + 2차 10종 (정적 퀴즈 앱 누락분 보완 포함)
- 미출시 4종(`파동권 건강생활`, `스트레칭 루틴`, `칼로리 사전`, `자연휴양림 지도`) 콘솔 ID 등록 및 연결

광고 계정이 닫혀도 내 앱에서 어떤 화면·어떤 국가·어떤 OS에서 비정상 트래픽이 튀었는지 스스로 확인할 수 있는 최소한의 블랙박스를 만든 셈입니다. 앞으로 나머지 Play 앱을 LevelPlay로 넘길 때도 이 구성을 기본 세트로 함께 묶어 나갈 계획입니다.
