---
title: Rejected Nine Times for a 20-Second Cold Start — the Culprit Was Not Loading
description: An app that paints in 0.2 seconds on our machine was rejected for taking over 20 seconds to open. Six new apps, nine rejections in one day. It was not bundle size and not the SDK version. It was three outbound requests fired while the first screen was still painting
date: 2026-09-25 09:00:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/toss-20s-cold-start/
alt_url: /ko/posts/toss-20s-cold-start/
tags: [apps in toss, toss, app review, performance, cold start, solo developer, devlog]
---
## Info
> Six new mini apps were rejected nine times in one day for "cold start over 20 seconds", while loading in 0.2 seconds on our own machine. The cause was not bundle size or SDK version. It was three outbound requests fired during the first paint — a cross-promo CSV with untimed icon loads, a hosted CSV refresh, and a 342KB ad script injected into head. The fix was to push everything external behind window load plus five seconds.
{: .prompt-info }

## The symptom

We submitted six new apps for review and collected nine rejections in a single day. One line each:

> Mini app cold start exceeded 20 seconds

On our machine the first screen paints in 0.2 seconds. Same on a phone. When a number is off by a factor of one hundred, the two sides are usually measuring different things.

Rejections came back in **six to twelve minutes**. Human approvals take fourteen to fifty. A different time window means a different gate: this was **automated review** cutting us down. The platform's own notice acknowledges that system review results can disagree with real app behaviour.

## Hypotheses we eliminated

Writing these down so we do not dig here again.

- **Bundle size** — no different from apps that were passing
- **SDK version** — rejected on both versions we tried
- **Ad placement config, bridge script, app metadata approval** — all unrelated
- **CPU** — with 6x throttling the longest task was 0.6 seconds
- **"But our other apps were approved"** — not evidence. Re-review of an already-live app passes in five to eight seconds. Different conditions

## What was left

One thing survived: **requests going outbound while the first screen was painting.**

Assume that in the review environment our own website and external CDNs are slow or blocked outright, and everything fits. One request without a timeout waits forever for a response, and the page's load never completes — even though the app is already drawn on screen.

Three of them were firing in our bundle:

1. **The cross-promo list (CSV) and its icons.** A row of other apps at the bottom of the screen. Apps showing seven or eight rows fired eight icon requests, and `new Image()` has no concept of a timeout. In a blocked environment it hangs forever.
2. **Lottery round data.** The code that fetches a hosted CSV sat inside an initialization function, so it launched along with boot.
3. **The ad SDK.** The banner initialization call injects a 342KB script into head as `<script async>`. Async or not, it holds the document's load event.

## requestIdleCallback was not the answer

We had already deferred these once, wrapping them in `requestIdleCallback`. Surely it runs when things are quiet.

Measuring showed the **idle callback running before load** — at the 150 to 200ms mark. The first screen is light, so from the browser's point of view things were already quiet. The requests went out exactly as before.

We believed it was deferred. It was not. We did not know until we measured.

## The fix

One function in the shared package, and everything outbound moved behind it.

```ts
/** Runs fn extraMs after window load.
 *  All external requests and external script injection go here. */
export function afterSettled(fn: () => void, extraMs = 5000): void {
  const run = () => setTimeout(fn, extraMs);
  if (document.readyState === 'complete') run();
  else window.addEventListener('load', run, { once: true });
}
```

The layout we settled on:

- Ad attach and preload → load + 1.5s
- Cross-promo CSV and icons → load + 5s, with an **8-second cap** on each icon, cut by setting `src=''`
- Lottery round CSV refresh → load + 5s

The point is ordering, not timing. **Paint the first screen from the bundle alone.** Fetch outside things once the screen is up and settled.

## Then we made a machine check it

Putting the fix in the code is not enough. The next app we build will make the same mistake and collect the same rejection.

A headless browser script now opens the app and **counts outbound requests during the first paint window**, wired into our release checklist. Anything other than zero fails. After the fix all six apps load in 140 to 180ms, with the first external request at 5.16 to 5.20 seconds.

## What is still unsettled

Written honestly as of September 20.

The six apps carrying the fix stayed in progress for over an hour after submission. Given that they were being cut in six to twelve minutes before, that is **the first time we cleared the automated gate**.

But another app with the same fix was rejected again in eight minutes, for the same reason, from a bundle that passes our local gate. We resubmitted the identical bundle to see whether the verdict is stable. If the same input produces different outcomes, the cause is variance in the review environment rather than our code — and that is a case to raise with the platform, with measurements attached.

## Takeaways

- Numbers measured on your network are not the review environment's numbers
- Paint the first screen **from bundled assets only**. Everything external goes after load
- `requestIdleCallback` does not guarantee "later". On a light app it runs before load
- An image request without a timeout hangs forever in a blocked environment. Cap it and cut it
- After fixing, **make a machine check it**. People forget by the next app
