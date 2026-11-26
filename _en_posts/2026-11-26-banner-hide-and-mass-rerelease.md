---
title: "Hiding Banners in 7 Action Games and Re-Releasing 114 Play Apps in 7 Batches"
description: "We audited banner placement across all 125 Play ad apps, added a 10dp inert gap, system inset padding, and in-gameplay banner hiding for 7 continuous-touch games, then shipped 114 updated AABs in 7 batches."
image:
  path: /assets/img/20261126_banner-hide-and-mass-rerelease/cover.png
  alt: "Banner audit and 114-app batch re-release summary"
date: 2026-11-26 01:15:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/banner-hide-and-mass-rerelease/
permalink: /posts/banner-hide-and-mass-rerelease/
tags: [ad-policy, ads, android, indiedev, devlog]
---

Between November 18 and 20, we audited banner placement across **all 125 ad-supported Play apps** in our monorepo and rolled out a sweeping accidental-click defense update.

Even though our Google publisher account ended on November 19, we kept every single line of this defense intact to protect our new **Unity LevelPlay** account. Here is what the audit found and how we shipped 114 updated AABs safely.

## 1. Auditing All 125 Flavors

We inspected CSS and layout code across every `adsRealFlavors` app (excluding 5 ad-free kids `adsStub` apps) and classified accidental-click risk:

| Risk Tier | Apps | Notes |
|---|---:|---|
| **High** | 20 | 15 standalone + 5 hubs (touch canvas at 0px from bottom, or action buttons within 9–16px) |
| **Medium** | 49 | 45 standalone + 4 hubs (card toolbars, sticky footer buttons) |
| **Low** | 52 | 48 standalone + 4 hubs (comfortable scroll padding) |
| N/A | 4 | Siege series (no banner unit) |

Two wrapper-wide issues stood out immediately:

1. There was **0px gap** between the bottom of the WebView and the top edge of the native banner.
2. Under `targetSdk 36` edge-to-edge, non-immersive flavors lacked bottom system inset padding, causing the banner to slightly overlap the gesture navigation bar on a Galaxy S23 Ultra.

## 2. Four Wrapper-Wide Defenses

- **10dp inert spacer + 1dp divider**: Added a dark (`#101116`) non-interactive 10dp strip between the WebView and banner, and locked the banner container height to adaptive banner height (56dp) before load to eliminate layout shift.
- **System inset padding**: Applied `navigationBars() or displayCutout()` bottom/side padding to non-immersive roots.
- **Play-only 20/day ad cap**: Once rewarded + interstitial views hit 20 in a day, ads are blocked and the banner + spacer collapse (`MiniBridge.setAdsBlocked`).
- **Extra Play-only bottom padding on 26 apps**: Added at least 26dp / 16px inert bottom padding across button-heavy action games, lotto apps, and daily trivia apps.

## 3. Hiding Banners During Gameplay in 7 Continuous-Touch Games

For seven games where players tap or drag all the way to the bottom edge (`tap-bird`, `sky-jump`, `snake`, `breakout`, `survivor-bird`, `pixel-pong`, `reaction`), spacing alone was not enough:

- Added a `setGameplayActive(Boolean)` bridge method.
- When a round starts, the banner switches to **`INVISIBLE`** (not `GONE`, preventing canvas resize jitter) and pauses auto-refresh.
- On game over or pause, the banner waits **1.5 seconds** before reappearing—eliminating stray post-round taps. Starting a new round cancels the timer.
- `WebViewClient.onPageStarted` resets the flag so hub navigation never leaves a banner stuck hidden.

## 4. Shipping 114 Apps in 7 Batches

Out of 125 flavors, 11 were not yet registered on Play. We shipped the remaining **114 live apps** in controlled waves:

- **5-app pilot batch** (`nursingQuiz`, `sajuLotto`, `tapBird`, `boxPush`, `hubArcade`) verified end-to-end (web, AAB, manifest, dex checks) first.
- **7 batches of 15–16 apps** for the remaining 109 apps: hubs and static quizzes first, followed by 93 standalone games.
- Each batch took roughly 15–18 minutes (about 2 hours total), and all 114 updates passed Play production review.

That baseline made the subsequent Unity LevelPlay migration dramatically safer—the accidental-click guardrails were already live everywhere.
