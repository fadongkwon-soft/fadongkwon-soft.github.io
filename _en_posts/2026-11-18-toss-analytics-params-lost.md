---
title: My Event Logs Were Quietly Wrong — Why Every Custom Value in My Apps in Toss Analytics Went Missing for Six Weeks
description: The entry event I added to measure growth program traffic logged 55 times in a day, while the SDK's own screen log recorded 1,070 on the same day. I almost wrote it off as "events always undercount," but on a second look my wrapper's logEvent was passing values in a shape that did not match the SDK contract. Every custom value such as mode, difficulty and result was dropped, and the same code sat in 25 wrappers. How I confirmed the contract from the SDK's type definitions and source, why I concluded revenue was not affected, the numbers after fixing two apps first, and how to verify an API that never throws by cross-checking it
image:
  path: /assets/img/20261118_toss-analytics-params-lost/cover-en.png
  alt: "My event logs were quietly wrong"
date: 2026-11-18 23:41:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/toss-analytics-params-lost/
alt_url: /ko/posts/toss-analytics-params-lost/
struct_exempt: [images]
tags: [apps in toss, toss, javascript, debugging, solo developer, dev log]
---

In late October, [Tap Bird was picked for the Apps in Toss partner growth program](/posts/toss-growth-program-tap-bird/), and from October 26 Toss started sending people over with a "browse a mini app for 10 seconds, earn points" promotion. At the end of that post I wrote that I would measure return visits separately for the `?from=growth` cohort. I had added `?from=growth` to the promotion's landing path in the console, and the app reads that value and logs an entry event.

```ts
if (GROWTH_ENTRY) logEvent('tb_growth_enter', {});
```

This post is about why that measurement was nearly useless for the first few days. The cause was not the program but one line in my wrapper code, and that line had not thrown a single error in the six weeks since mid-September.

## The trigger: 55 entries, 1,070 screens

On the evening of October 27, I queried Tap Bird's entry event through the console's event log API.

| Event | 10/26 | 10/27 (so far) | Parameters the console showed |
|---|---|---|---|
| `tb_growth_enter` (growth entry) | 55 | 59 | `anonymous_key`, `is_private_mode` |
| `tb_run_start` (run started) | 17 | 9 | `anonymous_key`, `is_private_mode` |

That day had 754 daily users. Seventeen run-start events were absurdly few by comparison. Yet the first conclusion was "console event counts always come in far below user counts, so use them only to compare trends, not totals." That was an assumption with nothing behind it.

Asked to check everything again from the start, I pulled out one more comparison: `/::screen`, the screen log the Toss SDK records on its own.

| Event | 10/24 | 10/25 | 10/26 |
|---|---|---|---|
| `/::screen` (logged by the SDK) | 71 | 53 | 1,070 |
| `tb_growth_enter` (logged by us) | — | — | 55 |

On the program's first day, screen logs jumped to about twenty times their usual level. The landing path had already been switched to `?from=growth` on October 24, so most people arriving that day were growth traffic. If things were working, the entry event should have been in the same range as the screen log. Fifty-five was a twentieth of it.

There was one more oddity. The run-start event passes the mode, world, stage and bird type, yet the console showed only the two parameters the SDK adds automatically. **None of the values we sent were there.**

## Digging in: the shape the wrapper handed the SDK

### On the app side it was a one-line pass-through

The shared package in my game monorepo sends analytics logs like this. It is a thin function that only sends on Toss and does nothing on Play or the web.

```ts
export function logEvent(name: string, params: Record<string, LogValue> = {}): void {
  try {
    window.TossAdsBridge?.logEvent?.(name, params);
  } catch {
    /* 분석 로그 실패는 무시 */
  }
}
```

The actual sending happens in the bridge (`toss-bridge.js`) inside each Toss wrapper. That is where the problem was.

```js
// Before
logEvent(name, params) {
  try {
    const fn = Analytics?.log;
    if (typeof fn !== 'function') return;
    const p = fn({ log_name: name, ...(params || {}) });
    if (p && typeof p.catch === 'function') p.catch(() => {});
  } catch {
    /* 분석 로그 실패는 게임을 막지 않는다 */
  }
},
```

It **spreads** the event name and the values into a single object, something like `{ log_name: 'tb_run_start', mode: 'adventure', world: 2, ... }`.

### The SDK contract was in its type definitions and source

Instead of guessing, I opened the type definitions of the SDK installed in the wrapper (`@apps-in-toss/web-framework` 3.5.0).

```ts
interface EventLogParams$1 {
  log_name: string;
  log_type: string;
  params: Record<string, LogParam>;
}

interface EventLogParams extends Omit<EventLogParams$1, "log_type"> {
  log_type: "debug" | "info" | "warn" | "error" | "event" | "screen" | "impression" | "click" | "popup";
}

declare const Analytics: {
  log: (params: EventLogParams) => Promise<void>;
  ...
};
```

The contract is `{ log_name, log_type, params: {...} }`. Values belong inside `params`, and `log_type` is required. The runtime code in the same package shows that `Analytics.log` passes the object it receives straight through to the native side of the Toss app.

```js
const eventLog = (params) => callAsyncMethod("eventLog", params);
...
const Analytics = {
  log: eventLog,
  ...
};
```

The click, impression and screen logs the SDK records on its own are all built in that shape.

```js
return eventLog({
  log_type: "event",
  log_name: log_name ?? `${groupId}::click`,
  params: { ...otherParams, search, referrer: getReferrer(), ... }
});
```

Side by side:

| | What my wrapper sent | SDK contract |
|---|---|---|
| Event name | `log_name` | `log_name` |
| Event type | Missing | `log_type: 'event'` |
| Custom values | Spread at the top level | Inside a `params` object |

The SDK passes the object through without checking it, and the native side, finding no `params`, recorded only the default parameters. That explains why every custom value disappeared. Why most events went missing while a few were still recorded, I could not confirm, because I cannot see how Toss processes them.

### How many copies of this code were there

I went through every wrapper folder.

| Bridge state | Wrappers |
|---|---|
| Has logEvent, wrong shape (values spread) | 25 |
| No logEvent at all (app calls do nothing) | 43 |

The wrong shape first arrived in a September 17 commit titled "unify logEvent across 29 Toss bridges," and every wrapper created after that was copied from this bridge and inherited the same line. In the 43 without logEvent, the app's `window.TossAdsBridge?.logEvent?.(...)` quietly did nothing. In neither case did a single error appear on screen or in the console. `Analytics.log` is designed to be "silently ignored, with no error" even on unsupported app versions, and the wrapper had wrapped it in a try/catch and a `.catch(() => {})` on top of that.

## Was revenue affected? I settled the scope first

The fix itself is one line, but every fix means a fresh bundle build and another review. So first I checked in the code whether ad revenue or app behavior was affected.

- Showing ads, hearts (play chances refilled by rewarded ads) and 1 KRW promotion payouts do not use logEvent at all. The only logEvent calls were analytics events such as run start and end, per-mode records, leaderboard opens, and cross-promotion impressions and clicks.
- logEvent is wrapped in try/catch on both the app side and the bridge side, so a failure never blocks the game.

The conclusion was that only analytics was affected. So I **fixed and shipped the two apps used directly for growth program measurement (Tap Bird and Gomoku) first**, and fixed only the source of the other 23 so the change would ride along with each app's next build.

```js
// After
logEvent(name, params) {
  try {
    const fn = Analytics?.log;
    if (typeof fn !== 'function') return;
    // SDK 계약 { log_name, log_type, params } — 값을 펼쳐 넣으면 params 가 사라지고 대부분 누락된다(10/27 발견).
    const p = fn({ log_name: name, log_type: 'event', params: params || {} });
    if (p && typeof p.catch === 'function') p.catch(() => {});
  } catch {
    /* 분석 로그 실패는 게임을 막지 않는다 */
  }
},
```

(The new comment says: SDK contract `{ log_name, log_type, params }`; spreading the values drops `params` and loses most events, found 10/27.)

| Time (10/27) | What happened |
|---|---|
| 18:46 | Commit fixing the Tap Bird and Gomoku bridges |
| 18:51 | Commit fixing the bridges of the other 23 wrappers (no review requested) |
| Right after | Test bundles Tap Bird 20261027-45 and Gomoku 20261027-32 sent to my phone, checked, then submitted for review |

When I checked the next evening, both bundles had already been approved, released and were live.

## The result: numbers after the fix

On the afternoon of October 30, I queried the same API again.

| Date | `/::screen` | `tb_growth_enter` | `tb_run_start` |
|---|---|---|---|
| 10/26 | 1,070 | 55 | 17 |
| 10/27 | 1,616 | 380 | 64 |
| 10/28 | 1,788 | 1,224 | 448 |
| 10/29 | 1,739 | 1,157 | 1,599 |

Entry events rose to about 1,200 a day, in the same range as the screen log (about 1,700). The more direct evidence is the parameter list. The run-start event's parameters grew from just `anonymous_key` and `is_private_mode` to include `mode`, `kind`, `world`, `stage`, `bird` and `growth`. The values we sent were finally arriving.

Two caveats when reading these numbers:

- On the night of October 28, Tap Bird's next bundle also went live (growth arrivals skip the home screen and go straight into a first flight, plus stronger entry detection). So the jump in run starts on October 29 includes the effect of that flow change. Entry events were already at 1,224 on October 28, before that bundle shipped, so I attribute that to the format fix.
- Entry events and screen logs do not have to match. One person viewing several screens adds several screen logs. What matters is that a ratio of one in twenty came back to the same range.

And the custom values from the six weeks before the fix cannot be recovered. Measurements from the first two days of the growth program for Tap Bird and Gomoku (such as the first-run start rate) could not be used for any decision because of this bug.

## What is left

- **Getting the other wrappers live**: The other 23 were fixed in source only, and each picks up the change the next time that app is built and released. In the current source, all 27 wrappers that have logEvent (including two that were created or got logEvent later) use the correct shape. I have not checked one by one whether every app's live bundle actually carries it.
- **Wrappers without logEvent**: As of now 47 still have no such function, so those apps record no analytics events. I plan to add it to the apps that need analytics first.
- **An automated check**: In my [launch incident chronicle](/posts/launch-incidents/) I listed this incident as the only one that still has no automated check. For now I look at the ratio of custom events to screen logs and the parameter list by hand. The next step is a launch gate check that verifies `log_type` and the `params` object in the bridge source.

## What I learned

- **A logging API that accepts anything without errors stays silent when the shape is wrong.** Analytics must never block the game, so swallowing failures is the right design. The price is that the "this is wrong" signal gets swallowed too. With an API like this, a successful call proves nothing.
- **Do not write it off as "events always undercount"; cross-check against an independent number.** Put a number that accumulates through a different path for the same app, day and people next to it (here, the SDK's own screen log), and a one-in-twenty gap shows up at once.
- **Check whether values arrived by looking at the parameter list.** Event counts alone leave a few events standing, which makes it easy to believe "it works." Whether the keys I sent appeared among the parameter names in the console was the stronger evidence.
- **Confirm the contract from the installed SDK's type definitions and source, not from memory.** It takes minutes to open them, and you can compare directly whether your wrapper calls the SDK the same way the SDK's own code does.
- **When code spread by copying, find every copy when you fix it.** One line sat identically in 25 wrappers. I split the rollout by impact (revenue or analytics), but fixed the source everywhere at once so it would not spread again from the next build.

The growth program and Tap Bird's adventure mode are covered in [Tap Bird Was Picked for the Apps in Toss Partner Growth Program](/posts/toss-growth-program-tap-bird/), and this incident along with 20 others is in [21 Launch Incidents, Zero Errors](/posts/launch-incidents/). News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The event counts in this post were queried through the Apps in Toss console event log API on October 27 and 30, 2026, and the code comes from commits in the wrapper repository and from the type definitions and source of the installed SDK 3.5.0. The SDK contract can change between versions, so if you are doing the same work, check the version you have installed.
{: .prompt-info }
