---
title: Adding Record Tabs to a Leaderboard With No Read API — 20 Mini Games
description: Toss Game Center lets you submit a score but never lets you read the rankings back. With no data to draw, I split the job in two — my app owns the time axis, Toss owns the comparison — and shipped daily, weekly, monthly and all-time record tabs across 20 games
image:
  path: /assets/img/20260916_leaderboard-record-tabs/cover.png
  alt: Two panels showing my app owning personal records and Toss owning global rankings
date: 2026-09-16 01:33:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/leaderboard-record-tabs/
alt_url: /ko/posts/leaderboard-record-tabs/
tags: [toss, apps in toss, minigame, ui, solo developer, dev log]
---

I wanted rankings in my mini games. A record that sticks around is a reason to play one more round.

What I did not want was a server. Working alone, the moment a server exists you inherit incident response, a privacy policy, and store data-safety declarations. Not for one game — for more than twenty.

So the first thing I checked was the **Toss Game Center leaderboard**. It was already in the SDK.

## What it gives you, and what it does not

The `Game` namespace in `@apps-in-toss/web-framework` offers exactly three things.

| Available | Missing |
| --- | --- |
| `Game.setLeaderboardScore({score})` — submit a score | **Any API to read rankings** |
| `Game.openLeaderboard()` — open the ranking webview Toss built | Filtering by period |
| `Game.getUserProfile()` — Game Center nickname and avatar | User identifiers (excluded for security) |

The missing read API decided the architecture. **If you cannot fetch the ranking, you cannot draw a ranking table.** The docs say it plainly: the leaderboard UI and its data belong to Toss, and developers cannot modify or delete entries.

I first read that as a limitation. Turned around, it was a clean division of labour.

## Two layers

```
┌─ Records ─────────────────────────────┐
│  [Today] [This week] [This month] [Hall of Fame] │  ← my app: personal records
│   1  1,240 pts   today 14:22             │
│   2  1,180 pts   today 09:15             │
│  🏆 Toss ranking                          │  ← Toss: global and friends
└───────────────────────────────────────┘
```

**My tabs own the time axis of your own play. Toss owns how you compare to everyone right now.** Testing on a real device showed the Toss ranking webview has two tabs — global and friends — with no period split at all. The roles do not overlap; they complete each other.

The value of this shape is in what is absent. No server, no personal data collected, no abuse handling. Toss polices score manipulation, and since I only touch records stored on the device, there is nothing new to declare in store data-safety forms.

## The existing record arrays were not enough

Fourteen games already kept a `records[]` array with an achievement timestamp. I assumed I could reuse it directly. I could not.

Those arrays are a **top ten sorted by score**. If today's run ranks fifteenth all-time, it was already discarded. Building "today's best" means accumulating per period.

So I added period buckets.

```ts
periods: {
  day:   { key: '2026-09-24',  top: [...] },
  week:  { key: 'W2026-09-21', top: [...] },
  month: { key: '2026-09',     top: [...] },
}
```

On submission, if the key has rolled over, that bucket empties and starts fresh. Storage is O(1) and each period keeps an exact top ten no matter how much you play. Only the Hall of Fame reuses the original `records[]` — storing the same record in two places guarantees they drift apart eventually.

### Never measure period boundaries with the device clock

My first version called `new Date()`. But roll the device clock back a day and "today's number one" becomes free.

The SDK has `Environment.getServerTime()`, so the app measures an offset once at startup and derives everything from that. On versions that do not support it the code falls back to the device clock, and the record tabs still work.

For weeks I keyed on **the Monday of that week** rather than an ISO week number. That removes the year-end argument about whether a date belongs to week 53 or week 1.

## The failures that stay quiet

The bugs reported after shipping taught me more than the feature itself.

### "I finished a round and it is not on the leaderboard"

Someone finished a game of Sudoku and saw nothing in the Toss ranking. They had played on **Easy**, and the behaviour was intentional.

A Toss leaderboard is **one per app**. Mix a twenty-second beginner puzzle with a ten-minute expert one and the ranking stops meaning anything. So only the representative difficulty submits — except **there was no way for a player to know that.**

Now the button says so.

> 🏆 Toss ranking · Normal only

The same report surfaced a real bug. Five games including Sudoku were missing `seed()`, which other games had. It uploads your pre-update best score once at startup. Without it, a long-time player simply does not exist on the leaderboard *until they beat their own record*.

### First place in my tab, last place on Toss

Sort direction is set by `gameInfo.sortOrder` in the console. Every game had shipped with the default of **points, descending** — including a reaction-time game measured in milliseconds.

Leave a lower-is-better game on descending and the slowest player wins. Nothing throws an error, and my own record tab still shows the correct first place. This class of bug is invisible to the eye.

So I wrote an auditor.

```
game                    code   console  unit
 breakout              desc   DESC   points
 memory-card           asc    ASC    sec
 reaction              asc    ASC    ms
 ...
✓ no problems
```

It compares the `dir` in code against the console value, checks that the period-tab element exists, and verifies the wrapper bridge actually carries the Game API. The first run reported 66 problems — nine sort mismatches and 57 bridges missing the API.

The missing bridges are the scarier half. If the wrapper does not load the `Game` API, **submission fails completely and silently** while the app runs normally. I have already shipped three bundles whose bridge script was never injected and been rejected for it, so this kind of thing belongs in a checker, not in documentation.

## Things I fixed along the way

Staring at home screens for the ranking work kept surfacing other problems.

### One row costs 60px

`.screen` is a flex column with a 1.25rem gap, so **any element placed in the flow costs a full row — about 60 pixels.** Leaving the hearts badge there pushed the cross-promotion list below the fold, and the result screen stacked four buttons so that "Home" sat off-screen entirely.

I grouped two places.

- `.start-row` — the start button and the hearts badge share a row
- `.result-actions` — the secondary result buttons share a row

I got it wrong once in between. Slotting hearts into the existing links row truncated "How to play" at 375px, because two buttons were already consuming the full width. It ended up next to the start button instead — which is better anyway, since that is the button that spends a heart.

Do not verify this by eye. Emulate 375×812, stand up a fake 60px banner, and assert `scrollHeight === clientHeight`.

### Games that kill you for looking away

A phone call ends your run. Backgrounding was already handled, but **there was no way to pause while the app stayed open.**

Seven real-time games got a pause button. I built it as a shared module that deliberately **never touches the game loop itself.** Every game has a different state machine — Sky Jump already had its own `paused` phase, and a module stopping the loop on its own would have broken that rule. The module owns the button and the overlay; pausing and resuming are callbacks the game supplies.

Whack-a-Mole was the test that mattered, since it runs a countdown. Pause is meaningless if the clock keeps running. Measured: 46.5 seconds at pause, still 46.5 after sitting for 2.5 seconds, and resuming continued without a time jump. The remaining time only decreases inside the loop's `tick(dt)`, so stopping the loop stops the clock.

The overlay also registers with the back-navigation stack. Pressing back in Toss resumes the game instead of closing the app.

### One icon breaks the tone

I used the `⏸` emoji for pause, and devices render it in yellow, clashing with the plain back arrow beside it. I now draw two bars with `currentColor` so it inherits the button's own colour.

Placement was off too. In a HUD using `justify-content: space-between`, dropping a button in pushes it toward the middle. Whack-a-Mole used `flex-start` and looked fine — which is exactly why the games looked inconsistent.

### Growing counts grow the layout

I switched hearts to glyphs like the tarot apps (`❤️❤️🤍`), but watching several ads keeps adding glyphs until they shove the HUD aside. Glyphs now cap at the daily allowance and switch to a number beyond it.

| State | Display |
| --- | --- |
| 2 of 3 | `❤️❤️🤍 +` |
| 12, above the base of 3 | `❤️ 12 +` |

I had also made the badge tappable for topping up early, while the sheet only ever said "You are out of hearts." It now branches on the remaining count: "You have 3 hearts / watch an ad for 3 more."

### Coordinates you tuned are coordinates the device moves

A report said hearts overlapped the selection panel in Juice Spinner. It did not overlap at 375×812 in the browser.

On a real device the Toss header and ad banner shrink the viewport, so the panel rides up — while the badge stayed pinned at `top: 58px`. Re-tuning the coordinate just moves the problem to another device. I removed the absolute positioning and placed the badge inside the top pill row, so overlap became **structurally impossible**.

### A button is only as wide as its contents, even with display:flex

In the cross-promotion list, the chevron (`›`) sat at a different position on every row, following the length of each description.

`<button>` is a form control, so `display: flex` does not make it fill its container. On the home screen the parent used `align-items: stretch` and stretched it; in a bottom sheet — a plain block container — nothing stretched it. Setting `width: 100%` makes rows fill regardless of where they are mounted.

## An ad for every hint is too much

Someone pointed out that watching an ad for every Sudoku hint is harsh. They were right. Saving an ad impression is a bad trade if it makes people abandon the puzzle.

Two hints per game are now free, then an invite-reward ticket, then an ad. The button icon runs `💡2 → 💡1 → 📺` so you can see **before tapping** whether this one is free. Discovering the ad after you commit feels like a bait and switch.

## What is left

Twenty games have record tabs, and fifteen console sort settings were corrected to match their real metric and submitted for review.

What I have not solved is the **weak metrics**. The word game submits "which attempt you guessed on" (1–6), a range so narrow that nearly everyone ties. The lights-out puzzle's "level reached" has the same problem. A ranking only means something when the metric spreads out, and some games do not. I will need real distributions before deciding.

And given that the new auditor caught 66 problems on its very first run, there are surely more of the same waiting. Written down in a document, I forget. Written as a checker, I cannot.
