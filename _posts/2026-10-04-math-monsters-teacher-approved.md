---
title: 수학 몬스터가 구글 플레이 '교사 추천' 앱에 선정됐습니다
description: 신청한 적도 없는데 Play 콘솔에 축하 알림이 와 있었습니다. 교사와 전문가가 수학 몬스터를 직접 검토해 만 6~12세 어린이에게 좋은 앱으로 승인했고, 이제 Play 스토어에 교사 추천 배지가 붙고 키즈 탭 추천 대상이 됩니다. 받은 평가와, 심사에서 두 번 거절당하며 고친 것들이 이 기준과 닮아 있었다는 이야기
date: 2026-10-04 21:35:00 +0900
categories: [Devlog, Retrospective]
tags: [수학몬스터, 교사추천, 구글플레이, 유아교육, 초등수학, 자녀교육, 1인개발자, 개발일지]
pin: true
image:
  path: /assets/img/20261004_math-monsters-teacher-approved/play-badge.png
alt_url: /posts/math-monsters-teacher-approved/
---

## Info
> Math Monsters, our arithmetic game for kids, has joined Google Play's Teacher Approved program. We never applied: apps made for children are reviewed by teachers and specialists automatically, and the approval arrived as a notification on 30 September 2026. The app now shows the Teacher Approved badge on Google Play and can be featured in the Kids tab. Here is what the reviewers noted, and why the fixes we made after two store rejections turned out to point the same way.
{: .prompt-info }

## 신청한 적 없는 축하 알림
Play 콘솔 알림을 보다가 9월 30일에 와 있던 알림 하나를 발견했습니다.

![Play 콘솔 알림 — 앱이 교사 추천 프로그램에 포함되었습니다](/assets/img/20261004_math-monsters-teacher-approved/notice.png){: w="420" }

**"축하합니다. 앱이 교사 추천 프로그램에 포함되었습니다."**

어디에 신청한 적도, 추천을 부탁한 적도 없었습니다. 생각지도 못한 소식이라 더 기뻤습니다.

## 교사 추천 프로그램이란
구글 플레이가 2020년에 시작한 프로그램입니다. **교사와 아동 교육·미디어 전문가**가 어린이용 앱을 직접 써 보고, 아이들에게 권할 만한 앱을 고릅니다.

- **신청하지 않아도 됩니다.** 어린이를 대상으로 하는 앱은 저절로 교사 검토 대상이 됩니다. 저희가 한 일은 수학 몬스터의 타겟층을 어린이로 정직하게 적은 것뿐입니다.
- **무엇을 보나**: 구글이 밝힌 기준은 이렇습니다. 연령에 맞는 말과 소리, 아이가 혼자 쓸 수 있는 화면, 그림의 질, 아이를 즐겁게 하는지, 건강한 발달과 창의력을 돕는지, 부적절한 내용이 없는지, 그리고 **광고·인앱 결제·다른 앱 홍보가 있다면 아이에게 적절한지**입니다.
- **선정되면**: Play 스토어에 **교사 추천 배지**가 붙고, Google Play **키즈 탭**에 추천될 수 있으며, 앱 상세 페이지에 교사와 전문가의 의견이 실립니다.

## 받은 평가
콘솔의 교사 추천 프로그램 화면입니다.

![Play 콘솔 교사 추천 프로그램 — 상태 승인, 교사와 전문가의 의견](/assets/img/20261004_math-monsters-teacher-approved/program.png){: w="760" }

**상태는 '승인'**, 대상 연령대는 만 6~8세와 만 9~12세, 마지막 검토일은 9월 29일입니다. 공개 스토어 페이지에는 "교사가 만 6~12세 연령대에 적합한 앱으로 승인함"이라고 나옵니다.

교사와 전문가의 의견란에는 이렇게 적혀 있었습니다.

| 항목 | 의견 |
| --- | --- |
| 적합한 연령대 | 만 6~8세 |
| 즐거움과 몰입도 | 인기 주제, 캐릭터 |
| 어린이를 염두에 두고 제작 | 단어 및 소리, 쉬운 사용, 예술 및 애니메이션 |
| 창의력 및 상상력 | 혁신적 |

사칙연산 문제를 풀어 몬스터를 잡는 단순한 게임인데, 창의력 항목에서 '혁신적'이라는 평가를 받았습니다.

지금 Play 스토어의 수학 몬스터 페이지에 들어가면 제목 아래에 **교사 추천** 배지가 보입니다.

![Play 스토어 수학 몬스터 페이지 — 교사 추천 배지](/assets/img/20261004_math-monsters-teacher-approved/play-badge.png){: w="760" }

## 돌아보면, 거절당하며 고친 것들
평가 기준 가운데 '광고·인앱 결제·다른 앱 홍보가 있다면 적절해야 한다'는 항목을 읽다가, 지난 한 달이 떠올랐습니다. 수학 몬스터는 Play 심사에서 두 번 거절당한 앱입니다.

- **8월 말, 첫 번째 거절.** 앱 안의 '다른 앱' 카드에 타로·사주 같은 어른용 앱이 함께 보였습니다. 구글은 아이용 앱 안의 다른 앱 홍보도 광고로 봅니다. 그래서 아이용 앱에서는 아이에게 맞는 앱만 보이게 고쳤고, 광고 SDK도 빌드에서 아예 뺐습니다.
- **9월 초, 두 번째 거절.** 스토어에 적어 둔 웹사이트와 개인정보처리방침 링크가 타로 글이 보이는 블로그 홈으로 이어졌기 때문입니다. 아이용 앱만을 위한 단출한 안내 페이지를 따로 만들어 연결했습니다.
- **9월 5일**, [유료 상품을 전부 없애고](/ko/posts/monsters-go-free/) 모든 모드를 무료로 열었습니다.
- **9월 말**, [별점 요청 창을 넣을 때](/ko/posts/review-prompt-toss-play/)도 아이용 앱은 껐습니다.

그때는 심사를 통과하려고, 또 아이가 쓰는 앱이니 당연하다고 생각해서 고친 것들이었습니다. 이 결정들이 선정에 얼마나 영향을 줬는지는 알 수 없습니다. 다만 교사들이 보는 기준과 같은 쪽을 보고 있었던 건 분명해 보여서, 그 거절들이 헛되지 않았다는 생각이 듭니다.

## 아들 사진이 아이콘이던 앱
수학 몬스터는 처음부터 스토어에 낼 생각으로 만든 앱이 아닙니다. 첫째가 구몬수학을 그만둔 뒤 집에서 연산 연습을 이어 가려고 만든, **아들 사진이 아이콘이던 연습 앱**이었습니다([그 이야기](/ko/posts/kumon-to-math-monsters/)).

아이 한 명을 위해 만든 앱을 교사와 전문가가 다른 아이들에게도 권할 만한 앱이라고 봐 준 셈입니다. 첫째가 자랑하는 '원조 몬스터' 앱에 이제 교사 추천 배지가 하나 붙었습니다.

## 받아 보기
광고도 유료 상품도 없습니다. 회원가입 없이 바로 시작할 수 있습니다.

- Google Play: <https://play.google.com/store/apps/details?id=com.fadongkwon.math_monsters>
- 앱인토스: <https://fadongkwon.com/toss/math-monsters/> — 휴대폰에서 열면 토스 앱으로 바로 연결됩니다.

앱 소개와 플레이 영상은 [수학 몬스터 소개글](/ko/posts/math-monsters/)에 있습니다. 소식은 이 블로그와 [인스타그램(@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/)에서 전해드립니다.
