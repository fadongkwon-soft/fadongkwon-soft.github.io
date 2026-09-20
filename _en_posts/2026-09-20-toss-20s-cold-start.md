---
title: 'Fixing a "Cold Start Over 20 Seconds" Rejection Twice — 20 Seconds Is When the Screen Stops Moving'
description: Apps that paint in 0.2 seconds on our machine were rejected for taking over 20 seconds to open. The first cause was outbound requests during the first paint. After fixing that they were rejected again, because the first screen kept re-rendering as remote data arrived
date: 2026-09-20 14:41:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/toss-20s-cold-start/
alt_url: /ko/posts/toss-20s-cold-start/
tags: [apps in toss, toss, app review, performance, cold start, solo developer, devlog]
---
## Info
> Mini apps that paint in 0.2 seconds on our machine were rejected for "cold start over 20 seconds". The first cause was outbound requests fired during the first paint. After fixing that, they were rejected again — because the first screen kept re-rendering for another ten to twenty seconds as remote data arrived. The lesson: 20 seconds is not when the network finishes, it is when the screen stops changing.
{: .prompt-info }

## The symptom

We submitted six new apps for review and collected nine rejections in a single day. One line each:

> Mini app cold start exceeded 20 seconds

On our machine the first screen paints in 0.2 seconds. Same on a phone. When a number is off by a factor of one hundred, the two sides are usually measuring different things.

Rejections came back in **six to twelve minutes**. Human approvals take fourteen to fifty. A different time window means a different gate: **automated review** was cutting us down. The platform's own notice acknowledges that system review results can disagree with real app behaviour.

## Hypotheses we eliminated

Writing these down so we do not dig here again.

- **Bundle size** — no different from apps that were passing
- **SDK version** — rejected on both versions we tried
- **Ad placement config, bridge script, app metadata approval** — all unrelated
- **CPU** — with 6x throttling the longest task was 0.6 seconds
- **"But our other apps were approved"** — not evidence. Re-review of an already-live app passes in five to eight seconds

## Cause one: requests going out during the first paint

One thing survived: **requests going outbound while the first screen was painting.**

Assume that in the review environment our own site and external CDNs are slow or blocked, and it fits. A request without a timeout waits forever, and the page's load never completes — even though the app is already drawn.

Three were firing in our bundle:

1. **The cross-promo list (CSV) and its icons.** Apps showing seven or eight rows fired eight icon requests, and `new Image()` has no concept of a timeout.
2. **Lottery round data.** A hosted CSV fetch sat inside an initialization function, so it launched with boot.
3. **The ad SDK.** Banner initialization injects a 342KB script into head as `<script async>`. Async or not, it holds the document's load event.

### requestIdleCallback was not the answer

We had already deferred these once with `requestIdleCallback`. Measuring showed the **idle callback running before load**, at the 150 to 200ms mark. The first screen is light, so the browser considered things quiet already. The requests went out exactly as before.

### The first fix

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

Ad attach moved to load + 1.5s, promo CSV and icons to load + 5s (icons capped at 8s and cut), round CSV refresh to load + 5s. After the fix all six apps loaded in 140 to 180ms with the first external request at 5.16 to 5.20 seconds.

We thought that was the end of it.

## And then they were rejected again

Four apps were cut for the same reason, from bundles that passed every local gate.

What broke it open was not code. It was **watching the app on a real phone**:

> "The 'apps you might like' row keeps updating every few seconds. Icons change, the order changes. It goes on past twenty seconds."

The screen was already up. It just would not stop moving.

## Cause two: the first screen kept re-rendering

Following the code:

1. The promo row **renders** from the bundled (or cached) list
2. At load + 5s the remote CSV arrives
3. If it differs, the list is **re-rendered wholesale** — the order changes and icons fall back to emoji
4. Icons for the new rows are fetched and **swapped in another 5 seconds later**

Because the first fix only pushed the requests back, the re-render now *started* five seconds in. On a slow connection the churn runs for ten to twenty seconds.

Review — human or automated — reads that as **still loading**. It also explains why the first rejections took an erratic six to twelve minutes: when the screen settles depends on when the icons arrive.

**"20 seconds" is not when the network finishes. It is when the screen stops changing.**

## The second fix: render once per session

- The promo list renders **once, at boot**
- Remote CSV and icons are fetched and written to `localStorage` only — they take effect **on the next launch**
- An icon is drawn on first render only if it is already cached; otherwise the emoji stands for this session
- Lottery round refresh behaves the same way: fetch, store, do not touch the screen

One line: **do not write code that updates the screen after boot. Remote data lands on the next launch.**

What a user loses is "an app added today does not appear today". That is a fine trade for not being rejected.

## Two gates

A fix that lives only in code will be forgotten by the next app. Two machine checks now sit in the release checklist.

- **load_gate** — opens the app headless and counts **outbound requests during the first paint**. Anything but zero fails
- **settle_gate** — watches the first screen's DOM for 16 seconds starting at load + 1.5s. **Zero changes** or it fails. Old bundles trip it at the five to six second mark when the promo row redraws

The need for that second gate is the point of this post. The first one only answers "when did we request", never "has the screen stopped".

## Where it stands

As of the afternoon of September 20. Bundles carrying the second fix are back in review and clear both gates. Some apps did get through with only the first fix applied, so there is enough variance in the verdict that the same conditions can land either way.

## Takeaways

- Numbers measured on your network are not the review environment's numbers
- Paint the first screen **from bundled assets only**. Everything external goes after load
- `requestIdleCallback` does not guarantee "later". On a light app it runs before load
- Deferring the request is not enough. **If the deferred response redraws the screen, you have the same problem**
- Fetch remote data, store it, and apply it **on the next launch**
- "Has loading finished" and "has the screen stopped" are different questions. Have a machine check both
