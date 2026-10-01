---
title: When to Ask for a Rating — One Review-Prompt Rule for Toss and Google Play
description: Reviews are one of the four signals Apps in Toss uses to pick recommended mini apps, yet our apps had never once asked for a rating before 29 September. Only for people who have really used the app, rarely, and without breaking the flow — how we added the same rating prompt to 33 Toss mini apps and 27 Google Play apps, and what tripped us up in testing
date: 2026-10-01 11:10:00 +0900
categories: [Devlog, Platform]
permalink: /posts/review-prompt-toss-play/
alt_url: /ko/posts/review-prompt-toss-play/
tags: [apps in toss, toss, google play, android, in-app review, solo developer, dev log]
---

## Info
> Reviews are one of the four signals Apps in Toss uses to pick recommended mini apps, yet none of our apps had ever asked for a rating until 29 September 2026. We added one shared rating-prompt gate to 33 Toss mini apps and 27 Google Play apps. It only fires for people who have used the app five times across at least two different days, never right after launch and never on top of an ad, at most three times per device with sixty days in between. Toss and Google each decide for themselves whether the dialog actually appears, so the app never waits for the outcome.
{: .prompt-info }

From 22 October, Apps in Toss picks recommended mini apps on four signals: UX, real usage, reviews and performance ([our notes on the exposure policy](/posts/apps-in-toss-exposure-policy/)). When we went through the thirty-odd apps we run, there was **not a single line of code asking anyone for a rating or a review.** Reviews had no way to accumulate in the first place.

So we added a rating prompt on both Toss and Google Play. The hard part was not adding it but deciding when to show it. Show it at the wrong moment and you collect irritation instead of reviews, and on Toss it is a reason for the review team to reject the build.

## The principle — at a satisfying moment, rarely, away from the flow

We followed what the Toss developer documentation recommends.

- **Ask right after the core action.** In our apps that means when a round ends, when numbers have been drawn, or when a card has been flipped and the reading shown.
- **Never wait for the result.** Toss decides on its own, under a fatigue policy, whether to show the dialog, and shows nothing to people who have already rated. Google Play decides by quota and does not even tell the app whether the dialog appeared. So nothing in the app — no screen change, no reward — depends on the outcome.
- **Never ask twice in the same session.**

## When it shows

| Condition | Value | Why |
| --- | --- | --- |
| Total uses | 5 or more | Do not ask people who have barely tried it |
| Days used | At least 2 different days | Ask people who came back, not one-day visitors |
| This session | From the 2nd use onwards | A sheet right after launch is a Toss rejection reason (we learned this with the notification consent sheet) |
| Other sheets | Skipped if the notification consent sheet was shown in this session | Never stack two sheets |
| Asking again | 60-day rest after a request | Asking often wears people out |
| Lifetime | At most 3 times per device | Some people will never leave one |
| Timing | 1.5 seconds after the result screen is drawn | Let them see the result first |
| Ads | If an interstitial or rewarded ad is showing, 1.5 seconds after it closes | Never on top of an ad. If it does not close within a minute, give up for that session |

If the user switched to another app in the meantime and the screen is hidden, the request is not made.

## One place, spread to every app

With more than thirty apps, adding this app by app guarantees that some app gets missed. So we attached the review decision to a point every app already calls when a round ends: the "one use finished" signal that decides whether to show the notification consent sheet. Only one shared module changed; each app just needed a rebuild.

- **Toss**: the wrapper's bridge calls `Review.request` from the Apps in Toss SDK. It only works on Toss app 5.253.0 or later; on older versions it skips quietly without recording anything, so the user gets another chance after updating Toss.
- **Google Play**: we added a new `requestReview` bridge to the Android wrapper that calls the Google Play In-App Review API. Older installs without that method also skip quietly.
- **Kids' apps are switched off.** For Hangul Monsters and Math Monsters the web-side decision is disabled, and the Play builds leave the review library out entirely — the same way we leave the ad SDK out.

## What tripped us up in testing

- **The dialog never appears on the emulator.** The emulator has no Play Store, so the request ends with "failed to bind to the service". It looks like an error but it is expected; the real dialog only appears for apps installed from Play. On the emulator we only confirmed that a request which passed the gate reached the native code.
- **The emulator clock runs on UTC.** We seeded usage history as "yesterday" by the PC's clock, which became "today" on the device, so the "two different days" condition never held. Dates have to be computed inside the app page before seeding.
- **Some games showed an interstitial right after the result screen.** Left alone, the rating dialog would collide with the ad or be buried under it. The prompt now waits while an ad is showing and fires after it closes.
- The decision rules are pinned down by 13 unit tests covering unmet conditions, the rest period, the lifetime cap, waiting for ads and storage errors.

## Release

On 29–30 September we submitted and released 33 Toss mini apps (the two kids' apps excluded), and on 30 September we pushed updates to 27 Google Play apps. The six apps we recently launched on Play will get the same change once their first review finishes; uploading a new version now would restart that review from the beginning.

The release notes say that people who have used the app several times may occasionally see a dialog to leave a rating. There is no reason to hide the change.

## Keeping it in new apps

The most common failure after a "do it everywhere at once" change is that the next new app quietly misses it. So we added an item to our launch checklist and made the pre-launch checker verify three things.

- The app code is wired to the review decision (and it is switched off for kids' apps)
- The Play build includes the review library (and kids' apps leave it out)
- The Toss wrapper bridge has the request function

All 35 of our current apps pass.

## What we will watch

By design, the first dialog only appears for someone who has used the updated app five times across two days. So the earliest effect should show up from this weekend. We log Toss reviews and Play reviews into our ledger every week, and once a month of numbers is in, we will add them to this post.
