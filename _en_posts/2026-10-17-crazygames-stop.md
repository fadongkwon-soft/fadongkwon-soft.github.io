---
title: All Four Rejected by CrazyGames — I Am Stopping Here
description: I submitted Siege King on October 16 and Yut Nori, Janggi and the Reaction Challenge on the 17th, and all four were rejected within a day. The reason was the same single sentence for every one, "the overall quality of the game does not yet meet the expectations of our platform." Seeing the most polished landscape game fall with the same wording, I concluded this was not about genre or layout, and I am stopping CrazyGames submissions here. What remains and what I learned
image:
  path: /assets/img/20261017_crazygames-stop/cover.png
  alt: All four games rejected by CrazyGames, stopping here
date: 2026-10-17 19:20:00 +0900
categories: [Devlog, Platform]
permalink: /posts/crazygames-stop/
alt_url: /ko/posts/crazygames-stop/
tags: [minigame, solo developer, dev log]
---

Less than a day after posting [the retry story](/posts/crazygames-siege-king/), the results came in. **All four rejected.** This is the last post in the CrazyGames series.

## What I Submitted

After [the first three rejections](/posts/crazygames-rejection/) I switched to "one new game that feels new," and then submitted four games over two days.

- **October 16 — Siege King (Castle Topple).** A new landscape-only game that knocks castles down with a physics engine. Every screen size the portal reviews at is 16:9, and this one was built landscape from the start.
- **October 17 — Yut Nori and Janggi.** Two traditional Korean board games with no game of the same name on the portal.
- **October 17 — Reaction Challenge.** Seeing one-keyboard 1 to 4 player games near the top of the portal's multiplayer tab, I added keyboard input in a day so four people can compete on one keyboard. All eight modes, including the target and hold modes, work with a single key each.

That same evening I also fixed the three that were showing as a portrait phone column, giving them a 16:10 landscape layout on desktop and uploading new versions. Janggi puts the board on the left with turn, score and undo in a right panel, Yut Nori puts the board left with the sticks, result chips and throw button on the right, and the Reaction Challenge home became two columns. In the review iframe (907×510) the board grew from 294px to 380px wide.

## The Result

All four were rejected within a day of submission. The reason shown in the portal notifications was **identical for all four, to the letter.**

> The overall quality of the game does not yet meet the expectations of our platform.

It is the exact sentence two of the first three received. This time nobody got "too close to existing games." Yut Nori and Janggi really were genres the portal did not have, so that wall was cleared. Instead all four hit the quality wall.

## How I Read It

The most important fact in this round is that **Siege King got the same sentence.**

- It was a genre the portal did not have (physics siege puzzles exist, but this is not a clone).
- It was landscape-only from the start, so there was no layout problem.
- It is the game I spent the longest on, and the only one built on an external physics engine.

It still fell with the same generic wording as Yut Nori. So this is not a wall that more genre differentiation or more desktop layout work gets over. The "quality" the portal means sits above the level of what we call minigames: art, presentation, sound, the impression of the first thirty seconds. A level that works on Toss and Google Play does not meet the entry bar on the portal.

The rejection is one sentence, so there is no way to know what exactly was lacking. I decided that fixing by guesswork and resubmitting was something to do once, not twice.

## So I Am Stopping

CrazyGames submissions stop here. The other portal (GameDistribution) is shelved along with it. If a game comes along later that I can honestly call properly made, I will reconsider then. I will not upload more of the current catalog, and I will not patch existing games to try again.

## What Remains

Nothing is thrown away.

- **The one-keyboard 1 to 4 player Reaction Challenge.** On desktop, four people compete with the A, F, J and L keys. It is in the Play and Toss builds too, and on phones the key labels are hidden so nothing changes.
- **Desktop landscape layouts for Janggi, Yut Nori and the Reaction Challenge.** Open them on a wide screen and the board and panel sit side by side instead of a portrait column. Good for anyone opening them in a PC browser, portal or not.
- **The portal prep tooling.** One command that produces the build, footage, covers and videos from a single config line, the step that swaps the in-game title when a name is taken, and the procedure for uploading a new version. Next time there is no starting from scratch.

## What I Learned

- **The portal's quality bar is higher than the app stores', and the reason is one sentence.** It is a place to bring one game you are confident will pass, not a place to bring a catalog and see what happens.
- **The desktop landscape layout should have been done before uploading.** Submitting the first three as portrait phone columns was my mistake, and the fix landed only after they were already in the review queue. That said, Siege King was landscape from the start and still fell, so the fix alone would not have changed the outcome.
- **Rejections were cheaper than I feared.** Seven rejections, no penalty on the account, and the four submissions took two days. I do not regret trying.

That is the end of this series. Next, back to Toss and Google Play.
