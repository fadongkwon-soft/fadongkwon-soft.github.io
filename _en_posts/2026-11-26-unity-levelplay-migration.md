---
title: "One Week After AdMob: Migrating 100+ Android Apps to Unity LevelPlay + Unity Ads"
description: "One week after Google rejected our publisher appeal, we migrated our Android wrapper to Unity LevelPlay mediation and Unity Ads. From 2 pilot apps to 7 new launches and 20 existing apps, here is our checklist covering SDK isolation, R8 verification, app-ads.txt, and Play Data Safety."
image:
  path: /assets/img/20261126_unity-levelplay-migration/cover.png
  alt: "Unity LevelPlay and Unity Ads migration summary"
date: 2026-11-26 01:05:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/unity-levelplay-migration/
permalink: /posts/unity-levelplay-migration/
tags: [ads, android, monetization, indiedev, devlog]
---

On November 19, [Google rejected our publisher account appeal](/posts/google-ads-appeal-rejected/), halting ad monetization across more than 100 Android apps on Google Play overnight. The path forward was clear: leave Google's publisher ecosystem behind and migrate to a new ad network.

Over the past week, we adopted **Unity LevelPlay mediation + Unity Ads**, starting with two pilot apps (`breakout` and `gonu`), followed by seven unreleased apps submitted directly with LevelPlay, and two rollout batches covering 20 existing live apps. Here is how we structured the migration to avoid breaking a 120-flavor monorepo.

## 1. One Properties File as the Network Switch

Our Android wrapper (`apps-in-toss-games/android/app`) builds over 120 product flavors. Branching by app name in Kotlin would quickly become unmaintainable, so we made the **presence of a single config file** the switch:

- If `android/levelplay-<id>.properties` exists, Gradle automatically wires that flavor to the `adsLevelPlay` source set.
- `levelplay-*.properties` is gitignored so keys never touch the repository.
- Both `AdManager.kt` and `ConsentManager.kt` preserve the exact same public contract as `adsReal`. `MainActivity.kt`, `MiniBridge.kt`, and all 100+ web games stay completely unaware of which ad SDK sits underneath.

Apps in Toss builds use Toss IAA, so none of those bundles were touched.

## 2. Stripping Google Mobile Ads & UMP, Verified via R8

Leaving Google Mobile Ads or `com.google.android.gms.ads.APPLICATION_ID` behind in manifests only adds bloat and confusion.

- We moved the UMP `ConsentManager.kt` into `src/adsUmp/` so only legacy flavors pull it in.
- `src/adsLevelPlay/AndroidManifest.xml` omits `APPLICATION_ID` entirely and declares only `com.google.android.gms.permission.AD_ID`.
- Dependencies are scoped to `mediation-sdk:9.8.0` and `unityads-adapter:5.17.0` (bundling Unity Ads SDK 4.22.0).

Instead of assuming the separation worked, we counted classes directly in R8's `mapping.txt` after release builds:

| Release Flavor | Google Mobile Ads (excl. identifier) | UMP | LevelPlay | Unity Ads | Manifest `APPLICATION_ID` |
|---|---:|---:|---:|---:|---|
| `breakoutRelease` (pilot) | 0 | 0 | 27 | 870 | None |
| `gonuRelease` (pilot) | 0 | 0 | 27 | 873 | None |
| `reactionRelease` (legacy control) | 376 | 6 | 0 | 0 | Present |
| `mathMonstersRelease` (kids `adsStub`) | 0 | 0 | 0 | 0 | None |

Kids apps (`adsStub`) continue to ship with zero ad SDK classes.

## 3. Seven Safeguards Built Into the New Wrapper

Switching ad networks does not make invalid traffic disappear—new accounts start with low trust and need tighter guardrails from day one:

1. **Untrusted environment gate (`AdSafety`)**: Debuggable builds, emulators, rooted devices, and installs outside `com.android.vending` skip `LevelPlay.init()` completely (zero ad requests).
2. **Ad warm-up window (`AdWarmupStore`)**: After a fresh install, `LevelPlay.init()` waits until the user accumulates 3 minutes (`180,000ms`) of foreground time and either launches a second session or completes one round. Until then, the banner container stays collapsed (`GONE`).
3. **Async reward gate (`RewardedOutcomeGate`)**: Even if `onAdRewarded` and `onAdClosed` arrive out of order, a 600ms grace window after close ensures the web layer receives exactly one `"earned"` or `"dismissed"` callback.
4. **Auto-refresh pause & exponential backoff**: Daily cap blocks (20/day), in-gameplay banner hiding, and host pause call `pauseAutoRefresh()`. Load failures back off exponentially up to 64 seconds.
5. **Privacy flags before init**: GDPR, CCPA, and COPPA metadata flags are applied immediately before `LevelPlay.init()`.
6. **Local ad telemetry (`AdLocalStats`)**: Daily counts per format (banner, interstitial, rewarded) are stored locally for 30 days for quick sanity checks.
7. **Release gate (`checkAdIds`)**: Fails release builds if keys or unit IDs are blank, malformed, or accidentally contain Google test IDs or AdMob IDs.

## 4. Device Verification Catch

On a Galaxy S23 Ultra over wireless ADB, `IntegrationHelper` reported `IronSource 9.8.0 VERIFIED` and `UnityAds 4.22.0 / Adapter 5.17.0 VERIFIED`. Testing on real hardware also caught an edge case where returning from a Play Games Services sign-in dialog skipped banner attachment—we fixed that immediately in `onHostResume()`. As soon as a live ad rendered on the test banner, we verified gameplay hiding without clicking it and uninstalled the debug build to avoid polluting live impressions.

## 5. Non-Code Checklist: Policy & Store Forms

- **`app-ads.txt`**: Added **162 Authorized Sellers lines** from Unity Cloud Monetization plus `ownerdomain=fadongkwon.com` to the site root.
- **Privacy policy**: Added Unity's privacy policy link to `https://fadongkwon.com/privacy/`.
- **Play Data Safety CSV**: Updated existing location, app interaction, and device ID disclosures with analytics and fraud-prevention purposes, and added *Other actions* and *Diagnostics*.

## 6. Rollout Order

After shipping the two pilots (`breakout v1.2.2`, `gonu v1.0.4`), we prioritized **7 unreleased apps** so they went through first-time Play review with LevelPlay already baked in (6 of the 7 were approved on November 24). From there, we started migrating existing live apps in batches of 10—20 apps converted so far, with the rest following the same properties-file switch.
