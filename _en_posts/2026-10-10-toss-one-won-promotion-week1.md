---
title: Toss 1-Won Promotion, Week One — 2,099 Won Spent, and Ad Revenue per Won Was All Over the Place
description: Day seven of my 1-won promotion on the Toss rewards tab. From October 1 to 8, 25 apps paid out 1 won 2,099 times. Extra ad revenue per won paid was about 10 overall, 4 without one outlier app, and a median of 2.3 per app. Nearly everyone was a first-time user, and no reviews complained about points
image:
  path: /assets/img/20261010_toss-one-won-promotion-week1/cover.png
  alt: Toss 1-won promotion week one, 2,099 won across 25 apps
date: 2026-10-10 09:00:00 +0900
categories: [Devlog, Platform]
permalink: /posts/toss-one-won-promotion-week1/
alt_url: /ko/posts/toss-one-won-promotion-week1/
tags: [apps in toss, promotion, mini app, solo developer, dev log]
---

A week ago I [put a 1-won promotion on the Toss rewards tab](/posts/toss-one-won-promotion/). At the end of that post I said I would check three things on day seven, October 10: **ad revenue per won paid, whether people come back, and reviews**. That day is today, so here are the numbers.

## How much went out

From October 1 to 8, **25 apps paid out 2,099 times** — in other words, **2,099 won**. That is about 3% of the 75,000 won budget (3,000 won per app).

| Date | Payouts |
| --- | ---: |
| Oct 1 (5 apps, from noon) | 29 |
| Oct 2 (recreated) | 0 |
| Oct 3 | 398 |
| Oct 4 | 441 |
| Oct 5 | 445 |
| Oct 6 | 290 |
| Oct 7 | 247 |
| Oct 8 | 249 |

October 2 is zero because, as described in [the previous post](/posts/toss-one-won-promotion/), I ended every promotion and recreated it to lower the budgets.

The striking part is that **daily payouts fell by almost half from October 6**. Not one app — all 25 dropped together. I changed nothing on the app side, so either fewer people visited the rewards tab itself or the order of cards inside the tab changed. The console doesn't show which.

Short games collected the most: **Gomoku 252, Mole Tap 186, Breakout 154, Memory Cards 133**. The lotto apps got few — Car Number Lotto 4, Saju Lotto 13, Name Lotto 19. Their numbers stay the same all week, so they pay out **once a week** by design; the low count is expected.

## Ad revenue per won

The rule from the last post: if an app's ad revenue rises by **less than 1 won per won paid, stop; more than 2 won, raise the budget.**

I kept the calculation simple. I compared each app's **average daily Toss ad revenue** for the seven days before the promotion (September 24–30) with the promotion period (October 3–8), and divided the increase by the payouts over the same period. The four lotto apps and the word game only started showing ads on October 1, so I couldn't separate the promotion's effect from the ads' and left them out. That leaves 20 apps.

| Basis | Extra ad revenue per won paid |
| --- | ---: |
| 20 apps combined | about 10.7 won |
| 19 apps, without Reaction Challenge | about 4.0 won |
| Median of per-app values (25 apps) | about 2.3 won |

The combined figure looks great, but **a single app, Reaction Challenge, pulled it way up**. Its daily ad impressions rose about fifteenfold. Without it the figure drops to 4 won, and the median of the per-app values is 2.3 won. 13 of 25 apps cleared 2 won; 8 fell short of 1 won (a few actually went down).

Some caveats for reading these numbers:

- **The ad revenue isn't only from promotion users.** It is the app's revenue from everyone. If users came or went for other reasons over the same days, that is mixed in.
- **The ad flow changed in the same period too.** In late September I reworked ads in several apps, adding a notice line before ads among other things. I tried comparing against apps that weren't in the promotion, but they had their own changes over the same days, so they couldn't serve as a baseline.
- **The window is only six days.**

So I can't say "pay 1 won, get 10 back". What I can say is that **the apps generally cleared the 2-won line**. With only 3% of the budget spent, raising it can wait until the budget starts running low.

## Do people come back?

I couldn't measure this properly yet. The console's promotion stats split people who arrived through the promotion into **new and existing users**. For Gomoku, the biggest payer, October 3–8 showed **228 new and 16 existing**. Nearly everyone coming through the rewards tab is **a first-time visitor** — which is exactly why I started the promotion.

What I couldn't isolate is whether those people come back the day after getting their 1 won. Apps in Toss picks recommended apps by return rate from October 22, so next I'll look at how each app's overall return rate moves before and after the promotion.

## Reviews

Three reviews have come in since October 1 (one for Reaction Challenge, two for Gomoku), and **not one says the points never arrived**. The payout path seems to be working.

## What I'll watch next

- **Whether the lower daily payouts continue.** If fewer people are visiting the rewards tab, there is nothing to do on the app side, but I can see whether the card text or the mission makes a difference.
- **The 8 apps under 1 won.** By the rule they are candidates to stop. Many of them are low-payout lotto apps, so I'll decide with another week of data.
- **The 14 new games.** The 9 board games and 5 retro games have promotions registered too, and they start once the games launch.

I collect the revenue numbers daily in my [revenue ledger](/posts/revenue-ledger-update/). My apps are on [Games](/games/) and [Apps](/apps/). If you spot one of my app cards on the **rewards** tab at the bottom of the Toss app, give it a round.

> The ad revenue comparison in this post is a simple before-and-after of each app's total revenue, not the promotion's effect in isolation. Read it as a pointer to the direction, nothing more.
{: .prompt-info }
