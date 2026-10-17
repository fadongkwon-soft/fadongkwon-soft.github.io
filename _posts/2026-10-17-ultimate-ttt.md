---
title: 얼티밋 틱택토 — 작은 판 9개로 즐기는 틱택토
description: "작은 틱택토 판 9개로 이어 이기는 전략 게임. 내가 둔 칸이 상대가 둘 판을 정해요. 3단계 AI와, 또는 한 폰으로 둘이. Google Play에 출시했습니다"
date: 2026-10-17 19:30:00 +0900
categories: [Products, Game]
tags: [game, android, 보드게임, 2인게임, 1인개발자]
pin: false
image:
  path: /assets/img/20261017_ultimate-ttt/ultimate-ttt-feature.png
alt_url: /posts/ultimate-ttt/
---
## Info
> **Ultimate Tic-Tac-Toe — 9×9** — Tic-tac-toe on nine small boards: where you play inside a small board decides which board your opponent plays in. Play against 3 AI levels or with a friend on one phone. 9 languages.
{: .prompt-info }

## 이런 게임입니다
큰 판 안에 작은 틱택토 판 9개가 들어 있는 틱택토예요. 작은 판에서 3개를 이으면 그 판을 차지하고, 큰 판에서 **차지한 작은 판 3개를 한 줄로** 이으면 이겨요.

보통 틱택토와 다른 점은 딱 하나예요. **내가 작은 판의 어느 칸에 두느냐가 상대가 다음에 둘 작은 판을 정해요.** 그래서 한 수 한 수가 "내 칸"이면서 "상대에게 보내는 판"이 돼요.

## 어떻게 하나요
- 작은 판의 아무 칸에 두면, 상대는 **그 칸과 같은 위치의 작은 판**에 둬야 해요. 예를 들어 오른쪽 위 칸에 두면 상대는 큰 판의 오른쪽 위 작은 판에 둬요. 둘 판은 파란 테두리로 표시돼요
- 보낸 판이 이미 끝났으면(누가 이겼거나 칸이 꽉 참) 상대는 아무 열린 판에나 둘 수 있어요. 상대를 끝난 판으로 보내면 오히려 자유를 주는 셈이니 조심하세요
- 작은 판에서 가로·세로·대각선으로 3개를 이으면 그 판을 차지해요. 차지한 판은 큰 X 또는 O로 덮여요
- 큰 판에서 내 판 3개를 한 줄로 이으면 승리! 더 둘 곳이 없으면 무승부예요

처음이라면 **클래식 3×3** 판으로 시작해 보세요. 보통 틱택토 한 판이라 손에 익히기 좋아요.

## 모드와 난이도
- **컴퓨터 대전 3단계**: 쉬움은 처음 배운 사람이 절반쯤 이기는 수준이에요. 보통은 쉬움을 확실히 이기고, 어려움은 한 수에 0.5초쯤 생각하며 앞을 꽤 멀리 봐요
- **선공 선택**: 내가 먼저, 컴퓨터가 먼저, 무작위
- **2인 대전**: 한 폰으로 번갈아 두는 대전

## 특징
- 얼티밋 9×9 판과 클래식 3×3 판
- 지금 둘 수 있는 판을 강조하고 나머지는 어둡게 — 어느 판에 둬야 하는지 한눈에 보여요
- 차지한 판은 큰 X/O로 덮고, 마지막 수는 표시해요
- 무르기, 판 종류·난이도별 승·패·무 전적
- 요령을 알려 주는 게임 방법 안내, 9개 언어 지원

![정해진 판(파란 테두리)과 차지한 판이 보이는 컴퓨터 대전 중](/assets/img/20261017_ultimate-ttt/ultimate-ttt-shot-ko-1.png){: w="360" }
![컴퓨터를 이긴 결과 화면](/assets/img/20261017_ultimate-ttt/ultimate-ttt-shot-ko-2.png){: w="360" }
![홈 — 판 종류·난이도·선공 선택](/assets/img/20261017_ultimate-ttt/ultimate-ttt-shot-ko-3.png){: w="360" }

## 플레이 영상
{% include embed/youtube.html id='HdQ5zC4jOHc' %}

## Download
- Google Play: <https://play.google.com/store/apps/details?id=com.fadongkwon.ultimate_ttt>

![얼티밋 틱택토 Google Play QR 코드](/assets/img/play-qr/ultimate-ttt.png){: w="200" .normal }

## 함께 출시된 보드게임
같은 날 Google Play에 함께 나온 보드게임들입니다.

- [백개먼](/ko/posts/backgammon/)
- [모리스](/ko/posts/morris/)
- [헥스](/ko/posts/hex/)
- [아마존스](/ko/posts/amazons/)

다른 보드게임도 있어요: [오목](/ko/posts/gomoku/) · [리버시](/ko/posts/reversi/) · [한판 바둑](/ko/posts/mini-go/)

소식은 이 블로그와 [인스타그램(@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/)에서 전해드립니다.
