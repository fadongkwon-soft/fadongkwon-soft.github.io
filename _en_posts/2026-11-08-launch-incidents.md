---
title: 21 Launch Incidents, Zero Errors — Three Months of a Solo Developer's Postmortems and the Launch Gate They Produced
description: From August to November, shipping apps to Google Play and Apps in Toss, I hit 21 launch incidents, grouped here into five kinds — review, revenue, visibility, data and build. A privacy policy URL that returned 404, apps that went live with zero ad placements, zero push consents for three weeks, every custom analytics value silently dropped. What they share is that nothing ever threw an error. For each incident I note how long it went unnoticed, why it was missed and what prevents it now, then describe the resulting 72 automated checks and the 98-item evidence-backed checklist
image:
  path: /assets/img/20261108_launch-incidents/cover-en.png
  alt: "21 launch incidents, zero errors"
date: 2026-11-08 01:15:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/launch-incidents/
alt_url: /ko/posts/launch-incidents/
struct_exempt: [images]
tags: [google play, apps in toss, automation, solo developer, dev log]
---

In mid-August this year I started shipping mini games and apps in earnest. Today 88 of my apps are on Google Play, and on Toss's Apps in Toss platform I have filled the workspace cap of 50. In those three months I hit 21 launch incidents.

Looking back, all 21 share one thing: **nothing threw an error.** Builds succeeded, consoles showed green, and the apps ran fine when opened. That is why one of them went unnoticed for five weeks.

This post is the record of those 21. For each one I note what went wrong, how long I did not know, why I missed it and what prevents it now. No amounts are included.

## In one sentence

> **A green light in the console (approved, active, sent) is not a success metric. The success metric is always a value seen from the user's side.**

The banner shows on a real device, the consent sheet actually appears, the delivery count goes up, the icon shows on another app's home screen, the URL returns 200 when you open it. Every one of the 21 happened because one of those was not checked.

## 1. Caught in review

| Date | Incident | Why it was missed | What prevents it now |
|---|---|---|---|
| 8/15 | First Play review rejected for an "invalid privacy policy" | The whole site was returning 404 and I never opened the URL myself | Check the policy URL's status code directly before submitting |
| 8/15 | Toss rejection for a "bottom sheet right after entry" | There was a usage condition, but a reviewer tapping fast still counted as right after entry | The sheet only appears after at least one round in the same session |
| 8/29 | Kids' app (Math Monsters) rejected under Play's Families policy — the other-apps list showed tarot and saju apps | The list was a CSV fetched at runtime, so exposure changed regardless of the build | The app registry must state whether an app is for kids, and kids' apps show only kids' apps |
| 9/19~20 | Six new apps rejected 13 times on Toss for "first load over 20 seconds" | The 20 seconds was not network time but **the moment the screen settled** | A check for zero external requests on first load and a check that the first screen does not change for 16 seconds |
| 11/6 | Play rejection: "not a valid privacy policy page" | I used a redirecting URL (www) to the canonical page; the automated check passed and only the human reviewer rejected it | One canonical policy URL with no redirect |

The 20-second rejection had two layers. Even after removing the requests the first screen made to outside servers (icons, a CSV, an ad script), the rejections continued, and it was the user watching a real device who pointed out that "the screen keeps changing." The other-apps list was redrawn wholesale after loading, so the screen kept moving for 10 to 20 seconds. The full story is in [Toss 20-second cold start](/posts/toss-20s-cold-start/).

## 2. Revenue that was silently zero

| Date | Incident | Unnoticed for | What prevents it now |
|---|---|---|---|
| 8/26 | AdMob account **suspended for 29 days** for invalid traffic | Learned from the suspension notice | Development builds use sample ad IDs only; real ad IDs are checked in release builds only |
| 9/10 | Ten Toss apps **went live with zero ad placements** | 2 days | An automated check that every wrapper has ad placement settings |
| 9/13 | The "Maybe later" button on a rewarded-ad sheet slid under the banner, making the ad look forced | That day | A check that elements fixed to the bottom of the screen leave room for the banner |

The zero-placement incident was the scariest. The games work perfectly without ads, so neither users nor the console sent any warning. I only found out while building a ledger that stacks per-app ad revenue by date, when those ten columns came up as zero ([the apps that shipped without ad placements](/posts/toss-ads-missing-placements/)).

The AdMob suspension came from builds carrying real ad IDs installed on my development phone and family phones. There was no appeal, and during the suspension I could not even open the console ([the invalid traffic suspension](/posts/invalid-traffic-suspension/)).

## 3. Working, but nobody could see it

| Date | Incident | Unnoticed for | What prevents it now |
|---|---|---|---|
| 8/19 | The other-apps list stayed on an old four-line CSV, so new apps appeared nowhere | Days | The command that publishes the registry to the site runs a structure check first |
| 9/4 | Six apps live on Play stayed "unreleased" in the site registry | 3 days | Fail if the store listing is live but the site's install page is missing |
| 9/12 | Play listing language counts varied by app — 1, 2 or 29 — and videos existed in only 2 languages | Weeks | A standard of 29 languages, with Korean-only apps kept on a separate list |
| 9/14 | Toss "core metrics" were empty for all 29 apps — inputs used for exposure and recommendation | **5 weeks** | A manual item in the Toss registration step |
| 11/1~3 | Four failed site deploys — icon files for five new apps did not exist | 3 days | An app-icon existence check, and icons before the release flag |

The longest one was Toss core metrics. The console did show a hint, but the release procedure had no item for it, so 29 apps had blanks for five weeks. The failed deploys were a case of knowing that a push is not a deploy and still skipping the check ([creating fifteen apps in one day](/posts/play-fifteen-apps-one-day/)).

## 4. Data that lied

| Date | Incident | Unnoticed for | What prevents it now |
|---|---|---|---|
| 9/7 | **Zero consents** for Toss functional push — the code that requests consent did not exist | 3 weeks | An automated check that app code has the consent request and the end-of-round signal |
| 9/8 | Snake's Toss description went out as "950" — a number from another column had shifted in | 4 days | A structure check on the registry CSV |
| 9/12 | The real reason the consent sheet never appeared: **group code and template code did not match** | 3 weeks | A check that the wrapper's template code matches the console value |
| 9/12 | Failed sheet requests were recorded as "asked," so those devices would never be asked again | — | Record only when the result says the sheet actually appeared, then confirm by the next day's delivery count |
| 10/27 | Every custom value in Toss analytics events was being dropped — the same format error in 25 wrappers | Weeks | No automated check yet; verified manually as a ratio against screen events |

The push incident had three layers. The console showed "sent" every day while the audience was zero. Adding the request code exposed the code mismatch, so the sheet still did not appear, and once that was fixed, even failed requests were being recorded as "asked." Fixing all three took three weeks ([the push consent root cause](/posts/push-consent-root-cause/)).

The analytics incident is the only one with no automated check yet. I had shrugged it off as "events are always undercounted," but in reality every value was being dropped and only the names remained. The growth program measurements made in the meantime were nearly useless because of this bug.

## 5. Builds and deploys that were silently wrong

| Date | Incident | Unnoticed for | What prevents it now |
|---|---|---|---|
| 8/31 | Six Toss bundles were **all the same game** | Went as far as test pushes | Check the page titles inside the bundle before upload |
| 9/11 | A scheduled post's tag `2048` was parsed as a number and killed the build on publish day | That day's post never deployed | A scheduled-post check script |
| 11/7 | Adding 6,147 audio files to the site made every deploy fail on a 10-minute timeout | That day | Keep the site at around 3,300 files |

The six-identical-games incident happened because the step that rewrites paths after copying a wrapper folder failed silently. The bundles built fine and uploaded fine. Only after opening the test pushes did I see that all six showed the same screen.

## What came after — the launch gate

On September 12 I set one rule: **do not call an app "launched" until its checklist is fully checked and the check tool passes.** What shows in the store is only half a launch.

| Part | What it is |
|---|---|
| Automated checks | 72, grouped into registry, development, ads, build, Toss and site stages |
| Checklist | 98 items per app: 40 automated, 52 manual, the rest marked not applicable |
| Verdict | Fails if even one item is unchecked |
| Evidence | Manual items are checked together with a date, a number or command output |
| Helper tools | First-load check, first-screen settle check, ad placement check, banner overlap check, back-navigation check, hub freshness check, QR decode check |

The automated checks count what a machine can count. Are the ad placement settings there, does the push template code match, are there no external requests on first load, does the site have the icon and install page, does the QR decode to the right address.

What a machine cannot see stays as manual items. Is the banner actually visible on a real device, does the consent sheet actually appear, is the next day's delivery count above zero. Those items are checked not as "done" but as **"confirmed working for users,"** with the observed value written next to them. So right after release an app's status is not "launched" but "released (awaiting verification)," and it closes only after the next day's numbers are confirmed ([fourteen games on one day, one week later](/posts/fourteen-games-first-week/)).

## What I learned

- **No errors means nothing.** All 21 happened without errors. Always check from the outcome side.
- **Look at user-side values, not console numbers.** Not "sent" but how many received it; not "active" but the screen on a real device.
- **If you write a rule down, apply it to existing apps too.** The group-code incident dragged on for three weeks because the rule was in the docs but never applied to apps already shipped.
- **Human memory always drops something when the batch grows.** Shipping fifteen apps in a day on memory means one gets missed. Let the machine count what can be counted.
- **Some incidents will slip past the tools.** The analytics incident was found after the gate already existed. The checklist grows by one line every time something breaks.

The apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The incidents and dates in this post come from my own release records for August to November 2026 (the incident table in my launch checklist and my work logs). Review criteria and console behavior can change, so check the latest guidelines before doing the same.
{: .prompt-info }
