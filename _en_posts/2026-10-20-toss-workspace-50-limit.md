---
title: An Apps in Toss Workspace Holds Only 50 Mini Apps — Getting Stuck at Number 51
description: On October 10, creating Quick Go brought my Apps in Toss workspace to 50 mini apps, and the next one was blocked with "a workspace can have at most 50 mini apps." Billiards, Mini Golf and Castle Topple went out on Google Play first, and a second workspace had its settlement registration rejected as a duplicate business. Here is when I should have known about the limit, and how it lines up with the October 22 exposure policy
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

All three **went out on Google Play first** and launched on October 12. The Toss code and app wrappers are ready, so they can go out as soon as a slot opens.

## Two things I tried

**1. Asking for a higher limit.** I asked through the Apps in Toss support chat whether the limit could be raised to 100 or more. As I write this, I am waiting for an answer.

**2. A second workspace.** I also tried creating another workspace to hold new apps. But to receive ad revenue, each workspace needs its own settlement (business) information, and **registering settlement for a second workspace under the same business was rejected.** Putting apps in a workspace that cannot receive revenue made no sense, so I dropped that route.

## What matters more than the limit

Apart from hitting the limit, this coincided with a change in Toss's exposure policy. [From October 22, Toss exposure is split by app metrics, not app count](/posts/apps-in-toss-exposure-policy/). The September webinar named "apps mass-produced with only the theme changed" as subject to ongoing sanctions, and a cap on launches per workspace was mentioned as well.

Looking back, 50 is probably not an arbitrary number. Toss wants **one app grown well rather than many apps launched**, and the limit and the policy point the same way.

So here is how I will use the remaining room:

- **Not for adding one more app at a time.** Even if the limit is raised, adding more of the same kind of app to a category only makes them pull down each other's rankings.
- **Hub apps that bundle similar games come first** — one per category, like puzzle, arcade and board, with individual games as modes inside.
- **Apps with weak metrics are candidates for cleanup**, starting with the lotto variants that differ only in theme.

## Summary

- An Apps in Toss workspace holds **up to 50 mini apps**. There is no advance warning; you are blocked when creating number 51.
- Unlaunched apps take a slot **from the moment they are created**.
- A second workspace under the same business may have its **settlement registration rejected**.
- If you are past 30 apps, **count your remaining slots now** — and keep an eye on the shift toward each app's metrics mattering more than the number of apps.

When a slot opens or the support team answers, I will write again along with the Toss launches of Billiards, Mini Golf and Castle Topple.
