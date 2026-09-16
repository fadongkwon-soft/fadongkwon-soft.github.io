---
title: "Traffic Never Comes Through One Door — Opening 54 Paths on Instagram and YouTube"
description: "I had built 29 apps and still left the road to them blocked. Store links were missing from 24 of 27 Instagram posts and 20 of 27 YouTube videos, and the Toss link appeared in none of the 54. While stamping three link lines out of my app registry, I found that the Shorts I had only made to fill a store listing field had quietly collected 1,939 views"
date: 2026-09-17 01:30:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/traffic-paths/
alt_url: /ko/posts/traffic-paths/
image:
  path: /assets/img/20260917_traffic-paths/cover.png
  alt: Store links missing across Instagram and YouTube
tags: [youtube, instagram, marketing, solo developer, dev log]
---

I am at 29 apps now. There are two shelves: Google Play and Toss. But looking at the last five weeks of numbers, the bottleneck was never the number of apps. It was **the road people take to reach them**.

So before building one more app, I knocked on the doors I assumed were already open. Most of them were shut.

## The audit — the doors were shut

I opened all 27 [Instagram](https://www.instagram.com/fadongkwon.soft/) posts and all 27 [YouTube](https://www.youtube.com/@FadongkwonSoft) videos and read them.

| Channel | Had a link | Had none |
| --- | --- | --- |
| Instagram, 27 posts | 3 | 24 (one had no caption at all) |
| YouTube, 27 videos | 7 (mostly a single Play line) | 20 |
| Toss mini app address | 0 | all 54 |

The cause was not laziness. It was the format. These are the rules I had written down for myself:

- Instagram caption: intro + CTA ("scan the QR on the last card to reach the store") + hashtags
- Shorts description: one Korean line + one English line + four hashtags

**Neither format has a slot for a link.** The better I followed my own rules, the more reliably the link fell out. That is why twenty-nine launches never caught it. I did it by the book every time.

## Three lines

The fix itself is simple. Three lines at the end of the post, right before the hashtags.

```
Google Play: https://play.google.com/store/apps/details?id=com.fadongkwon.snake
토스 미니앱 / Toss: https://fadongkwon.com/toss/snake/
홈페이지 / Homepage: https://fadongkwon.com
```

Only Toss goes through my own site. **A Toss mini app has no public web address** — it opens inside the Toss app and nowhere else. The `fadongkwon.com/toss/<app>` page was already doing that job: on a phone it hands you to Toss, on a desktop it explains where to go. So the site becomes the hub that joins the two shelves.

I did not type those lines by hand. Typing the same block fifty-odd times is exactly where typos come from, and I recently shipped a typo to eight apps by assembling release notes by hand. Instead I read the package name and slug from my app registry, stamped out the blocks, and pasted the generated file.

YouTube is done: all 27, re-read on the public pages to confirm. Instagram stopped at 6. Editing post after post from one account reads as a risk signal on that side, so the remaining 21 blocks sit in a file and go in by hand, spaced out.

⚠️ A URL in an Instagram caption is **plain text you cannot tap**. I still put it there. It tells people where the app lives; the thing that actually gets tapped is still the QR on the last card.

## Then I looked at the view counts

The Shorts existed for one reason: **to fill the "video URL" field on a Play store listing.** The point was the preview that plays on the store page, not building an audience on YouTube. I have never promoted the channel.

The 27 videos add up to **1,939 views**. Ten of them passed 100.

| Video | Views |
| --- | --- |
| Memory Cards | 215 |
| Sudoku | 211 |
| Number Slide | 193 |
| Minesweeper | 188 |
| Pixel Pong · Nonogram | 180 each |
| Snake | 152 |
| Reaction Challenge | 148 |
| Hangul Monsters | 138 |
| Brick Breaker | 125 |
| The other 17 | 209 total |

The spread is the interesting part. On September 10 I uploaded four videos on the same day in the same format, and they split like this:

- Number Slide 193 · Minesweeper 188
- 2048 6 · Gomoku 1

Same channel, same length, same title pattern, same hashtags. From where I sit, Shorts distribution behaves like a lottery. But you still have to buy tickets to scratch them. Without twenty-seven uploads sitting there, there is no 1,939 either. **A chore done to fill a listing field had quietly opened a traffic path.**

Which is why putting links in the descriptions was not late housekeeping but the right thing to do today. Across 1,939 plays, nobody watching could find the answer to "where do I get this game" anywhere on the screen.

## There are paths inside the apps too

Incoming roads are not the only roads. Someone already inside one of my apps moving to the next one is traffic too.

The "more apps" list inside each app had only Korean and English. Someone opening an app in Japanese saw Korean names. I widened it to nine languages: app names are pulled automatically from the translation each game actually uses, and the one-line descriptions were newly translated. All 27 apps on that list now follow the same rule.

## What is left

- 21 Instagram posts — apply the saved blocks, spaced out
- 25 gameplay videos as Reels — Instagram still has no video at all
- Watch what changes now that the descriptions carry links

The conclusion lands where it always does. Before adding a new shelf, it is faster to put up a sign in front of the doors that are already open.
