---
title: 앱인토스에 3개 앱 출시 (Apps in Toss Launch)
description: 사주로또, 주스 스피너, 병 돌리기를 토스 미니앱으로 만나보세요
date: 2026-08-12 21:30:00 +0900
categories: [Blogging, Episode]
tags: [앱인토스, Apps in Toss, 토스, 미니앱, 사주로또, 주스 스피너, 병 돌리기, Flutter, Flutter Web, 1인개발자]
pin: false
math: true
mermaid: true
image:
  path: /assets/img/20260812_apps-in-toss/icon.png
---
## Info
> Our three apps — **Saju Lotto**, **Juice Spinner**, and **Spin the Bottle** — are now
> available as mini-apps on **Apps in Toss**, running inside the Toss app with no separate
> install. Search for each app inside Toss, or open the links below on a phone with Toss installed.
{: .prompt-info }

## 앱인토스란?
[앱인토스(Apps in Toss)](https://apps-in-toss.toss.im/)는 토스 앱 안에서 미니앱을 바로 실행할 수 있는
플랫폼입니다. 별도 설치 없이 토스만 있으면 어떤 앱이든 몇 초 만에 열 수 있습니다.

Google Play에 올려둔 세 앱을 Flutter Web으로 포팅해 토스 미니앱으로 출시했습니다.
같은 코드베이스에서 스토어 버전과 미니앱 버전을 함께 관리합니다.

## 출시 앱

### 사주로또 (Saju Lotto)
생년월일시(사주)로 나만의 로또 번호를 만들어 주는 앱입니다. 같은 사주는 같은 기간에
항상 같은 번호를 받는 결정론 방식이라, 매주 "내 번호"가 생기는 재미가 있습니다.
로또형(범위 지정)과 연금복권 720+형을 지원하고, 번호 저장·지난 회차 당첨 확인·
'내 사주로또 운' 시뮬레이션까지 토스 안에서 그대로 동작합니다.

- 열기: `intoss://saju-lucky-number` — 아래 QR을 폰 카메라로 찍으면 바로 열립니다

![사주로또 QR](/assets/img/20260812_apps-in-toss/qr-saju-lotto.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/saju-input.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/saju-result.png){: .w-25 .normal}

### 주스 스피너 (Juice Spinner)
인원 수(2~12명)와 과일을 고르고 돌리는 복불복 룰렛입니다. 음료 내기, 청소 당번 정하기,
순서 정하기 등 모임에서 가볍게 쓰기 좋습니다.

- 열기: `intoss://juice-spinner` — 아래 QR을 폰 카메라로 찍으면 바로 열립니다

![주스 스피너 QR](/assets/img/20260812_apps-in-toss/qr-juice-spinner.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/juice-main.png){: .w-25 .normal}

{% include embed/youtube.html id='6fmDzfNP6aA' %}

### 병 돌리기 (Spin the Bottle)
클래식한 병 돌리기를 그대로 옮겼습니다. 소주·맥주·와인 등 9종의 병 중에 골라 돌리면
병 입구가 가리키는 사람이 당첨. 벌칙 정하기, 진실게임까지 자리에 맞게 활용해 보세요.

- 열기: `intoss://spin-the-bottle` — 아래 QR을 폰 카메라로 찍으면 바로 열립니다

![병 돌리기 QR](/assets/img/20260812_apps-in-toss/qr-spin-the-bottle.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/bottle-main.png){: .w-25 .normal}

{% include embed/youtube.html id='7pIVdiZN86M' %}

## 뒷이야기
Flutter 앱을 토스 WebView 미니앱으로 옮기면서 겪은 것들이 꽤 많았습니다.
20초 로딩 게이트를 넘기 위한 번들 다이어트(CanvasKit·한글 폰트를 전부 앱에 내장해
외부 요청 0건), 전면 광고 뒤 렌더링이 멈추는 WebView 이슈 우회, 웹 전용 오디오 교체 같은
작업들이었는데, 이 과정은 기회가 되면 별도 포스트로 정리해 보겠습니다.

## Download
> 토스 앱에서 **사주로또**, **주스 스피너**, **병 돌리기**를 검색하거나, 각 앱의 QR을 폰 카메라로
> 찍어주세요(토스가 설치돼 있어야 합니다). Google Play 버전은 각 앱의 제품 포스트에서 확인할 수 있습니다.
{: .prompt-tip }
