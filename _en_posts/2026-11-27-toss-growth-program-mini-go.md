---
title: "Quick Go Was Selected for the Apps in Toss Growth Program — Preparing for November 30 With Lessons From Tap Bird and Gomoku"
description: "Following Tap Bird and Gomoku in October, Quick Go is my third app selected for the Apps in Toss growth program. Starting November 30, Toss will automatically run a 'browse and earn points' promotion. Applying what I learned from the previous D+7 results—age fit, verifying the first screen before launch, event tracking, and review timing—here is the baseline and retention plan for Quick Go."
image:
  path: /assets/img/20261127_toss-growth-program-mini-go/cover.png
  alt: Apps in Toss growth program selection email — Quick Go has been selected for the growth program
date: 2026-11-27 20:45:00 +0900
pin: true
categories: [Devlog, Platform]
permalink: /posts/toss-growth-program-mini-go/
alt_url: /ko/posts/toss-growth-program-mini-go/
tags: [apps in toss, toss, mini app, solo developer, dev log]
---

On the afternoon of November 27, another welcome email arrived from Apps in Toss: [Quick Go](/posts/mini-go/) has been selected for the **Apps in Toss Growth Program**. After [Tap Bird](/posts/toss-growth-program-tap-bird/) and [Gomoku](/posts/toss-growth-program-gomoku/) in late October, this is my third app to make the list.

The promotion starts automatically on **Monday, November 30**. As before, Toss funds and runs a "browse the mini-app and earn points" promotion, then watches whether those visitors come back once it ends.

## One big change from last time

One line in the email immediately stood out:

> "You can choose the age group of users who join the promotion, or exclude users who participated recently."

Back in October with Tap Bird and Gomoku, the campaign belonged to Toss and we could not choose the audience at all—the only editable field was the landing screen. As I documented in [the D+7 results post](/posts/toss-growth-program-d7-result/), roughly three-quarters of the Benefits tab traffic was age 50 and older.

Receiving the exact same audience, Gomoku kept 1.0% (215 users) the week after the promotion ended while Tap Bird kept 0.14% (30 users)—a **sevenfold gap**. That made it unmistakable how much audience-game fit decides the outcome.

Go (Baduk) is one of the strongest natural fits for older players on Toss, and this time the console also lets us target age groups and exclude recent participants. On paper, Quick Go is starting from a much better position than the first two apps.

## Quick Go's baseline before launch (Nov 12–26)

I pulled the current numbers from the console dashboard before the promotion begins.

| Metric | Value (Nov 12–26) |
| --- | --- |
| Daily active users (DAU) | 13–27 (avg ~20) |
| Average session length | ~241 seconds (~4 minutes) |
| Weekly retention (new cohorts) | Week 1: 6.3% (latest week 8.4%), Week 2: 3.1% |
| Age breakdown | Teens 44%, **50+ 47%** (60+ 37%) |
| Gender / OS | Male 67% · Female 33% / Android 88% |

An average session of roughly four minutes is longer than Gomoku's (192 seconds) and nearly five times Tap Bird's (51 seconds). Once players sit down at the board, they stay.

## Lessons from Tap Bird and Gomoku — and what Quick Go still needs

With Tap Bird and Gomoku, I patched the first screen and fixed a landing-URL detection bug only after the promotion had already started, so more than 7,000 visitors saw the old home screen over the first three days. This time, I want the fundamentals ready **before November 30**.

Looking at Quick Go's current home screen, it has almost the exact same gaps Gomoku had in October:

1. **The first screen is a settings form.** Right under the title sits a "vs. computer: 0W 0L 0D" card followed by seven option tiles (mode, board size, difficulty, color, komi, handicap, confirm-to-place). During a 10-second browse, the Go board never appears.
2. **No instant-play growth entry.** There is no `?from=growth` path yet to skip the home screen and open an Easy 9×9 board ready for the first stone.
3. **Event logging (`logEvent`) is missing from the Toss wrapper.** To avoid losing funnel data like last time, I need to wire up `logEvent` using the SDK's `{ log_name, log_type, params }` contract and archive daily logs before the console's 14-day window expires.
4. **No daily reason to return.** Just as Gomoku's Daily Puzzle, streaks, and next-day reminder gave players a reason to come back, Quick Go needs a quick daily loop—such as a 1-minute **Daily Life-and-Death / Capture Puzzle**, streaks, and Toss Game Center ranking.

One thing is already covered: the latest live bundle (`20261126-4`, deployed November 26) already includes the fix to [only prompt for a review after a win](/posts/review-prompt-after-win/), preventing the wave of 1-star ratings that hit Gomoku after losses.

## Plan around November 30

- **Before launch (by Nov 30):** Review the console's age targeting and recent-participant exclusion settings, and prepare a first-screen patch (`?from=growth` instant 9×9 game + board preview / folded settings on home) along with `logEvent` tracking, verified on a real device.
- **During the promotion:** Roll out daily retention hooks (Daily Life-and-Death puzzle, streak tracking, Toss ranking) and archive daily funnel metrics separately.
- **D+7 after the promotion ends:** Just like with Tap Bird and Gomoku, I will share the exact post-promotion return numbers once a full week has passed.

My apps are listed under [GAMES](/games/) and [APPS](/apps/), and several can be tried [right in the browser](/play/). Updates are posted here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> Baseline metrics were pulled from the Apps in Toss console dashboard on November 27, 2026 (covering Nov 12–26). Post-promotion D+7 return results will be published in a follow-up post.
{: .prompt-info }
