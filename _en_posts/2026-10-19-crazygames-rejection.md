---
title: I Submitted Three Games to CrazyGames and All Three Were Rejected the Same Day — Plus How I Got Hooked on Ragdoll Archers
description: I submitted Sky Jump, Brick Breaker and Gomoku to the web game portal CrazyGames, and all three were rejected the same day. Gomoku was "quite close to existing titles," and the other two "do not yet meet quality expectations." This covers what I changed for the portal, how I read the rejection reasons, why I stopped the plan to upload 31 more, and what I realized after getting hooked on Ragdoll Archers while browsing the portal's top games
image:
  path: /assets/img/20261019_crazygames-rejection/cover.png
  alt: CrazyGames rejection, three games rejected the same day
date: 2026-10-19 09:00:00 +0900
categories: [Devlog, Platform]
permalink: /posts/crazygames-rejection/
alt_url: /ko/posts/crazygames-rejection/
tags: [minigame, solo developer, dev log]
---

So far my minigames have gone out on Toss and Google Play. But on Play, publishing alone does not bring people. An app nobody can find might as well not exist. So I chose **web game portals** as the next distribution channel, starting with CrazyGames.

On October 10 I submitted three games, and **all three were rejected the same day.**

## What I submitted

I picked three games with the most new users on Toss over the last 30 days and among the top Play installs:

- **Sky Jump** (arcade)
- **Brick Breaker** (arcade)
- **Gomoku** (board)

I changed quite a bit for the portal, too.

- **The portal version hides every outbound link** — other-app promos, app sharing, and the "show off" button on results. Portals do not allow sending players elsewhere.
- **Ads are off.** The first stage (Basic Launch) has no ads, so rewards that normally come from watching an ad are simply granted.
- **I added PC controls.** Many portal players are on PCs, so Brick Breaker got mouse and keyboard controls, and Gomoku's board now keeps its proportions on wide screens. These fixes also go into the next Play and Toss builds.

## The rejection reasons

All three were stopped at the pre-review, before the formal review.

- **Gomoku:** "The concept is quite close to existing titles; we're prioritizing more differentiated experiences."
- **Brick Breaker and Sky Jump:** "The overall quality does not yet meet the expectations."

At first I wondered what "quality" meant I should fix. But putting the two side by side, this was not about a bug or a single screen. **Portals already have hundreds of gomoku, brick breaker and jumping games.** I read it as: being reasonably well made is not a reason to add one more. This is not something fixing shared code can solve.

## Stopping the plan to upload 31 more

The plan was to follow these three by **uploading the remaining 31 games at once to see how they did**. I had already drafted descriptions, controls, categories and tags for each.

But most of those 31 are also ports of classic genres — Minesweeper, Sudoku, 2048, Solitaire and so on — and are likely to be rejected for the same reason. So I **put the second upload and submissions to another portal (GameDistribution) on hold**.

If I submit again, there is one condition: **a single new game that is differentiated from the start.** The current candidate is [Castle Topple](/posts/castle-topple/) (now called Siege King in Korean stores), built on a physics engine.

## And then, Ragdoll Archers

One embarrassing confession. To see what kind of games were on the portal, I browsed CrazyGames' popular games and opened **Ragdoll Archers**: two floppy, doll-like archers shooting arrows at each other. When an arrow hits, the body goes limp, holds on in some odd pose, and then collapses.

I meant to play a few rounds and ended up stuck on it for a long while. I went in to publish my games and came out hooked on someone else's.

Yet this did more than anything to help me understand the rejections. On paper Ragdoll Archers is simple: draw the bow and shoot, that is all. What keeps you from putting it down is **physics that falls apart differently every time**. The same arrow produces a different scene depending on where and how it lands. Most of the games near the top of the portal had something like that — **something that makes you think "I haven't seen this before" at a glance**.

My Gomoku is a well-made gomoku. But there is nothing new about it. Only then did I feel I understood what the rejection email meant by "more differentiated experiences."

## Summary

- Portals are not app stores. **A clean port of a classic genre does not get through pre-review on its own.**
- If the rejection is about genre and quality, **do not submit more of the same kind.** It is not a problem fixes can solve.
- Go back to the portal with **one game that feels new**.
- Getting hooked on someone else's game counts as research. Probably.

The portal changes (hidden outbound links, PC controls) are kept, not thrown away. The next game I submit can be built that way from the start.
