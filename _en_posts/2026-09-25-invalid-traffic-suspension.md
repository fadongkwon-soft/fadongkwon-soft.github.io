---
title: My Ad Account Was Suspended 29 Days for Invalid Traffic — The Culprit Was My Own Dev Phone
description: On August 26 my ad publisher account was suspended for 29 days over invalid traffic, with no appeal available. Auditing every codebase turned up a cause that was not malicious clicking but builds carrying real ad IDs installed on my development phone and run for months. The investigation, the four code-level blocks I added, and the fact that hurt most
date: 2026-09-25 20:00:00 +0900
categories: [Blogging, Episode]
permalink: /posts/invalid-traffic-suspension/
alt_url: /ko/posts/invalid-traffic-suspension/
image:
  path: /assets/img/20260925_invalid-traffic/cover.png
  alt: Illustration of a development phone generating invalid ad traffic
tags: [admob, invalid traffic, ad policy, android, solo developer, dev log]
---

On August 26 my ad publisher account was suspended. The reason: **invalid traffic**. The duration: **29 days**. That window closed yesterday.

During a suspension no ads serve at all. Two things were more frustrating than the revenue going to zero. First, **there was no appeal channel** — this was not the kind of action you argue your way out of, but one that simply expires. Second, **console access itself is blocked while suspended.** I wanted to register my test devices to prevent a recurrence, and I could not open that screen.

The notice also spelled out the stakes: a repeat means a **permanent ban**, and up to **60 days of earnings can be forfeited**. So finding the exact cause mattered far more than waiting out the 29 days.

## I had misunderstood what "invalid traffic" means

Seeing the phrase for the first time, I pictured someone attacking my apps by clicking the ads repeatedly. So I spent the first few days looking for who did it. Wrong direction.

Invalid traffic means **any impression or click that has no value to the advertiser**. Malice is not part of the definition. Impressions a developer generates while testing their own app count too — the advertiser did not pay to show ads to the person who built the app.

Only after reading the definition properly did I start suspecting my own code.

## I audited all four codebases

At the time, ad-carrying apps were spread across four codebases: two Flutter apps, one Android wrapper, and one separate Android app. I opened all of them and checked exactly two things.

**One: which ad IDs do debug builds use?**

The two Flutter apps had the **real ad IDs hardcoded even in debug builds**. Which means every time I installed and ran them on my phone during development, real ads served, and every one of those impressions was recorded against my account.

**Two: is there any test-device registration?**

I searched for `setTestDeviceIds`. Across four codebases: **zero occurrences.** With that setting, requests from the listed devices are treated as test requests and never counted as invalid traffic. It existed nowhere.

Put the two together and the conclusion writes itself. The likely cause was **builds carrying real ad IDs installed on my development phone and run for months.** The builds I had sideloaded onto family phones were the same story.

Google does not disclose the precise reason, so this is an inference. But it was a hole obvious enough that no other explanation is needed.

## Secondary cause: the internal test track

I found one more thing. My email and my spouse's were registered as testers on the Play internal test track.

Here is the part that is easy to miss: **builds on the internal test track are release-signed.** They are not debug builds; they run with real ad IDs. It is tempting to assume "it is a test track, so it will be treated as testing," but from the ad system's point of view those are ordinary users.

## What I suspected but ruled out

There are two Android emulators on my development PC, and I had run automated playthroughs on them at some point, so I suspected this strongly.

It turned out to be **irrelevant.** AdMob automatically treats emulators as test devices. Running an app on the emulator and reading the log showed the message that the request was sent from a test device, verbatim. No configuration needed for it to be discounted.

While checking, though, I found something else: **release builds using real ad IDs** were installed on that emulator. Harmless in the end because of the automatic test-device treatment, but that is safety by coincidence. Going forward, emulators get debug builds only.

## What I put in place

### 1. Split ad IDs by build type

Debug builds now use only Google's test ad units. On the Flutter side I branched on `kReleaseMode` and went as far as overriding the application ID with the sample value in the debug manifest. Any scheme that relies on a human remembering to switch it back will fail at least once.

### 2. Register real devices in code

I collected the device hashes for three devices — my dev phone, a tablet, and a family phone — and added them via `setTestDeviceIds` to all four codebases.

Extracting a device hash is slightly awkward. Running the app prints a log line telling you the hash to use for registration, but to see that log you must run the app once. **That run itself must not become invalid traffic, so it has to be a debug build.** For the remote phone I connected over wireless debugging, installed the debug APK, pulled the log, and uninstalled it.

### 3. Clean up testers and tracks

I emptied every tester email list on Play, removed the sideloaded APK from the family phone, and paused all eleven internal test tracks. Play has no way to delete an uploaded bundle, so paused plus zero testers is the furthest state you can reach.

### 4. Fix the overlapping banner

The audit turned up a separate problem: on Android, the bottom banner was drawing over the content. That is a layout where reaching for a button near the bottom of the screen can land on the banner instead. **Accidental clicks are invalid traffic too.** Now the app reserves space below once the banner loads.

## One more layer: do not request real ads when detected

Everything above assumes I configured things correctly. So I added one last safeguard in code.

If an emulator, a rooted device, or a debuggable state is detected, the app requests **only Google sample ad units, even in a release build.** It is written with spoofed device properties in mind. On a normal user's device nothing changes, and if I accidentally run a release build in my development environment, no real ad serves.

## The fact that hurt most

I wrapped all of this up in late August. And then found something missing from my accounting.

**Code fixes have no effect on live apps until they are deployed.**

The code on my PC was safe, but the apps installed on users' phones still ran the old code. To be protected from the moment ads start serving again, the fixed code had to actually be published before then. I only factored in that obvious fact as the reinstatement date approached, and spent early September rushing updates out for every ad-carrying app.

## The rules I wrote down

To avoid a repeat, I turned this into a checklist.

1. **Debug builds use test ad units only.** Enforced by build configuration, not by memory.
2. **Register real devices as test devices.** My own devices and family devices, all of them.
3. **Never run a release build with ads on a real device.** If verification is needed, use a debug build.
4. **Do not sideload onto family or friends' phones.** Do not add them as track testers either.
5. **Pause test tracks when not in use.** Release-signed means real ads.
6. **Keep banners out of interaction areas.** Accidental clicks are invalid traffic.
7. **Copy these settings into every new ad-carrying app.** New apps are the most dangerous.

And I corrected one belief that mattered most. Test-device registration is a mechanism that **discounts** that device's impressions and clicks. It is not absolution for repeated clicking. Clicking ads freely because you registered the device is still dangerous.

## The rest of the story

Around the same time, Apps in Toss tightened its own ad abuse policy. As I noted in the [September policy roundup](/posts/toss-policy-changes/), the platform's framing is that "abnormally inflated ad impressions have been reducing the opportunity and revenue of mini apps that operate normally." My incident was small and carried no malice, but I cannot pretend I was not standing in the direction that sentence points.

A month of zero revenue on the Play side is also why I could only publish [the Apps in Toss ad numbers](/posts/toss-ad-revenue-first-month/). Those other figures will go into the next report.

The first thing to do when adding ads is not to place them attractively. It is to block the requests coming from your own devices. I learned that at the cost of a month.

My apps are on [Google Play and Apps in Toss](/posts/apps-in-toss-launch/), and some can be [played right in the browser](/play/). Updates go out here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> This post describes what actually happened on my account and my own inferences about it. Platforms do not disclose the precise basis for an invalid-traffic determination, so the same symptom will not always have the same cause.
{: .prompt-info }
