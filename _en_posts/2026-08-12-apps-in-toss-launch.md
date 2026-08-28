---
title: Apps in Toss Launch — Saju Lotto, Juice Spinner & Spin the Bottle
description: Three of our Android apps are now Toss mini apps you can open inside Toss with no separate install — Saju Lotto, Juice Spinner, and Spin the Bottle.
image:
  path: /assets/img/20260812_apps-in-toss/icon.png
  alt: Apps in Toss launch
date: 2026-08-12 21:30:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/apps-in-toss-launch/
alt_url: /posts/apps-in-toss-launch/
---
## Info
> Our three apps — **Saju Lotto**, **Juice Spinner**, and **Spin the Bottle** — are now
> available as mini-apps on **Apps in Toss**, running inside the Toss app with no separate
> install. Search for each app inside Toss, or open the links below on a phone with Toss installed.
{: .prompt-info }

## What is Apps in Toss?
[Apps in Toss](https://apps-in-toss.toss.im/) is a platform that runs mini apps directly inside
the Toss app. Nothing to install — if you have Toss, any app on it opens in a few seconds.

I ported three apps already on Google Play to Flutter Web and shipped them as Toss mini apps.
The store builds and the mini app builds live in the same codebase.

## The apps

### Saju Lotto
Saju Lotto generates lottery numbers from your birth date and time — your saju, the traditional
Korean four-pillars birth chart. The draw is deterministic, so the same birth details always
return the same numbers for the same period, which is what makes it feel like you have "your
numbers" each week. It supports both range-style lotto games and the Pension Lottery 720+ format,
and saving numbers, checking past draws, and the "my Saju Lotto luck" simulation all work
the same way inside Toss.

- Open: [Open Saju Lotto in Toss](https://fadongkwon.com/toss/saju-lucky-number/) — or scan the QR code below with your phone camera

![Saju Lotto QR code](/assets/img/20260812_apps-in-toss/qr-saju-lotto.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/saju-input.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/saju-result.png){: .w-25 .normal}

### Juice Spinner
Pick a group size (2 to 12 people) and a set of fruits, then spin. It is the kind of roulette you
reach for when someone has to buy the drinks, take the cleaning shift, or go first.

- Open: [Open Juice Spinner in Toss](https://fadongkwon.com/toss/juice-spinner/) — or scan the QR code below with your phone camera

![Juice Spinner QR code](/assets/img/20260812_apps-in-toss/qr-juice-spinner.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/juice-main.png){: .w-25 .normal}

{% include embed/youtube.html id='6fmDzfNP6aA' %}

### Spin the Bottle
The classic party game, straight across. Choose from 9 bottles — soju, beer, wine and more —
give it a spin, and whoever the neck points at is picked. Good for deciding forfeits or starting
a round of truth or dare.

- Open: [Open Spin the Bottle in Toss](https://fadongkwon.com/toss/spin-the-bottle/) — or scan the QR code below with your phone camera

![Spin the Bottle QR code](/assets/img/20260812_apps-in-toss/qr-spin-the-bottle.png){: .w-25 .normal}
![Desktop View](/assets/img/20260812_apps-in-toss/bottle-main.png){: .w-25 .normal}

{% include embed/youtube.html id='7pIVdiZN86M' %}

## Behind the scenes
Moving a Flutter app into a Toss WebView mini app turned up plenty of surprises. Getting under
the 20-second load gate meant putting the bundle on a diet — CanvasKit and the Korean fonts are
now all embedded in the app, so there are zero external requests. I also had to work around a
WebView issue where rendering stalls after an interstitial ad, and swap in web-only audio.
I will write that up as a separate post when I get the chance.

## Download
> **Tap one of the "Open in Toss" links above from your phone**, or scan the QR code with your
> phone camera (you need Toss installed). You can also search for each app by name inside Toss.
> The Google Play versions are linked from each app's own product post.
{: .prompt-tip }
