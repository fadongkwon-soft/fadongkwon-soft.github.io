---
title: Back to CrazyGames — After Three Rejections, One New Game Submitted as "Siege King"
description: On October 10 all three games I submitted to CrazyGames were rejected the same day, for "too close to existing games" and "quality not yet meeting expectations." Instead of uploading more of the catalog, I decided to go back with a single new game that feels new, and picked the physics-based Castle Topple. Then the portal told me the name "Castle Topple" was already taken, so I submitted it under its Toss English name, Siege King. It is awaiting review now, and the result will be a follow-up post
image:
  path: /assets/img/20261017_crazygames-siege-king/cover.png
  alt: Back to CrazyGames — one new game submitted as Siege King after three rejections
date: 2026-10-17 01:45:00 +0900
categories: [Devlog, Platform]
permalink: /posts/crazygames-siege-king/
alt_url: /ko/posts/crazygames-siege-king/
tags: [minigame, solo developer, dev log]
---

On October 10 I submitted three minigames to the web game portal CrazyGames: Sky Jump, Brick Breaker and Gomoku. **All three were rejected the same day.** This post is about what I changed over the following six days and how I went back.

## Reading the Rejection Reasons Again

There were two kinds of rejection mail.

- **Gomoku:** "The concept is quite close to existing titles. We are prioritizing more differentiated experiences."
- **Brick Breaker and Sky Jump:** "The overall quality does not yet meet the expectations."

At first I tried to fix the second one. I assumed I just had to find what was lacking and polish it. Put side by side, though, both reasons said the same thing. The portal already has hundreds of gomoku, brick breaker and jump games. **A reviewer has no reason to add one more well-made copy.** It was not something a bug fix or a nicer screen would solve.

## Changing the Plan: One Game Instead of a Batch

The original plan was to upload **the remaining 31 games in one go** after the first three passed, and see what happened. Descriptions, controls, categories and tags were already drafted for every one of them.

I dropped that plan. Most of the 31 are also classic genres moved to the web, like Minesweeper, Sudoku, 2048 and Solitaire, so they would likely fall for the same reason. I put the other portal (GameDistribution) on hold as well.

The new rule has one line. **Submit a single new game that feels new.** Whether that one passes decides whether this channel is usable at all.

## Why Castle Topple

The candidate was [Castle Topple](/posts/castle-topple/), a physics puzzle where you pull back a cannon and knock castles down. Three reasons.

- **It collapses differently every time.** Blocks tilt, crack and slide under real physics, so the same level never produces the same scene twice. Browsing the portal's top games, that "I have not seen this before" feeling mostly came from exactly this.
- **It is landscape only.** Most portal players are on PC, and every screen size the reviewers use is 16:9. A portrait phone game uploaded as is shows up as a narrow column in the middle of the screen. This game is landscape from the start, so that problem does not exist.
- **It is the only game in our catalog built on an external physics engine.** There is little chance of it being lumped together with the other minigames.

## On the Portal, "Castle Topple" Already Belonged to Someone

I got stuck on the very first screen. I typed the game name and tried to move on to the preview, and the portal said **"The game name is already in use."**

Searching the public catalog turned up no game called Castle Topple, so most likely another developer has it registered privately. Portal rules say the registered name must match the title shown inside the game, so I could not simply change the portal-side name alone.

So I borrowed the English name we already use on Toss: **Siege King**. The game had been live there as "파괴왕 공성전 / Siege King," so nothing new had to be invented. The Google Play English name stays Castle Topple, and only the portal build swaps the in-game English title and the cover and video titles to Siege King.

## Landscape Meant Retooling the Prep Pipeline

A portal submission is one game file plus three cover images (landscape, portrait, square) and two preview videos (landscape, portrait). Until now I had only uploaded portrait phone games, so filming and video assembly were all built for portrait.

To fit a landscape game I changed three things. The capture window is rotated to landscape, the landscape video is used as is while the portrait video centers the wide frame with a blurred background above and below, and a step that swaps the in-game title for the portal-only name is now part of the build. Now one line for the name and a landscape flag in the config file, and a single command produces the build, footage, covers and videos.

## Submitted — Status: AWAITING REVIEW

I submitted Siege King on the evening of October 16. Category Puzzle, mobile orientation landscape only, saving in on-device storage. The first stage (Basic Launch) forbids ads, so it went up without them, and all seven self-check items passed. The status is **AWAITING REVIEW**.

Last time the three rejection mails arrived the same day. This time a full day has passed with no mail. That could be a good sign or just a slower queue, so I am not drawing any conclusion yet.

## The Next Post Is the Verdict

When the result comes in I will post it as is. If it passes, the next story is attaching the portal SDK for the full launch. If it is rejected, I will post the reason verbatim and decide again whether to keep going down this road.

One more thing. The day after Siege King, Yut Nori, Janggi and the Reaction Challenge, where four players share one keyboard, followed it onto the portal. That story goes with the results, in a separate post.
