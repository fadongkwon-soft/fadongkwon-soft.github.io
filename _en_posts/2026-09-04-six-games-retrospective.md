---
title: Shipping Six Mini Games at Once — A Five-Day Retrospective
description: Sudoku, Nonogram, All Lights Off, Hangul Word Guess, Tap Bird and Number Rush went live on Google Play and Apps in Toss within five days. Why one shared spec, the one-pass registration order, and the mistakes I actually made
date: 2026-09-04 23:50:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/six-games-retrospective/
alt_url: /posts/six-games-retrospective/
image:
  path: /assets/img/20260904_six-games/cover.png
  alt: Six game icons
tags: [minigame, apps in toss, solo developer, dev log, typescript]
---

Today I published six launch posts at once: [Sudoku](/en/posts/sudoku/), [Nonogram](/en/posts/nonogram/), [All Lights Off](/en/posts/lights-off/), [Hangul Word Guess](/en/posts/hangul-word/), [Tap Bird](/en/posts/tap-bird/) and [Number Rush](/en/posts/number-tap/).
The first line of code was written on the night of August 30; Apps in Toss went live on September 3 and Google Play on September 4. **Six games in five days**, on two stores.
Last month, in [What I Learned Building 8 Apps Alone](/en/posts/solo-dev-8-apps/), I wrote that the next round would be "a batch." This is the record of actually running that batch.

## Why six at once

Of the time it takes to ship one game, **writing the game logic is less than half.** Store listings, screenshots, icons, content-rating questionnaires, privacy declarations, ad placements, push-consent forms, the cross-promo registry, the blog post and the Instagram card — the other half is repetitive work that has nothing to do with the game.

Repetitive work is nearly free once the procedure is fixed. So this time the goal was to **bind six games to one shared spec and run the release procedure six times in a row, so the procedure itself hardens.** The errors I hit registering the first app were down to zero by the sixth.

## The shared spec — what all six games have in common

The games differ, but the skeleton is one.

- **Daily seed + streaks**: a seed derived from the date produces "today's puzzle," and solving it extends your streak. Without a server, every player in the world gets the same board.
- **Guaranteed unique solutions**: the three puzzle games (Sudoku, Nonogram, All Lights Off) only serve boards with exactly one answer. For Sudoku I solved all 100 generated boards to confirm uniqueness; for Lights Off I checked that the GF(2) linear-algebra solver agrees with brute force; for Nonogram I verified that line logic alone completes every board — all as automated Node tests. A board that "has to be guessed" is the fastest way to lose stars in a puzzle game, so this is where most of the time went.
- **Nine languages**: Korean, English, Japanese, Chinese, Spanish, Portuguese, German, French, Italian. Device language is detected; anything else falls back to English.
- **Ad hooks**: rewarded ads for hints and revives, an interstitial every three rounds. The first Play build shipped without ads, though (see below).
- **Shared UI packages**: screen transitions, storage, seeded RNG, the cross-promo list and the share button all live in the monorepo's shared packages. The genuinely game-specific code is 300–700 lines per title.

## The release procedure — hardened by six repetitions

### Google Play first, then Apps in Toss

Listing a game in the Apps in Toss game category requires a game rating. Going through the Korean rating board directly costs money and 10–15 days per title, but **if you release on Google Play as a game first, IARC issues a self-classified rating for free and automatically**, and its certificate ID is accepted by Apps in Toss as-is. I registered the six on Play on the morning of August 31 and had six IARC IDs the same day.

### The one-pass registration order

Registering a new Play app in the wrong order means meeting the errors one at a time on the review page. The order that six runs settled on:

1. Create the app (the package name is now mandatory)
2. The ten app-content declarations — privacy policy, ads, advertising ID, target audience, data safety, the IARC questionnaire…
3. Store settings (category, contact)
4. Main listing (English) + Korean translation
5. **Countries/regions before creating a release**
6. Production release + release notes
7. Submit from the publishing overview

Step 5 was the key. Create the release first and you get "no countries selected"; pick the countries first and the error never appears. Trivial, but it removes one round trip per app.

### Skipping internal testing

All six went straight to production without an internal-testing track. The web games were already verified in a local browser and an emulator, and a new app's first review takes days either way.

### Gameplay video as a default deliverable

Every one of the six got a YouTube Shorts gameplay clip linked from its listing. There's an emulator auto-play → screen-record → ffmpeg pipeline, so it's under ten minutes per game. The rule "only skip the video for apps where there's nothing to watch" held this time too.

## The mistakes I actually made

The upside of a batch is that the procedure hardens. The downside is that **the accidents come six at a time.**

**All six bundles were the same game.** The Apps in Toss wrapper is created by copying the first game's, and the step in the build script that rewrites the source-game path failed silently. The result: bundles for all six apps containing the reaction-speed game, uploaded, with test pushes already sent. I caught it before requesting review, but from then on **checking that `dist/index.html`'s `<title>` is the right game before uploading** is a fixed step in the procedure. Wrongly uploaded bundles can't be deleted, so they're still sitting in the console with a "defective" memo.

**New apps missing from cross-promo.** My apps show each other in an "other apps you might like" list, and three days after going live the six new games weren't in it. The cause: the `play=0` flag in the registry CSV was never flipped after launch. With no server, that flag file is the only source of truth, and updating it wasn't on the checklist. Now "confirm live → flag to 1 → publish" is the last line of the release procedure.

**The Play builds shipped without ads.** My AdMob account has been suspended for invalid traffic since late August (until September 24), so the Play builds went out with the ad SDK removed. The Apps in Toss builds use the platform's own ad inventory instead, so I created 17 banner/interstitial/rewarded placements for them. The rating rule that the two platforms' games "must be identical" is about game content, so ads or no ads isn't an issue.

**CSS `display: flex` overriding the `hidden` attribute, for the third time.** A trap I've already written about twice on this blog, and I stepped in it again in Number Rush: `.card .row[hidden]` had `display: flex` on it, so a row that should have been hidden stayed visible. This time I fixed just that rule; adding `[hidden] { display: none !important }` to the shared CSS to close the path for good is the first task of the next batch.

## The day after launch — five pieces of feedback

Everything my family and friends told me within a day of going live went into v1.0.1.

- Number Rush feels too similar to Reaction Challenge → tagged as neighbors so they recommend each other
- Nobody understood the "Free mode" button in Hangul Word Guess → "Start"
- Reviving in Tap Bird kills you instantly → pipes cleared on revive + one second of invulnerability
- Wanting to replay the same Sudoku board → six-digit game numbers, per-difficulty history and retry
- Cleared Lights Off levels can't be replayed → a level-select screen with stars, locks and retries

And one thing missing from all six — **a button to leave the game and go home.** I'd been relying on the back gesture, but a game screen with no visible exit feels claustrophobic. It went into ten apps at once, including the four older games.

## Five days in numbers

- 6 games, 2 stores, 9 languages
- 6 new Play registrations: several review-page errors on the first app → 0 on the sixth
- 6 IARC ratings, issued the same day
- 17 Apps in Toss ad placements, 6 scheduled pushes, 6 notification-consent forms
- 6 YouTube Shorts, 12 blog posts (KO/EN), 6 Instagram posts
- 5 pieces of feedback + 1 shared improvement shipped within 24 hours of launch
- Play listings machine-translated into 27 languages (free) — an app that speaks nine languages is invisible in search if its listing speaks two

## Next

The procedure is set. The next batch is 13 games whose code is already finished (2048, Minesweeper, Snake, Brick Breaker, Gomoku, Solitaire…) — only icons and screenshots remain. With this checklist, registration itself should fit in a day. I'll write it up when it happens.

I post updates here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
