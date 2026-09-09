---
title: Why a 100dvh Container Still Scrolls — The targetSdk 35+ Edge-to-Edge Trap
description: Fifteen apps reported the same thing at once: the screen shifts a few pixels up and down. The cause was the edge-to-edge layout that targetSdk 35 and above enforces. The body takes padding equal to the safe-area insets, and a container inside it set to 100dvh counts those insets a second time, overflowing the document. The diagnosis and the one-line fix
date: 2026-09-15 20:00:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/edge-to-edge-scroll/
alt_url: /posts/edge-to-edge-scroll/
image:
  path: /assets/img/20260915_edge-to-edge/cover.png
  alt: Diagram of safe-area insets being counted twice in a 100dvh layout
tags: [android, webview, css, apps in toss, minigame, dev log]
---

I was checking a mini game on my phone when I noticed something odd. Dragging a finger across the game screen shifted the whole page up and down by a few pixels. There was no reason for a scrollbar to exist here — it is a full-screen game, and the container height is set to `100dvh`.

It was not one app either. **All fifteen apps had the same symptom.**

## The symptom

- On a game built to fill the screen, dragging a finger scrolls the document by a few pixels.
- The amount differs by device. Some barely move; others shift noticeably.
- It does not reproduce in a browser, desktop or mobile. Only in the app-wrapped builds.
- Not fatal to gameplay, but in drag-controlled games the board wobbles and inputs land off target.

Those last two facts pointed the way. Something that **varies by device** was getting into the calculation, and only inside the app.

## The cause: the insets were being counted twice

Android enforces **edge-to-edge layout from targetSdk 35**. Your app draws all the way under the status bar and the navigation bar, and in exchange the responsibility for avoiding those regions moves to you. The WebView follows suit and reports real values for `env(safe-area-inset-*)`.

Our shared CSS looked like this:

```css
body {
  padding: env(safe-area-inset-top) env(safe-area-inset-right)
           env(safe-area-inset-bottom) env(safe-area-inset-left);
}

#app {
  height: 100dvh;   /* ← the problem */
}
```

Read separately, both rules are correct. Pad the `body` by the insets so content does not hide under the status bar, then fill the screen height with `#app` inside it.

The problem is what happens **together**. `100dvh` is the full screen height, insets *included*. But `#app` starts at a position already pushed inward by the insets. So the document height becomes:

```
body top padding + 100dvh + body bottom padding
= inset(top) + screen height + inset(bottom)
= screen height + total insets
```

The document overflows by exactly the sum of the insets. That was the few pixels of scroll. It also explains why the amount differed by device — inset sizes differ. And why browsers never reproduced it: in a normal browser tab the insets are 0, and counting 0 twice is still 0.

## The fix

Subtract the insets back out of `100dvh`.

```css
#app {
  height: calc(100dvh
               - var(--banner-h, 0px)
               - env(safe-area-inset-top, 0px)
               - env(safe-area-inset-bottom, 0px));
  display: flex;
  flex-direction: column;
}
```

`--banner-h` is a separate concern. In environments like Apps in Toss, where the ad banner overlays the page, the bridge writes the banner height into that variable and the screen shrinks accordingly. The Android wrapper leaves it at 0 because its native layout already positions the WebView above the banner. The same CSS has to behave differently in the two environments, which is why it is a variable.

You **must** give `env()` a `0px` fallback. In an environment without inset support, `env(safe-area-inset-top)` resolves to nothing rather than to a value, which makes the entire `calc()` invalid and throws away the height declaration altogether. With a second argument it computes as 0 instead.

Games with platform-specific overrides needed the same treatment, since the banner default differs on Apps in Toss:

```css
.platform-toss #app {
  height: calc(100dvh - var(--banner-h, 56px)
               - env(safe-area-inset-top, 0px)
               - env(safe-area-inset-bottom, 0px));
}
```

One shared stylesheet, plus the 15 games that carried this override, all changed together.

## Why it hit fifteen apps at once

The reason the same bug existed in fifteen apps is simple: every game shares the CSS in the common package. That cuts both ways, and the good side showed up immediately. Once the cause was found, one line in the shared stylesheet fixed most of the apps at once, and only the ones with their own override needed separate attention.

**A bug in shared code multiplies by the number of apps, but so does the fix.** Had I built those fifteen separately, I would have gotten it wrong fifteen different ways and had to fix each one differently.

## Takeaways

To avoid the same trap:

- `100dvh` is the screen height **with insets included**. Using it inside an element that already has safe-area padding guarantees double counting.
- Handle insets at **exactly one layer**. If the `body` handles them with padding, do not use bare `100dvh` anywhere inside it.
- Always pass a fallback to `env()`. Without one, `calc()` becomes invalid on unsupported environments.
- After raising targetSdk to 35 or above, **drag up and down on a real device.** A few pixels of scroll is invisible in an emulator or a browser.

That last point stings the most. I checked that features worked and moved on, and the bug sat in fifteen apps for weeks.

My apps are on [Google Play and Apps in Toss](/en/posts/apps-in-toss-launch/), and some can be [played right in the browser](/en/play/). Updates go out here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
