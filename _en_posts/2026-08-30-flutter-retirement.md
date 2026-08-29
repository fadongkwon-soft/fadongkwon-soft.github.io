---
title: Retiring Flutter — What I Learned Rewriting Three Apps for the Web
description: Why Flutter web kept fighting me inside mini-app platforms, and what I kept and dropped while rewriting a spinner game, a bottle game, and a fortune-lotto app in plain TypeScript
date: 2026-08-30 20:00:00 +0900
categories: [Blogging, Episode]
tags: [flutter, mini apps, web apps, refactoring, solo developer, devlog, TypeScript]
permalink: /en/posts/flutter-retirement/
alt_url: /posts/flutter-retirement/
---

Today I moved my `flutter_project` folder into an archive. For almost two years it
was where my apps started their lives; as of today, not a single live app of mine
runs on Flutter. Juice Spinner, Spin the Bottle, and Saju Lotto have all been
rewritten in plain web tech (TypeScript + Vite), and the rewrites are submitted as
updates on both Google Play and the Korean mini-app platform I ship to.

This is not a "Flutter is bad" post. For native apps, Flutter remains excellent.
It's a record of how **Flutter web builds running inside webview mini-app
platforms** cost me more in maintenance than they returned — at solo-developer
scale, at least.

## Why retire it — the incidents that piled up

Looking back, the warnings were regular, and I had written up each one as it happened.

**A 20-second white screen, and an automatic rejection.** Flutter web needs to
download the CanvasKit renderer (several MB) before it paints anything. By default
it comes from Google's CDN, and when that CDN was slow in the mini-app review
environment, the blank screen exceeded 20 seconds and the review bot rejected the
app. Bundling CanvasKit fixed the rejection — but each app now weighed tens of
megabytes.

**Full-screen ads that killed the canvas.** Coming back from a native interstitial
sometimes left Flutter web's render surface (a WebGL context) dead: touches and
sounds worked, but nothing drew. The only dependable cure was to stash the user's
pending intent and reload the whole app after every rewarded ad.

**A storm of 404s for fonts I had already bundled.** The app shipped with a Korean
font, yet the engine kept trying to download hundreds of Noto Sans KR subsets. Two
separate mechanisms conspired, and understanding how an empty font family in a
theme-level TextStyle reaches the engine cost me a full day.

**The dart2js integer trap.** On the web target, integer seeds beyond 2^53 get
silently truncated — so numbers that should change weekly came out frozen. The
kind of bug that can never happen on native, only on web.

Each incident got fixed. But the pattern was clear: **almost none of the problems
were in the game logic — they were in the glue that bolts Flutter onto the web.**
And these apps are, at heart, a few select boxes and one canvas.

## The rewrite — one monorepo, three games

My newer games were already plain web apps in a pnpm monorepo, with shared packages
for storage, ad abstraction, and cross-promotion. Moving the three remaining
Flutter apps into the same frame was the obvious next step.

**Juice Spinner / Spin the Bottle** — half-day ports. I carried over the canvas
wheel-drawing code, the "4.5 turns plus random" spin formula, and the
winner-angle math verbatim from the Flutter sources, and let a CSS transition do
the rotation. The APK went from **around 40MB to 5.8MB**. Feature-for-feature
identical.

**Saju Lotto** — the final gate, and the one I was most careful with. The app's
entire reason to exist is determinism: the same birth data must always produce the
same numbers for the same period. So the rewrite had to be **bit-for-bit
identical** to the original. What had to move:

- A 19-digit integer seed (birth date, gender, and period encoded by digit
  position) — JavaScript numbers are 53-bit too, so `BigInt` was mandatory.
  The exact trap dart2js had set for me once before.
- A SHA-256-based RNG — Web Crypto is async, which is wrong for a simulation
  that calls it tens of thousands of times, so I ported a standard synchronous
  implementation.
- A solar-to-lunar calendar converter — two 225-entry lookup tables carried over
  verbatim from the original Dart package.

Verification was done with golden vectors: I had the original Dart code print
outputs for representative cases (solar/lunar birthdays, the pension-lottery game
type, the hourly-period quirk), then diffed the TypeScript port against them.
Not one line of UI was written until the diff came back empty.

**Existing users keep their data.** Flutter web's shared_preferences lives in
localStorage under a `flutter.` prefix, and a mini-app keeps its origin across
updates. So on first run the new app reads those keys and migrates saved profiles,
presets, and numbers in place. From the user's perspective the app just got
lighter; nothing disappeared.

## What got better for free

On the web, the workarounds simply evaporated. The ad-recovery reload hack is
deleted (the DOM survives an interstitial just fine), and the full-history win
simulation now replays **~1,200 draws in 0.3 seconds** on a synchronous JS SHA-256.
I even added a new feature the same day: "if you had bought five games with your
saju last week, what would you have won?" — possible only because a deterministic
generator can *re-create* last week's numbers on demand.

The winning-numbers data ships as a bundled CSV, but the same CSV also lives on
this blog (GitHub Pages), where a **GitHub Actions job appends new draws every
Sunday morning**. The app fetches that remote CSV in the background and merges it
into its cache — always current, no redeploy needed.

## Wrapping up — the archive

The last day's work was unglamorous: move the shared signing keystore to a stable
home and re-point the build config (then prove it with the signing-validation
task), move `flutter_project` into `_archive/`, delete the obsolete build scripts,
and leave a README in the archive explaining why it exists. Nothing was deleted —
the original code remains the oracle for determinism checks.

If I compress the lesson into one line: **use a framework where it is a
first-class citizen.** Flutter is first-class in native apps; inside a webview
mini-app, the first-class citizen is the web itself. Time leaking through the glue
layer isn't feature work — it's pure maintenance, and for a solo developer that
maintenance is the opportunity cost of the next app.
