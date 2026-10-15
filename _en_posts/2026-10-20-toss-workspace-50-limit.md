---
title: An Apps in Toss Workspace Holds Only 50 Mini Apps — Stuck at Number 51, Then Raised to 52
description: On October 10, creating Quick Go brought my Apps in Toss workspace to 50 mini apps, and the next one was blocked with "a workspace can have at most 50 mini apps." A second workspace had its settlement registration rejected as a duplicate business, and after contacting support the limit was raised to 52 as an exception, with no more beyond that. Here is where the two slots went, what to do until app deletion arrives, and how it lines up with the October 22 exposure policy
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

On October 10 I created [Quick Go](/posts/mini-go/), one of three new games, in the Toss console. When I went on to create Billiards and Mini Golf, this message appeared:

> A workspace can have at most 50 mini apps.

Quick Go was **number 50**.

## How I found out

The first block was actually something else. `billiards` for Billiards and `mini-golf` for Mini Golf are the names used in app addresses (appName), and **someone else on Toss was already using them.** So I tried again as `billiards-classic` and `mini-golf-game`, and that is when the 50-app message showed up.

The reason I did not know is simple: **nothing warns you about the limit.** The console does not show a count when you create an app, and nothing pops up at number 49. You find out the moment you try to create number 51.

And those 50 **include apps that have not launched yet.** An app takes a slot the moment it is created in the console. If you created apps early to reserve their names, those count too.

## What happened for lack of slots

Three games could not go to Toss right away:

- **Billiards** (8-ball and 9-ball)
- **Mini Golf**
- **[Castle Topple](/posts/castle-topple/)** — a cannon puzzle built on a physics engine

All three **went out on Google Play first** and launched on October 12. The Toss code and app wrappers were ready.

## Two things I tried

**1. A second workspace.** I first tried creating another workspace to hold new apps. But to receive ad revenue, each workspace needs its own settlement (business) information, and **registering settlement for a second workspace under the same business was rejected as "duplicate business information."** Putting apps in a workspace that cannot receive revenue made no sense, so I dropped that route.

**2. Asking for a higher limit.** Through the Apps in Toss support chat I asked three things: whether the limit could be raised to 100 or more, whether one business can run more than one workspace, and whether deleting a retired app frees its slot.

After some waiting, the answer came:

- **As an exception, the limit was raised to 52.**
- **An app deletion feature is planned.** For now there is no way to delete an app.

I explained my hub app plan and asked once more whether 60 was possible, but since this increase was already an exception, **a further increase was not possible**.

## Where the two slots went

The two new slots went to **Siege King** (Castle Topple's new Korean name) and **Mini Golf**, both launched on Toss on October 14. Billiards is still Play-only, and the five board games I made after that are on hold for Toss too.

This also changed how I build. For [Reaction Challenge](/posts/reaction-modes-retrospective/), instead of launching new apps, **I added eight modes to the existing app.** With no room for more apps, the direction became making each app deeper rather than adding apps.

## What matters more than the limit

Apart from hitting the limit, this coincided with a change in Toss's exposure policy. [From October 22, Toss exposure is split by app metrics, not app count](/posts/apps-in-toss-exposure-policy/). The September webinar named "apps mass-produced with only the theme changed" as subject to ongoing sanctions, and a cap on launches per workspace was mentioned as well.

Looking back, 50 is probably not an arbitrary number. Toss wants **one app grown well rather than many apps launched**, and the limit and the policy point the same way.

What remains is **hub apps** that bundle similar games: one per theme, such as fortune, puzzle, arcade, board games, quizzes and party games, with today's individual apps becoming modes inside them. With no free slots, the hubs will come **after app deletion arrives**, taking the places of low-activity apps that get cleaned up — starting with the lotto variants that differ only in theme.

## Summary

- An Apps in Toss workspace holds **up to 50 mini apps**. There is no advance warning; you are blocked when creating number 51.
- Unlaunched apps take a slot **from the moment they are created**, and right now **apps cannot be deleted.**
- A second workspace under the same business gets its **settlement registration rejected**.
- Support may raise the limit a little as an exception, but in my case **52 was the end**.
- If you are past 30 apps, **count your remaining slots now** — and before a new app, consider **adding modes to an existing one**. The exposure policy points the same way.

When app deletion arrives, I will write about which apps I cleaned up and which hubs took their place.
