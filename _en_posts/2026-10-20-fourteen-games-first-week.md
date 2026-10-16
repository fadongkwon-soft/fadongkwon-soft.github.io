---
title: One Week After Launching 14 Games on the Same Day — Closing a Launch With D+1 and D+7 Checks
description: On October 9 I launched five retro games and nine board games on Toss on the same day. A launch counts as done not when it goes live but when D+1 metrics and push notifications actually register, the first reviews are checked on D+7, and the automated gate passes. Here are the conversion metrics for all 14, impressions per ad placement, how push sends relate to consenting users, zero reviews, and two places where the tooling was wrong along the way
image:
  path: /assets/img/20261020_fourteen-games-first-week/cover.png
  alt: Closing the launch of 14 games with D+1 and D+7 checks
date: 2026-10-20 09:30:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/fourteen-games-first-week/
alt_url: /ko/posts/fourteen-games-first-week/
tags: [minigame, apps in toss, google play, solo developer, dev log]
---

On October 9 I launched [five retro games](/posts/retro-games-retrospective/) and [nine board games](/posts/board-games-retrospective/) on Toss on the same day. They had gone live on Play earlier. This post is not a launch retrospective; it is a record of **how the launch was closed**.

## Defining "launch complete"

Our launch checklist runs about 150 lines per app, and the final section is the **closing gate**. Every automated check must pass (the banner does not cover UI, the back button does not quit the app, the first load makes no external requests, there are at least four screenshots, and so on), and the checklist must have no unverified items left.

Three of those items cannot be verified on launch day.

- **D+1 key metrics**: do the conversion metrics configured in the console actually record values? Right after setup the console only says "available from tomorrow."
- **D+1 push**: did the daily 8 p.m. notification actually go out? Same-day counts are zero.
- **D+7 first reviews**: are there first reviews on both Play and Toss? Sometimes reviews appear only on Toss, so both are checked.

So after launch the apps stayed in a "released, pending verification" state, and a week later, on October 16, I closed all 14 at once.

## D+1 metrics: all 14 registered

Toss console conversion metrics can be pulled as daily time series through the API. For all 14, the primary conversion, "users who watched an in-app ad," registered every day from the day after launch. On their best day Yut Nori had 61 users, Box Push 38 and Four in a Row 38, and even the lowest, Checkers, had 21. The numbers themselves are not the point; the point is confirming **the metric wiring is alive**.

The activation metric API is not open, so that was left to the console screen. Since conversions register through the same event path that activation uses, the gate was closed on the conversion values.

## Ad impressions: zero rewarded was not a defect

The ad placement report gives daily impressions per placement. Banners had impressions every day on all 14 (122 to 316 for the week). Interstitials varied by game.

What stood out was that **rewarded impressions were zero on all nine board games**. My first thought was a missing placement, but the code simply has no path that calls a rewarded ad. Board games have no hint or revive moment where a rewarded ad would go. The placements exist in the console and are unused. Toss marks a placement for deletion after 23 days without impressions, and since there is no plan to use them, I left them alone.

## Push: not unsent, just nobody to receive it

Functional push notifications only go to users who opted in. Of the 14, seven recorded sends (Yut Nori 8, Make Ten 8, Box Push 7, Four in a Row 7, Dots and Boxes 5, Reversi 1, Checkers 1) and seven recorded zero.

For the seven at zero, the conversion metric "users who agreed to notifications" was also zero. The templates were created with the same code on the same day, and the seven that sent prove the sending side works, so I judged it **not a wiring problem but simply no consenting users yet**, and closed the item. Sends will start automatically once someone opts in.

The tooling tripped once here. The API that lists push templates **returns zero templates unless the smart-message flag is set, even when templates exist**. The first query came back as "no templates," which was alarming, but with the flag on all 14 appeared. It was a trap I had hit before and written down, which is why it was found quickly.

## D+7 reviews: zero on both stores

The Play reviews API only returns reviews with text from the last seven days. All 14 had zero. Toss has no public reviews API, so I call the same-origin REST endpoint from a browser logged into the console. Also zero for all 14, and none in the previous day's collection either.

Zero reviews in a week is disappointing but not unusual. Existing games that now have Toss reviews only started getting them several weeks after launch.

## Closing

I recorded the three items with evidence in all 14 checklists and ran the closing gate. All 14 passed. The two entries for retro and board games on the execution checklist were marked complete and committed.

## Summary

- Define launch complete as **the day D+1 metrics and push, and D+7 reviews, have been verified**, not the day it goes live, and nothing slips through.
- Zero impressions or zero sends may or may not be a defect. You need the code path and the consenting-user count together to decide.
- APIs have traps where a single flag turns the result into zero. Once bitten, write it down.
