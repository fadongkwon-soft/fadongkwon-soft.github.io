---
title: Two Bugs Hiding in the Instant a Screen Changes — A Speed Divided by Nothing and a Tap That Lingered
description: The real reason the brick-breaker ball crawled was that I measured a hidden element and got a height of 1px. In the slide puzzle, the same finger motion that placed the last tile also pressed the banner that had just appeared, skipping the completion screen entirely. Both bugs lived in the instant a screen changes, and in both cases my own defensive code hid the cause
date: 2026-09-18 20:00:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/screen-transition-traps/
alt_url: /posts/screen-transition-traps/
image:
  path: /assets/img/20260918_transition-traps/cover.png
  alt: Diagram of a screen transition with a mis-measured canvas and a leftover click event
tags: [javascript, canvas, pointer events, debugging, minigame, dev log]
---

I fixed two bugs in the same week that looked nothing alike, and then found they lived in the same place: **the single instant when a screen changes.**

One computed a value wrongly, the other received an event one beat too late. And in both cases, code I had written for safety was hiding the cause.

## 1. The ball crawls

I built a brick breaker, ran it on my phone, and the ball was visibly slow — unplayably slow. I raised the speed coefficient, suspected the frame timing, fixed and reinstalled a few times, and nothing changed. "Are you sure you actually fixed it?" was a fair question to get.

Speed is set like this:

```ts
/* Ball speed (px/s), based on screen height. Level 1 crosses the screen in ~1.5s */
function speedForLevel(lvl: number): number {
  return Math.min(H * 1.25, H * 0.62 * (1 + (lvl - 1) * 0.04));
}
```

`H` is the canvas height. Tying speed to height keeps the "crosses the screen in about a second and a half" feel regardless of device size. At 800px tall that is roughly 496 px/s.

### I stopped guessing and measured the speed

When three fixes in the same spot change nothing, the assumption is wrong. So I attached headless Chrome and recorded **how far the ball actually moved per frame**, by intercepting the canvas call that draws the circle and logging its coordinates.

The answer was unambiguous. `H` was **1**.

Which makes the speed `1 × 0.62 = 0.62 px/s`. Six tenths of a pixel per second. It was not crawling; it was effectively parked.

### Why it was 1

Here is the sizing code:

```ts
function resizeCanvas(): void {
  const r = wrap.getBoundingClientRect();
  W = Math.max(1, r.width);
  H = Math.max(1, r.height);
  ...
}
```

And the start path ran in this order:

```ts
resizeCanvas();      // ← game screen is still display:none
showScreen('game');
```

`getBoundingClientRect()` on a `display: none` element returns **all zeros**. So `r.height` was 0, and `Math.max(1, 0)` turned it into 1.

This is the heart of the bug. That `Math.max(1, ...)` exists to prevent division by zero. Had a real 0 gone through, the division would have produced `Infinity` or `NaN`, and the canvas would have drawn nothing or gone black — **and I would have found the cause in five minutes.** The guard converted a loud, obvious failure into a quiet wrong answer that merely looked like "a slightly sluggish game."

### The fix

Reverse the order:

```ts
showScreen('game');   // make it visible first
resizeCanvas();       // then measure
```

And recompute the speed at the moment the ball launches, when the screen is certainly visible:

```ts
function launchBall(): void {
  const speed = currentSpeed();   // recomputed here
  ...
}
```

## 2. The tap that placed the last tile also pressed the next screen

A request came in for the slide puzzle (the 15 puzzle): when the board is solved, do not jump straight to the results — show the completed picture, and go on only after one more tap.

I built it. On solve, the blank fills with the final tile to complete the picture, a "🎉 Solved! / Tap to continue" banner appears over it, and tapping the banner goes to the results.

The verdict after testing on a phone was: "It jumps to the results the moment it completes."

### One finger motion is three events

A single tap in a browser is not one event. It is:

```
pointerdown → pointerup → click
```

Three, in that order. And the code that moves the final tile finishes during `pointerup`. That is the moment the puzzle completes and the banner appears over the board.

But **`click` has not fired yet.** By the time it does, the banner occupies those coordinates, and the banner carries a "tap me to go to the results" listener. So one lift of the finger moved a tile, solved the puzzle, and pressed the banner. To the player, the completion screen never existed.

### A two-layer fix

```ts
let solvedAt = 0;
const SOLVED_TAP_GRACE_MS = 450;

function completeFromTap(): void {
  if (!awaitingTap) return;
  if (performance.now() - solvedAt < SOLVED_TAP_GRACE_MS) return; // ignore the motion that solved it
  awaitingTap = false;
  solvedBanner.hidden = true;
  void finishRun();
}

// click also arrives as a leftover from the solving tap, so only accept a fresh pointerdown
solvedBanner.addEventListener('pointerdown', completeFromTap);
```

First, the banner listens for **`pointerdown` only**, not `click`. The `pointerdown` of the solving motion happened before the banner existed, so any `pointerdown` reaching the banner is necessarily a new motion.

Second, for **450 ms after completion no tap is accepted at all.** Listening only for `pointerdown` already blocks this case, but event ordering and synthesis vary across devices and browsers, so the time grace is a second layer. A person needs longer than that to see the change and press again, so it costs nothing in feel.

Backing out with the back button goes straight to the results with no grace period, so that someone who solves the board and leaves does not lose the record.

### Where my verification went wrong

This bug came back *after* I had reported it fixed, which is the worse part.

For the first verification I loaded **a board saved one move from completion** and checked that the result screen appeared. On that path the banner behaves correctly. The actual failure only happens on the **path where you place a tile with your finger** — and I verified in a way that never went down that path.

The second time I did this: built a board with one move left, pressed the final tile with a real tap sequence (`pointerdown` → `pointerup` → `click`), reproduced the `click` landing on the banner, and confirmed the banner stayed. Then confirmed a second tap moved on to the results.

**A verification that does not traverse the path where the symptom occurs is not a verification.**

## What the two have in common

Different in character, identical in shape:

| | Brick breaker | Slide puzzle |
|---|---|---|
| When | Just before showing a screen | Just after a screen appeared |
| What | The moment of measuring size | The moment an event arrives |
| What hid it | The `Math.max(1, ...)` guard | Reaching for the familiar `click` |
| Symptom | A quiet wrong answer (slow ball) | A skipped animation |

Three things worth keeping:

**Make an element visible before measuring it.** Knowing that `getBoundingClientRect()` returns zeros for hidden elements does not stop you from violating it with statement order. When a screen transition and a size measurement live in the same function, check the order every time.

**Defensive code that makes failures quiet makes diagnosis hard.** Something like `Math.max(1, x)` prevents a crash but lets a wrong value through. During development, failing loudly is better. I am now pairing guards like this with a console warning when the input is implausible.

**Do not repeat a guess more than three times.** Three fixes in the same place with no change is a signal that the premise is wrong. The brick breaker took five minutes once I measured the speed directly. Before that, it took days.

Both games are on [Google Play and Apps in Toss](/en/posts/apps-in-toss-launch/), though not yet in the [play-in-your-browser](/en/play/) list. Updates go out here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
