---
title: We Put a 1 KRW Promotion on the Toss Benefits Tab — 26 Mini Apps, 3,000 KRW Each
description: Our 26 mini apps now sit in the 'do a mission, get points' slot of the Toss benefits tab, paying 1 KRW the moment a mission is done. On day one, 15 people opened the word game from the card and only one was paid; the name-lotto promotion was rejected within four seconds because of the word 'draw'. Payout periods, mission length, the order of ads and payouts, and the console fields you cannot change later — what we learned starting out
date: 2026-10-03 12:25:00 +0900
categories: [Devlog, Platform]
permalink: /posts/toss-one-won-promotion/
alt_url: /ko/posts/toss-one-won-promotion/
tags: [apps in toss, toss, promotion, marketing, mini app, solo developer, dev log]
---

## Info
> On 1 October 2026 we started paying 1 KRW in Toss points to people who open one of our mini apps from the Toss benefits tab and complete a short mission. It began with five apps and grew to 26 by 3 October, each with a 3,000 KRW budget. The payout period matches how often the app has something new, the mission is kept short, and no ad ever stands between the mission and the payout. Here is what the first days showed and what the console will not let you change later.
{: .prompt-info }

## What We Started
The **Benefits** tab at the bottom of the Toss app has a section of cards that pay points for using mini apps. Apply through the promotion menu of the Apps in Toss console and your app gets a card there too. According to the console, about 160,000 people see that section every day.

When someone taps the card, opens our app and finishes the mission we set, they get **1 KRW in Toss points** on the spot.

- **1 October, noon**: we started with five apps — Saju Lotto, Lights Out, the word game, Breakout and Tarot Fortune.
- **3 October, 1 a.m.**: we widened it to 26 apps. Twenty-four are running; the two tarot apps are waiting on bundle review.
- **Budget**: 3,000 KRW per app, 78,000 KRW in total. One person can receive at most 1 KRW a day, so each app can bring in up to 3,000 visits.

The 1 KRW is less a reward than **a reason to open the app once.** Apps in Toss actively recommends promotions as the way for a new app to find its first users. If an app that nobody searches for yet can meet even a handful of first-time visitors a day from the benefits tab, 3,000 KRW did not seem expensive.

## Three Rules We Kept

### Payout period = how often there is something new
Games that offer a new round every day and the daily tarot pay **once a day**. Apps like Saju Lotto, whose numbers **stay the same for a week**, pay **once a week**. Paying people to come back every day to look at the same numbers buys nothing.

The console has a daily limit field but no weekly one, so the once-a-week limit lives in the app's code. It follows the cycle in which the numbers change, at midnight on Sunday.

### Keep the mission short
The first day's numbers settled this rule for us.

| App | Mission | Came in from the card | Got 1 KRW |
| --- | --- | ---: | ---: |
| Lights Out | Tap 5 cells | 10 | 11 |
| Breakout | Play one round | 19 | 15 |
| Saju Lotto | Enter saju and get numbers | 7 | 2 |
| Word game | Finish one round | 15 | 1 |

These cover 1 October from noon to 11:30 p.m. The two columns are counted differently, so they do not line up exactly (Lights Out even shows more payouts than entries).

The word game brought in **15 people and paid one.** The mission was "finish one round", so payment came only on the result screen, and few people played until they solved the word or ran out of tries. Lights Out asked for "tap 5 cells", and almost everyone who came in was paid.

So for every app we added afterwards we kept the mission **as short as possible.** Games with long rounds were cut down to a few moves: place 5 stones in Gomoku, slide tiles 10 times in 2048, tap 5 cells in Minesweeper, catch 5 moles in Whack-a-Mole, return the ball 5 times in Pixel Pong. Games whose rounds are short anyway — Tap Bird, Sky Jump, Tower Stack, Snake and the like — kept "play one round".

Breakout usually has three or four users a day. On the first day, 25 came in.

### No ad between the mission and the payout
The moment it looks like "watch an ad, get points", you run straight into ad policy. I have already [had an ad account suspended for invalid traffic](/posts/invalid-traffic-suspension/) once, and cannot afford it again.

So people who arrive from the card **see no ad at all until they have their 1 KRW.**

- Games skip the round-start ad and the ad notice for that round.
- Games that pop up a "watch an ad to continue" sheet the moment a round ends (Tower Stack, Sequence Memory, Whack-a-Mole) pay **before** that sheet appears.
- The lotto apps show **only the first combination without an ad** on the week's first draw and pay at that moment. The other combinations open with an ad as usual.

After the payout everything works as before. Ads shown after the 1 KRW has been paid have nothing to do with the mission.

## What We Wish We Had Known About the Console

### Many fields cannot be changed once set
Visibility, the **mission name**, the payout amount, the screen the card opens and the per-person daily limit are all fixed after registration. The **promotion name**, on the other hand, can be edited.

So the mission name stays generic, like "Play Solitaire", and the specific condition, like "move cards 5 times", goes into the promotion name. If the app changes and the condition changes with it, only the name needs editing.

### The budget can only go up
The first five apps got 10,000–20,000 KRW each. When we widened to 26 apps we wanted 3,000 KRW for every app, but **the budget cannot be lowered.** The edit screen lets you type a smaller number, then refuses to save it because it is "smaller than the existing budget".

The only way down is to **end the promotion and create a new one.** Ending returns the remaining budget to the business wallet. Budgets that had never been spent came back immediately; the rest arrived that evening. But a new promotion comes with **a new promotion code.** The code is built into the app bundle, so each bundle had to be uploaded and reviewed again. Around midnight on 2 October we recreated all five that way.

### "Draw" can be rejected as gambling
The Name Lotto promotion was registered as "draw this week's numbers from your name" and **rejected as gambling-like within four seconds.** On the same day the Star Sign and Car Plate lottos were approved with "draw numbers", so the judgement is inconsistent. Renaming it to "get your numbers" got it approved at once. For lotto-style apps, **"get"** is the safe word from the start.

### Start only after the new bundle is live
Once a promotion is approved, the console offers a start button — do not press it yet. Start the promotion only **after** the bundle that contains the promotion code is live. If the card goes on earlier, people land in the old bundle without the code, finish the mission and never receive their 1 KRW. This actually happened with Tarot Fortune, which went live on the old bundle; we paused it a little over an hour later.

The order is:

1. Register the promotion in the console. Most are approved automatically within seconds, and the code appears on approval.
2. Upload a bundle with the code, open it through a personal test link and complete the mission once. That turns on the console's "tested" flag.
3. Get the bundle reviewed and release it.
4. Only then start the promotion.

## The First Half Day
Of the 24 promotions switched on at 1 a.m. on 3 October, **21 apps paid out 151 times by around noon.** Reaction Speed paid 16 times, Gomoku 14, Breakout 13, Sequence Memory 12, and the number slide puzzle, Whack-a-Mole and Tower Stack 11 each. The shorter the game, the more people collect.

## What We Will Look At
On **10 October**, day seven, we check three things.

- **Ad revenue per 1 KRW** — how much the app's daily ad revenue rose after payouts began, divided by daily payouts. Below 1 KRW we stop; above 2 KRW we add budget.
- **Do people come back?** — from 22 October Apps in Toss picks recommended apps by return rate ([our notes on the exposure policy](/posts/apps-in-toss-exposure-policy/)). If many people take the 1 KRW and leave, the return rate could actually fall. We will look at visitors from the benefits tab separately.
- **Reviews** — a single review saying "I didn't get my points" sends us back to check the payout path.

Payouts are collected into our ledger every day and shown per app on the dashboard. That part is written up separately in [the revenue ledger update](/posts/revenue-ledger-update/).

## Try It Yourself
Look for the mini-app cards that pay points in the **Benefits** tab at the bottom of the Toss app. Ours are 26 apps, including Solitaire, 2048, Minesweeper, Gomoku, Sudoku, Reaction Speed and Saju Lotto. It is only 1 KRW a day, but play a round, and if you like it, come back.

News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
