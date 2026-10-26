---
title: Gomoku Was Picked for the Apps in Toss Growth Program Too — No Email, a Promotion Already Running, and a First Screen Rebuilt From Day-One Data
description: Right after Tap Bird, Gomoku turned out to be selected for the Apps in Toss partner growth program as well. Tap Bird got an email; Gomoku got nothing, and I only found out from the console the day after the promotion started. Day-one traffic was five times normal, but fewer than 1 percent of people who came from the Benefits tab returned the next day. So I turned the first screen from a settings form into a board you can play right away, and added a daily puzzle, streaks, and a Hard win-streak ranking
image:
  path: /assets/img/20261027_toss-growth-program-gomoku/cover.png
  alt: The growth program banner in the Apps in Toss console — Congratulations! Gomoku was selected for the growth program
date: 2026-10-27 01:12:00 +0900
pin: true
categories: [Devlog, Platform]
permalink: /posts/toss-growth-program-gomoku/
alt_url: /ko/posts/toss-growth-program-gomoku/
tags: [apps in toss, toss, mini app, gomoku, solo developer, dev log]
---

Two days after I wrote about [Tap Bird being picked for the growth program](/posts/toss-growth-program-tap-bird/), I learned that [Gomoku](/posts/gomoku/) had been selected for the same program. The banner above is the official notice that was sitting on Gomoku's page in the Apps in Toss console.

## No email arrived

Tap Bird got a "you've been selected for the growth program" email. Gomoku got nothing. I opened Gomoku's console page for something else the day after the promotion began, saw the banner, and only then found out.

The Apps in Toss announcement says that selected apps get a growth program menu in the console and are also notified by KakaoTalk message and email. I searched my inbox again and found nothing about Gomoku. Both apps' promotions were created at the same moment, so either one notice went out per workspace or the second one was simply dropped.

To see whether I had missed anything else, I checked **all 52 live apps** in the console. Only two were selected: Tap Bird and Gomoku. From now on I check each app in the console instead of trusting the inbox.

## Day-one data — five times the traffic, and almost all of it left

The promotion started at 11 a.m. on October 26. The terms match Tap Bird's: people arrive from the Toss Benefits tab through "browse for 10 seconds, earn 5 won," stay 10 seconds, and get their points.

| Metric | Value |
| --- | --- |
| Daily users (normal) | 82–133 |
| Daily users (Oct 26, day one) | 480, of which 430 from the Benefits tab |
| Next-day return, users from the All tab | 18% |
| Next-day return, users from the Benefits tab | 0.8% |

On a normal day, one in five people who find Gomoku in the All tab comes back the next day. Of the people who arrive through the Benefits tab, not even one in a hundred does. That is exactly the number the growth program watches to decide on further support: **do the people who came to browse come back?**

## The first screen was a settings form

I looked again at what Gomoku shows during those 10 seconds.

- Right under the title sat a card reading **"vs. computer: 0 wins, 0 losses, 0 draws."** For a first-time visitor that line carries no information.
- Below it were three tiles for mode, difficulty, and who moves first, and only then the Start button. **During a 10-second visit, the board never appeared.**
- The default difficulty was Normal, and Black played under renju forbidden-move rules (double three, double four, overline). A newcomer could easily get blocked in the first game without knowing why.
- There was no reason to come back. No daily challenge, no streak.

## What I changed

**1. A board you can play right away.** First-time visitors arriving through the promotion skip the home screen and land directly in an Easy game. Under the board, "Tap any spot to place your first stone" pulses gently. The regular home screen now leads with a board preview, and tapping the board starts a game. Settings and records are folded away, and records only appear once there is something to show.

**2. Easy first games.** New players now start on Easy, and Easy has no forbidden moves. Normal and Hard keep the renju rules.

**3. The daily puzzle.** A "win in 2 or 3 moves" puzzle that changes every day. From games the Gomoku AI played against itself, I kept only the 120 positions you can win within the move limit by forcing with fours in a row. Tests confirm that every puzzle really can be won in that many moves. From the second attempt on, a hint ring marks the first move, and solving every day builds a "🔥 N-day streak."

**4. From the result screen to tomorrow.** When a game ends, the result screen points to the daily puzzle. If you have already solved it, it tells you a new one arrives after midnight and offers a reminder for tomorrow.

**5. A Hard win-streak ranking.** To spark some competition I added a Toss ranking. My first idea was "win rate, after at least 10 games on Hard," but the code showed three holes:

- Leave a game you are about to lose and no loss is recorded. The win rate stays at 100 percent.
- The Toss ranking only takes your personal best. Go 10 for 10 on a lucky run, stop, and you are first forever.
- The top spots pile up in 100 percent ties.

So the ranking uses the **longest win streak on Hard** instead. A win adds one; a loss or resignation resets it to zero. Leaving mid-game counts as a loss, and even closing the app does: an unfinished game is recorded as a loss the next time you open it. Games where you used undo count as practice and do not extend the streak, even if you win. These rules are spelled out ahead of time all over the app: on the home screen, the game screen, the undo, leave, and resign confirmations, the result screen, and the records screen.

## What testing caught

Running it on a phone turned up a few fixes.

- **You could not see whose turn it was.** The "●" in the turn indicator is white text, so Black's turn looked like White's. It is now the same stone graphic as on the board.
- **The home preview looked like Go.** The lines were drawn on cell edges, so the stones sat inside squares. Gomoku stones go on intersections.
- **The ad notice appeared twice.** A notice attaches to every button that can trigger an ad, and adding the puzzle buttons put two on one screen. Now only one main button per screen gets it.
- **Ranking scores almost vanished silently.** Gomoku's Toss wrapper was missing the ranking API. Shipped as-is, every score submission would have failed without any error. The pre-release check caught it.

## Where things stand

- The new Gomoku entered Toss review early on October 27. The promotion is already running, so people arriving right now still see the old screen.
- Once approved, I will release it immediately and add `?from=growth` to the promotion's landing path so growth-program visitors are counted separately.
- The metrics are the same as for Tap Bird: first-game start rate, second-game start rate, and next-day and one-week return. The baseline is **0.8 percent next-day return from the Benefits tab**.

## Summary

- Gomoku was also selected for the Apps in Toss **partner growth program**. **No notification email arrived**, so I had to check each app in the console. Of 52 apps, two were selected: Tap Bird and Gomoku.
- Day one brought five times the usual users, but only 0.8 percent of Benefits-tab visitors came back the next day.
- The first screen went from a settings form to **a board you can play right away**, and the **daily puzzle**, **streaks**, and a **Hard win-streak ranking** give people a reason to return.
- The ranking uses **streaks** instead of win rate, to close the loopholes of leaving, resigning, and undoing to protect a record.

A week after the promotion ends, I will report how many people came back to Tap Bird and Gomoku.

My apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). News goes out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The notification behavior and promotion terms are described from what the Apps in Toss console and announcements show. Return results will follow in a separate post after the promotion ends.
{: .prompt-info }
