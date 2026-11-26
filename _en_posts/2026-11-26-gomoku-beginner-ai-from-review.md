---
title: "\"The AI Is Too Good, I Keep Losing\" — Turning One 4-Star Review Into a Beginner Gomoku Mode"
description: "A single 4-star Toss review collected by our midnight automation prompted us to add a new 'Beginner' tier below Easy in Gomoku—and taught us why simply lowering block probabilities isn't enough when your scoring function still spots 4-in-a-rows."
image:
  path: /assets/img/20261126_gomoku-beginner-ai-from-review/cover.png
  alt: "Gomoku Beginner AI difficulty update"
date: 2026-11-26 01:32:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/gomoku-beginner-ai-from-review/
permalink: /posts/gomoku-beginner-ai-from-review/
tags: [board-game, gomoku, indiedev, devlog]
---

At 00:03, [our scheduled Toss review collector](/posts/midnight-automation-agents/) surfaced a short 4-star review on Gomoku:

> ★★★★☆ | Gomoku | 2026-11-20 | "Please lower the AI difficulty—it's too strong and I keep losing."

A month earlier we had actually *strengthened* Easy mode after players said it was too passive. Weakening Easy again would disappoint returning players, so we kept Easy, Normal, and Hard untouched and added a fourth tier underneath: **Beginner**.

## 1. Why Lowering Block Probability Alone Fails

Our Gomoku AI (`games/gomoku/src/logic.ts`) evaluates moves in priority order: win in one → block opponent's four → create an open four → block opponent's open three → pick from top-scoring positional moves.

Simply gating "block opponent's four" behind a 45% roll and skipping steps 3–4 looks right on paper, **until execution falls through to step 5**. Because the general shape evaluator assigns massive tactical weights (`300` to `100,000`) to open threes, open fours, and fives, step 5 immediately picks up the exact threat we just tried to ignore.

## 2. Separating Out `beginnerScore()`

To make Beginner genuinely approachable without playing completely random stones across the board, we wrote a dedicated `beginnerScore()` helper:

- Still completes an immediate five-in-a-row if available.
- Blocks an opponent's four only **45% of the time** (`BEGINNER_BLOCK_FIVE = 0.45`).
- Skips open-four attacks and open-three blocks completely.
- Scores candidate squares gently—capping line bonuses at 3-in-a-row with no tactical spikes—and picks randomly from the **top 10 candidates** (`BEGINNER_POOL = 10`).

The result feels natural (stones still cluster around active play) while letting newcomers build real attacks and win.

## 3. Tests and Localization

We updated `Difficulty` to `'beginner' | 'easy' | 'normal' | 'hard'`, expanded `games/gomoku/test/ai.test.mjs` with regression tests, and added 4-button difficulty selectors across all 9 supported languages. Designing an AI that loses *gracefully* turned out to be just as interesting as making one play well.
