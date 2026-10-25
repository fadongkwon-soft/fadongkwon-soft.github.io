---
title: Re-Measuring All 100 Box Push Levels with a Solver, and Why I Decided Not to Build Level 101
description: I re-ran all 100 levels through a solver to check that later levels really are harder. The rank correlation between level number and minimum pushes, box count and search nodes came out at 0.95 to 0.98, so "it gets harder" passed, but three weak spots showed up, a flat tutorial stretch, saturation at the search cap in the final levels, and trap-free levels pushed too far back. Here is how I corrected the ordering, why the 101 to 200 expansion is on hold (one to three returning users a day), and the daily puzzle I added instead
image:
  path: /assets/img/20261026_box-push-difficulty/cover.png
  alt: Solver-based difficulty check of 100 Box Push levels
date: 2026-10-26 01:43:00 +0900
categories: [Devlog, Game]
permalink: /posts/box-push-difficulty/
alt_url: /ko/posts/box-push-difficulty/
tags: [puzzle, solo developer, dev log]
---

[Box Push](/posts/box-push/) is a 100-level Sokoban. After release two questions came in, "does it really get harder as you go" and "please add levels from 101 on," and on October 21 I decided to answer both with numbers. This post is that measurement and the decision.

## Re-measuring all 100

The levels were generated with a fixed seed and arranged by the generator's own difficulty score. This time I pushed all 100 back through the solver and measured three things: minimum pushes (the A\* shortest solution), the number of boxes, and the number of nodes BFS expanded before finding a solution. Node count is the closest proxy for "room to get lost."

Rank correlation between level number and each metric:

| Metric | Rank correlation with level number |
| --- | ---: |
| Minimum pushes | 0.98 |
| Box count | 0.95 |
| BFS nodes expanded | 0.95 |

"It gets harder" passes. Three weak spots showed, though.

1. **Levels 1 to 5 are flat.** Intended as a tutorial, but numerically indistinguishable.
2. **Eleven of levels 81 to 100 share the same value.** I had capped BFS at 40,000 nodes and the late levels saturated at the cap. Levels at the cap cannot be ordered against each other.
3. **Trap-free levels were pushed back.** Some levels have A\* node counts equal to their push count, meaning you just follow the shortest path, yet BFS expanded a lot. Many boxes and a long route produce many nodes without anywhere to actually get lost. There were 9, 7 and 3 of these across three stretches.

## Correcting the order

Which 100 levels to include stays on the original difficulty score; **only the order of levels 16 to 100** was redone. The ordering score is the node count re-measured with the BFS cap raised to 200,000, plus the log of A\* nodes divided by pushes. That second term is "the amount of trap." It grows when there are many places to go besides the shortest path and sits near zero for trap-free levels.

At first I sorted each stretch separately, which created reversals at the stretch boundaries, so I switched to re-sorting the whole range at once. In simulation the rank correlation with pushes dipped only slightly, from 0.981 to 0.975, and 58 levels moved, by at most ten positions.

Saved progress is keyed by level number, so for levels that moved, existing users' star records attach to a different level. The next section is why I accepted that.

## Why I did not build level 101

Daily users on the Toss side are 22 to 52, almost all new. Returning users are one to three a day, 95 percent of arrivals come through the benefits-tab mission card, and 59 percent are aged 60 or over. Nobody is getting anywhere near level 100. They are not leaving for lack of levels; they are simply not coming back.

So the 101 to 200 expansion is on hold, with a defined condition for reopening it: **when level-clear events start showing level 90 or above.** The obstacle when expanding will be hints. The hint solver is capped at 80,000 nodes and 2.5 seconds, and the starting state of level 93 already takes 0.2 seconds on a PC, so one to two seconds on a phone. Harder levels may not produce a hint in time.

## What went in instead: the daily puzzle

Instead of more levels, I added a reason to come back tomorrow. The home screen has a daily puzzle card, picking one level a day from a pool of levels 16 to 60 on a 45-day permutation cycle. The same level does not repeat within 45 days and everyone gets the same one. Only the first clear of the day is recorded, for a streak count, and per-level bests and resume are left alone. Locked levels do not unlock through the daily puzzle. The pattern came straight from Lights Off and Sudoku, which already had it.

## Summary

- The 100-level difficulty curve does rise numerically, with rank correlations of 0.95 to 0.98.
- To correct three weak spots (flat tutorial, search-cap saturation, trap-free levels), I re-sorted levels 16 to 100 as a whole. 58 levels moved by up to ten positions.
- Levels 101 to 200 are on hold because returning users number one to three a day; the restart condition is observing clears at level 90 or above.
- A daily puzzle went in instead. The bottleneck is return visits, not level count.

The apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> User counts and ratios are from the Apps in Toss console dashboard on October 21, 2026. Solver metrics are the generator's measurements and may differ from perceived difficulty.
{: .prompt-info }
