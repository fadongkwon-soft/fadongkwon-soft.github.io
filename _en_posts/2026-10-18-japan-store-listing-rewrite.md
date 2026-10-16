---
title: Rewriting 45 Japanese Store Listings From Machine Translation to Real Japanese — Genre Words in Titles and Avoiding Trademarks
description: Our Google Play ja-JP listings were English run through a machine. I rewrote the title, short description and full description for 45 games using the genre words Japanese store users actually search for. The 30-character title formula, trademark-safe terms such as リバーシ instead of オセロ, keeping the in-app name and store title identical, why apps under review were skipped, and a rules typo the translation uncovered
image:
  path: /assets/img/20261018_japan-store-listing-rewrite/cover.png
  alt: Rewriting Japanese Play Store listings for 45 games
date: 2026-10-18 09:30:00 +0900
categories: [Devlog, Platform]
permalink: /posts/japan-store-listing-rewrite/
alt_url: /ko/posts/japan-store-listing-rewrite/
tags: [google play, aso, minigame, solo developer, dev log]
---

When I expanded the Play listings to 29 languages in September, the Japanese version was the English description carried over almost word for word. Not wrong, but not what Japanese users type into search. Japan has the highest revenue per casual game user of any market, and it was an asset I had registered and never touched.

On October 16 I rewrote the Japanese listings for 45 games. Here are the rules and the process.

## The title formula: game name plus a Japanese store genre word

Play titles are limited to 30 characters. I settled on one rule. **Put the Japanese name used inside the app first, then the genre word that top apps in the Japanese store actually use.** If the in-app title and the store title differ, users get confused and reviewers may flag it, so I pulled the Japanese names straight from each game's resources.

The genre words are not our translations but **the spellings top apps in each genre use**. For Sudoku, "ナンプレ" is searched more than "数独." Minesweeper is "マインスイーパー," Four in a Row is "四目並べ," Gomoku is "五目並べ," block puzzles are "ブロックパズル," and bubble shooters are "バブルシューター."

## Trademark-safe terms

Trademarks were the thing I watched most closely. Play prohibits another company's trademark in titles and descriptions, and our monorepo has a separate check tool that filters original game names. Japanese had a few catches.

- **オセロ** is a registered trademark, so we write **リバーシ**.
- **倉庫番** is a trademark too, so the box-pushing game is described as **箱押しパズル**.
- Janggi is a different game from Japanese shogi, so it is **韓国将棋(チャンギ)**. Write just 将棋 and people download expecting a different game.
- Yut Nori keeps the proper name with an explanation, **ユンノリ(韓国すごろく)**.

## What the descriptions stick to

- **Facts only.** No "広告なし" on an app that shows ads, and offline support and app size match reality. Back in September, when I turned ads on, I had to fix the "no ads" line in all 29 languages, so this time I was careful from the start.
- **Only features that exist in the game.** Modes and features were written from each game's Japanese resource file. Describing a mode that does not exist is simply a false description.
- The full description follows one structure: **the key points in the first three lines before the fold**, then a feature list, controls, and modes.
- No performance or price words such as "無料," "人気" or "No.1" in titles. Play's metadata policy prohibits them.

## A typo the translation uncovered

While rewriting the Pixel Pong description I noticed the Japanese version said "5点先取" (first to 5). The code, however, has the classic 1P and 2P modes at **first to 11, win by 2** from the very beginning; 5 points is the arcade-mode value only. The English listing and the other 28 languages correctly said "first to 11, win by 2," but the Japanese listing and **the in-app help text in all nine languages** were wrong.

I fixed the four spots in the Japanese description and corrected the in-app help in the source. Translation turned out to be not just carrying text across, but **a chance to check whether the original is right**.

## Apps under review are skipped

Changing a listing restarts the Play review. So I left alone any app whose binary review was in progress. Janggi had a new version under review, so its Japanese rewrite was postponed. The test is simple: **does the version shown on the public store page differ from the version of the last bundle we uploaded?** If so, it is under review.

## Confirming the rollout

I applied the changes to 45 apps through the API and all succeeded. Public pages only change after review, but the same evening the Japanese titles for Reversi and Lights Off had already updated. The rest will follow over a few days.

The effect will show up in store visits from Japan. Once October's numbers are in, I will compare them with September.

## Summary

- Titles are **the in-app name plus the spelling top apps in that genre use**. Not our own translation.
- Genre names such as オセロ and 倉庫番 can be trademarks. Filter them with a check tool.
- Descriptions stick to facts and in-app features. Translation is a chance to verify the original.
- Do not touch the listing of an app under review.
