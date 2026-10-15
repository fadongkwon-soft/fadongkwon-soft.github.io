---
title: An Apps in Toss Workspace Holds Only 50 Mini Apps — Getting Stuck at Number 51
description: On October 10, creating Quick Go brought my Apps in Toss workspace to 50 mini apps, and the next one was blocked with "a workspace can have at most 50 mini apps." A second workspace under the same business had its settlement registration rejected, and there is currently no way to delete apps. Here is how I plan to release new games with 50 as the hard maximum, and how it lines up with the October 22 exposure policy
image:
  path: /assets/img/20261020_toss-workspace-50-limit/cover.png
  alt: Apps in Toss workspace limit of 50 mini apps
date: 2026-10-20 09:00:00 +0900
categories: [Devlog, Platform]
permalink: /posts/toss-workspace-50-limit/
alt_url: /ko/posts/toss-workspace-50-limit/
tags: [apps in toss, toss, mini app, solo developer, dev log]
---

Since my first mini app on Apps in Toss in August, I kept adding apps for two months: minigames, fortune apps, quizzes, lotto variants, and this month the five retro games and nine board games.

On October 10 I created [Quick Go](/posts/mini-go/), one of three new games, in the Toss console. When I went on to create the next new game, this message appeared:

> A workspace can have at most 50 mini apps.

Quick Go was **number 50**.

## How I found out

The first block was actually something else. The app address names (appName) I wanted for the next two games **were already taken by someone else on Toss.** So I tried again with different names, and that is when the 50-app message showed up.

The reason I did not know is simple: **nothing warns you about the limit.** The console does not show a count when you create an app, and nothing pops up at number 49. You find out the moment you try to create number 51.

And those 50 **include apps that have not launched yet.** An app takes a slot the moment it is created in the console. If you created apps early to reserve their names, those count too.

## There was no other way

**A second workspace.** I tried creating another workspace to hold new apps. But to receive ad revenue, each workspace needs its own settlement (business) information, and **registering settlement for a second workspace under the same business was rejected as "duplicate business information."** Putting apps in a workspace that cannot receive revenue made no sense, so I dropped that route.

**Deleting apps.** I wondered whether deleting a retired app would free a slot, but **there is currently no way to delete a mini app.** I was told a deletion feature is planned.

So **50 is the maximum.** Some of the new games I made in the meantime went out on Google Play first.

## From here on, it is swapping

With all 50 slots filled, the only way to put a new app on Toss is to **take down an existing app and put the new one in its place**. So I changed how I approach new games.

- **Modes before apps.** For [Reaction Challenge](/posts/reaction-modes-retrospective/), instead of launching new apps I added eight modes to the existing app — making an app deeper rather than adding apps.
- **Pair each new app with one to retire.** Before a new game goes to Toss, I pick the app with the weakest metrics to take down. The lotto variants that differ only in theme are first in line.
- **Hub apps.** Apps that bundle similar games, one per theme, such as fortune, puzzle, arcade, board games, quizzes and party games, with today's individual apps becoming modes inside them. Their slots will also come from cleaning up existing apps.

## What matters more than the limit

Apart from hitting the limit, this coincided with a change in Toss's exposure policy. [From October 22, Toss exposure is split by app metrics, not app count](/posts/apps-in-toss-exposure-policy/). The September webinar named "apps mass-produced with only the theme changed" as subject to ongoing sanctions, and a cap on launches per workspace was mentioned as well.

Looking back, 50 is probably not an arbitrary number. Toss wants **one app grown well rather than many apps launched**, and the limit and the policy point the same way. Swapping apps within 50 slots is, in the end, a way of following that direction.

## Summary

- An Apps in Toss workspace holds **up to 50 mini apps**. There is no advance warning; you are blocked when creating number 51.
- Unlaunched apps take a slot **from the moment they are created**, and right now **apps cannot be deleted.**
- A second workspace under the same business gets its **settlement registration rejected**.
- If you are past 30 apps, **count your remaining slots now**. Once full, a new app means **taking down an existing one** — and before that, consider **adding modes to an existing app**.

When app deletion arrives, I will write about which apps I took down and what went in their place.
