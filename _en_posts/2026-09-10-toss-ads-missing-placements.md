---
title: I Shipped Ten Mini Games With No Ads — The Apps Were Done, the Ad Slots Were Never Created
description: "On September 8 I launched ten mini games on Apps in Toss, and every one of them shipped with an empty ad slot because I never created the ad placements in the console. Nothing errored, so it took two days to notice. How I found a configuration gap that fails silently, and why fixing it in the console is not the end of it"
date: 2026-09-10 01:06:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/toss-ads-missing-placements/
alt_url: /posts/toss-ads-missing-placements/
image:
  path: /assets/img/20260910_missing-placements/cover.png
  alt: An empty ad slot where a banner should be
tags: [apps in toss, in-app ads, mini app, monetization, solo developer, dev log]
---

On September 8 I launched ten mini games on Apps in Toss: 2048, Brick Breaker, Pixel Pong, Gomoku, Sky Jump, Solitaire, Number Slide, Minesweeper, Snake and Tower Stack.

All ten shipped **serving no ads at all.**

Nothing was broken. The games run perfectly, and the code that attaches ads was all there. What was missing was not code — it was **the step where you create the ad placements in the console.** With nothing to request, the space where an ad should be was simply empty.

## What was missing

Wiring in-app ads on Apps in Toss takes two sides:

1. **The console**: for each mini app you create ad placement groups — one per format, like a bottom banner, an interstitial and a rewarded slot. Creating one issues a `groupId`.
2. **The app**: you put that `groupId` in your code and request ads through the SDK.

I had only done part two. The game code had the banner mount point, the flow that shows an interstitial when a round ends, and the handler that trades a rewarded view for a hint. But part one never happened, so there was no `groupId` to put anywhere, and the apps shipped requesting nothing.

The previous batch of six was fine. Look up Sudoku in the console and you find three placements — bottom banner, interstitial and rewarded (hint) — created on September 4, by hand, the day after release. In the next batch of ten, that step vanished entirely.

## Why it vanished

Shipping ten at once multiplied the per-app console work: store listing, screenshots, category and keywords, age rating, privacy policy, review submission. Do that ten times over and the feeling of "shipped" arrives the moment you hit submit for review.

But **ad placements live on a different screen from the release flow.** Following the release steps never takes you through that menu. For the six, I went in separately the day after — and because that was a memory rather than a procedure, it did not repeat for the next batch.

Memory is enough when you ship one app. It is not enough when you ship ten.

## Why two days went by

This is the character of the failure: **nothing fails.**

- The app throws no error. The ad area is just empty and the game is fine.
- The console raises no warning. There is no "this mini app has no ad placements" notice.
- Users are not inconvenienced. If anything the games feel cleaner without ads.

The only signal is revenue that never arrives — and zero revenue from ten freshly launched apps **does not look wrong.** It reads as "nobody has found them yet." That is exactly how I read it.

## How I found it

Comparing per-app ad revenue on console screens had become impractical, so I had started pulling the whole workspace report into a ledger as a date-by-app table. Looking at that table, something stood out.

The ten new games **had no rows at all.**

Not rows showing zero revenue — no rows. Which means zero impressions. If nobody had found the games, impressions would be low, not zero. Meanwhile the earlier six were logging dozens of impressions a day over the same period.

There is a lesson in that. **Zero impressions and zero revenue are different signals.** Zero revenue is ordinary — if no ad wins the auction you can have impressions and still earn nothing. Zero impressions means you never requested an ad. Those two do not belong in the same column on a dashboard.

## What it cost

About two days, from launch on September 8 until I noticed. Two days of ad revenue across ten apps, gone.

Honestly, the amount is small. Scaled from what the earlier six earned over the same window, it is a few hundred won a day. Less than a cup of coffee.

What actually stings is not the amount but that **there is no way to get it back.** The people who played during those two days have already moved on. The time spent building the games and the effort spent walking the release process are unchanged; only what that window could have produced is gone. And not because a line of code was wrong — because I did not open one screen.

## Fixing it does not end in the console

This is the second painful part. Creating the placements is not the finish line.

1. Create placements per mini app in the console. Ten games × banner, interstitial and rewarded is thirty of them.
2. Put each issued `groupId` into that game's configuration.
3. Rebuild the bundle and **submit it to Apps in Toss for review again.**
4. Ads only serve once that review passes.

So something that should have been done in one release now costs **another full review cycle.** That wait, more than the two lost days, is the real price. That work is underway now, and ads will appear once review clears.

## What changes for the next batch

Things I wrote down so this does not repeat.

**Monetization goes into the launch checklist.** Until now the checklist ended at "visible in the store." Creating ad placements moves inside it. The further a step sits from the main flow, the more it needs to be written down.

**Watch for zero impressions.** I already have a ledger that shows per-app impressions daily, so a released app sitting at zero impressions should be impossible to miss. Configuration that fails silently is caught by metrics, not by memory.

**Look at the ad slot on a real device right after launch.** Checking only that features work is the direct cause here. Confirming a banner is where a banner should be takes ten seconds. Missing [a vertical-scroll bug across fifteen apps for weeks](/posts/toss-policy-changes/) came from the same laziness.

**Accept the cost of shipping many apps at once.** Shared code genuinely makes development faster. But the console work you do by hand scales honestly with the number of apps. That, I now know, is the real bottleneck of this approach.

## Closing

I built the thing and never flipped the switch. The apps were finished and the code was ready, and ten of them went out with empty ad slots because I skipped one console screen.

Still, I do not think this lands entirely badly. Without building a ledger that stacks revenue per app, I would not know yet. This is what I paid to learn why making numbers visible matters.

Introductions to all ten go up one a day starting tomorrow. The story behind the previous six is in [Shipping Six Mini Games at Once](/en/posts/six-games-retrospective/).

My apps are on [Google Play and Apps in Toss](/en/posts/apps-in-toss-launch/), and some can be [played right in the browser](/en/play/). Updates go out here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
