---
title: Tap Bird Was Picked for the Apps in Toss Partner Growth Program — Two Days Turning a "One-Round Game" Into One Worth Coming Back To
description: On October 24, Apps in Toss emailed that Tap Bird had been selected for its partner growth program. From October 26, Toss itself runs a "browse a mini app for 10 seconds, earn points" promotion and then watches whether users return. A game with 50-second sessions and 9 percent weekly retention would let thousands of people wash straight through. Over the weekend I built an adventure mode (feathers, levels, 24 birds, 10 worlds, 100 stages), tuned difficulty with bot simulations, and caught a bug where hit points were a free pass
image:
  path: /assets/img/20261025_toss-growth-program-tap-bird/cover.png
  alt: Tap Bird selected for the Apps in Toss partner growth program
date: 2026-10-25 10:20:00 +0900
pin: true
categories: [Devlog, Platform]
permalink: /posts/toss-growth-program-tap-bird/
alt_url: /ko/posts/toss-growth-program-tap-bird/
tags: [apps in toss, toss, mini app, solo developer, dev log]
---

On Friday, October 24, an email arrived from Apps in Toss. [Tap Bird](/posts/tap-bird/) had been selected for the **partner growth program**. I had never applied for it, so I read the email twice.

## What the program is

Here is what the email said.

- Toss **itself** creates a "browse a mini app and earn points" promotion and starts it **automatically on Monday, October 26**. Unlike the [1-won promotions](/posts/toss-one-won-promotion/) I run, Toss pays for it.
- The condition is **10 seconds of browsing**. Enter the app, stay 10 seconds, points are paid, up to twice per person per 12 hours.
- The scale is thousands of visits a day until the budget runs out, **roughly a week**. With the two-per-person cap, that is 10,000–20,000 unique arrivals.
- We choose the screen the promotion lands on, in the console. The email asked for "a screen that shows what the app is right away."
- After the promotion ends, Toss looks at **whether users come back**.

That last item is the point. The [exposure policy in effect since October 22](/posts/apps-in-toss-exposure-policy/) picks recommended and boosted apps by retention and conversion. This program is Toss sending traffic and then measuring retention, a test of exactly that criterion. It landed in the same week that [All-tab traffic dried up and revenue started falling](/posts/toss-exposure-policy-revenue-drop/), so letting it pass was not an option.

Why Tap Bird, the email does not say. Among my 46 apps it is not near the top in users or revenue. I do not know the selection criteria and will not guess.

## Tap Bird today: 50-second sessions, 9 percent come back next week

I pulled the last month (September 24 to October 23) from the console dashboard.

| Item | Value |
| --- | --- |
| Daily users | 25–50 (40–65% of them from the 1-won promotion) |
| New-user share | Almost all new |
| Weekly retention | Week 1 8.7%, week 2 3.9% |
| Session length | 42–58 seconds |
| Age | Teens 43%, 60 and over 32% |

It is an arcade game you play once and leave. The high score is the only lasting motivation, and high scores only climb for teenagers. The odd split between teens and seniors is a trait of Benefits-tab traffic, and this promotion's arrivals will probably look similar. So the menu has to get simpler, and any progression I add has to be "a bonus you never have to tap."

**Left as is, 20,000 people browse for 10 seconds and leave.** The payout condition is "10 seconds," not "one round," so the default behaviour of an arrival is to look at the first screen for 10 seconds and go. The first screen has to create "maybe one tap" within those 10 seconds, and the end of the first round has to show "the next goal," or this traffic never becomes an asset.

The email came Friday evening and the program starts Monday, so zero business days. Toss review usually takes one to three days, so I gave up on swapping the bundle before launch and aimed for the late part of the promotion and **the second visit onward** to see the new version. Retention is made on the second visit anyway.

## Design: from "one round equals a score" to "one round equals feathers plus XP"

The reference was Ragdoll Archers on CrazyGames. Not the ragdoll combat, but three structures. **Something that remains when you die** (currency for permanent upgrades), **new gear unlocking at each level**, and **physics you feel in your body**. Translated into Tap Bird:

- **Feathers.** The existing coins, promoted. Every round earns feathers, and feathers buy permanent upgrades: hit points, invulnerability time, magnet, shield, starting boost. A failed round still leaves something behind.
- **XP and levels.** Levelling up opens new bird species. The results screen shows "N XP to the next bird."
- **24 birds.** From sparrow through hummingbird, pigeon, owl, penguin, duck, ostrich and thunderbird. They differ in hit points, jump and weight.
- **Hit points.** Hitting a pipe takes a hit point and bounces you instead of killing you outright. At zero you fall.
- **10 worlds, 100 stages.** From clear skies to a snowstorm mountain and a kingdom above the clouds. Clear 8 of a world's 10 stages and the next world opens.
- **Daily missions and cosmetics.** Colours, hats, trails.

One decision was unavoidable. Once progression exists, **the online leaderboard becomes unfair**. A score set with a 5-hit-point bird and one set with a sparrow cannot sit in the same list. So I split the game into two modes. **Classic** is sparrow only with the Toss Game Center leaderboard; **Adventure** has progression, stages and local records. Existing players' records carry on in Classic.

The first screen changed too. So that a promotion arrival recognises the game within 10 seconds, the home screen now has **one big "Start Adventure" button**, and tapping it starts the next stage immediately.

## Difficulty was tuned with bots

With 100 stages, you cannot play-test them all by hand. I separated the game rules so they can run without a screen, and ran an "average player" bot 150 rounds per stage to get clear rates. The bot uses the same rules file as the real game, so changing one changes the other.

| Bird | Average clear rate by world (W1 → W10) |
| --- | --- |
| Sparrow (2 HP) | 64 · 59 · 39 · 45 · 40 · 40 · 30 · 20 · 28 · **3%** |
| Pigeon (3 HP) | 82 · 80 · 60 · 70 · 59 · 61 · 44 · 45 · 44 · **15%** |

Each world's first stage starts at 95 percent for the sparrow and falls to 7 percent in the last world. The later worlds are endgame, assuming 3–4 HP birds and practice. The expert bot clears the same stretches at 85 percent or better.

## Two things testing caught

On a real device the feedback was **"a 3-HP bird clears everything."** That did not match the simulation.

**1. Hit points were a free pass.** On a head-on collision there was logic that moved the bird into the centre of the pipe gap, and that pipe was then **counted as passed**. With 3 HP you could hit three pipes in a row and still fill the goal. Hit points were not a cost; they were a free ticket. I changed it so a pipe you hit does not count toward score or goal. Same for a pipe you touch during invulnerability and a pipe blocked by a shield. One rule: **the only pipes that count are the ones your body never touched.** Hit points are "surviving one more time," not passing.

**2. The HP upgrade was exploitable.** The "Sturdy Body" upgrade bought with feathers was sold up to level 5, but its effect stopped at level 3. Levels 4 and 5 took feathers for zero effect, a bug, and in the other direction, maxing it to 3 let the pigeon clear the last stage of world 8 almost half the time. I capped the upgrade at **2 levels** and total hit points, bird plus upgrade, at **5**. After the fix, pigeon +2 clears that stage 10 percent of the time; the expert bot 69 percent.

Both would have ended as "feels easy, I guess" without the simulation. When the bot says the numbers are right and a human says it is easy, it is the rules that are wrong.

## Getting ready to measure retention

To answer "did this program create retention," arrivals from the promotion have to be counted separately.

- I appended `?from=growth` to the promotion's entry path in the console. The app reads it and logs an entry event. It differs from the 1-won promotion's `?from=promo`, so payout logic is unaffected.
- The comparison cohort is Benefits-tab arrivals from the 1-won promotion. The current baseline is **8.7 percent weekly retention**.
- Three things to watch: first-round start rate among promotion arrivals, second-round start rate after the first, and D+7 return rate.

## Where it stands

- The first cut of Adventure mode went live on Toss the night of October 24. The expanded version with 10 worlds, 100 stages and 24 birds is in review, and the same version has been submitted to Google Play.
- The promotion starts October 26.
- Ads appear only when you tap a button on the results screen (revive, double feathers), and the every-third-round ad is announced in advance under the button. The same pattern I learned from the [ad-notice rejection](/posts/toss-ad-notice-rejection/).

## Summary

- The Apps in Toss **partner growth program** has Toss pay for a "browse 10 seconds, earn points" promotion and then measure **retention**. I do not know why Tap Bird was picked.
- A game with 50-second sessions and 9 percent weekly retention would let the traffic wash through. So I added **Adventure mode** (feathers, levels, 24 birds, 10 worlds, 100 stages) and **split it from Classic** for leaderboard fairness.
- Difficulty was tuned with 150-round bot simulations, and device testing caught **hit points acting as a free pass** and **upgrade levels with no effect**.
- Retention is measured separately through the `?from=growth` cohort. The baseline is 8.7 percent.

When the promotion ends and D+7 has passed, I will report how many of the 20,000 came back.

My apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played in the browser](/play/). Updates come through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The selection criteria and scale of the growth program come from an individual notification email and may differ from the public Apps in Toss guide. Retention results will follow in a separate post after the promotion ends.
{: .prompt-info }
