---
title: Adding Hearts to Games With Nowhere to Put a Rewarded Ad
description: Pure score games have no hint, no undo and no revive, so there is no hook to hang a rewarded ad on. Here is the shared entry-ticket module we built for seven games, and the two traps we walked into
date: 2026-09-15 01:00:00 +0900
categories: [Blogging, Episode]
permalink: /posts/rewarded-ads-hearts/
alt_url: /ko/posts/rewarded-ads-hearts/
tags: [ads, rewarded ads, apps in toss, google play, solo developer, devlog, TypeScript]
---
## Info
> Rewarded ads need a hook — a hint, an undo, a revive. Pure score games have none, so we built a shared "hearts" entry ticket that is unrelated to gameplay: one heart per run, refilled to the daily amount by one ad, reset every day. This post covers the four rules and the two traps we hit.
{: .prompt-info }

## A Rewarded Ad Needs Somewhere to Live
There are two kinds of ads. Interstitials, which interrupt, and rewarded ads, which people choose to watch because they want something.

The second kind pays better and is resented less. The catch is that **it needs somewhere to live.**

Games with hints, undo or revive are easy. Put the ad in front of that feature and you are done.
Games that only measure a score have no such place. What would a hint mean in Reaction Challenge? Undo in Number Rush is simply cheating.

So we used a ticket that has **nothing to do with the game itself.** Hearts.

## Only Four Rules
- 🎟️ **One heart per run** — regardless of how many people play. Four players on Reaction Challenge is still one run, one heart
- 📺 **One ad refills a full day's worth** — and only when the player taps it themselves
- 🌅 **Reset to the daily amount when the date changes** — hearts do not pile up
- 🏁 **A run already underway finishes** — hitting zero never cuts a game short

The third rule matters most. Allowing hearts to accumulate rewards whoever watches the most ads, and at that point **ads become the only way to keep playing.** With a daily reset, someone who never watches a single ad still gets the daily allowance every day.

## One Heart Per Ad Was Too Harsh
Tarot Fortune had hearts before the others. At first one ad gave one heart.
That is exactly one card draw — it disappears the moment you use it. You watch an ad and feel like you got nothing.

So an ad now **refills the whole daily amount.**
If an app gives five hearts a day and an ad returns three, watching it does not even restore your day. That reads as a penalty, not a reward.

## Trap One — Locking a Door Where No Ad Can Load Makes a Wall
Hearts refill through ads. Which means that **anywhere an ad cannot be shown, the refill button does nothing and the gate becomes a wall.**

We had two such places. The web build that runs straight in a browser has no ad bridge at all. And on Google Play, five of the seven games are built without the ads SDK, because the strategy puts ads on the Toss side and ships the Play builds ad-free.

So the gate only turns on **where a rewarded ad can actually be shown.** Everywhere else hearts are not counted and everything passes through.

## Trap Two — Three Outcomes, Read as Two
A rewarded ad ends in one of three ways. Watched to the end, dismissed by the user, or never shown at all.

**Dismissed and never-shown must not be treated the same.** Dismissing is the user's choice, so withholding the reward is right. But an empty inventory or a network error is our problem. Withholding there locks a feature for someone who did nothing wrong.

We got this backwards in the nursing exam app. The outcome is a string and the code treated it as an object, which produced the opposite failure: **the reward was granted while no ad ever played.** All three outcomes are now handled separately.

## Never Spend a Heart Without Consent
An action started by a button carries clear intent — a new run, an undo, a preview. Those spend immediately without asking.

In Minesweeper, though, stepping on a mine brings up the revive prompt on its own. The player did not ask for it.
Quietly deducting a heart there **spends it without consent.** Those cases ask first.

## Where It Is Now
One shared module, wired into seven games. Games with shorter runs got a more generous daily allowance.

| Game | Hearts per day |
|---|---:|
| Reaction Challenge | 5 |
| Memory Cards | 5 |
| Gomoku | 3 |
| Minesweeper | 3 |
| Number Rush | 3 |
| Number Slide | 3 |
| Solitaire | 3 |

Tarot Fortune kept its existing hearts; only the refill amount changed to match the rules above.

## What Is Still Open
Whether the numbers are right is an open question. Three hearts may feel stingy; seven would remove any reason to watch an ad. The plan is to run it for a few days and adjust.

Other notes from building these apps are collected in the [dev log](/archives/).

I post updates here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
