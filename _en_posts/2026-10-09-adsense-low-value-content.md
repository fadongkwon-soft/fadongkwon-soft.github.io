---
title: AdSense Rejected My Site for Low-Value Content — 600 of 954 Sitemap URLs Were Empty Pages
description: AdSense turned my site down again for low-value content. I blamed 78 tarot posts, but counting my own sitemap showed 603 of 954 submitted URLs were tag lists and redirect screens. What I found, what I fixed, and what I chose not to do
date: 2026-10-09 17:40:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/adsense-low-value-content/
alt_url: /ko/posts/adsense-low-value-content/
tags: [solo developer, dev log]
---

On October 5 another rejection arrived from AdSense. The reason: **low-value content**. This time I had also used up my review requests, so the notice said **I could not ask for another review until October 12**.

Honestly, my first reaction was to bolt a different ad network onto the site instead. In the end I didn't. I took the site apart from the top instead, and a number I never expected came out of it.

## The first suspect: 78 tarot posts published in one day

Besides the dev log, this blog has a tarot dictionary that covers all 78 cards, one post per card. Nearly all 78 went up **on a single day, August 29**, and they all share the same structure (introduction → upright and reversed → readings by situation → FAQ → cards to read alongside).

Each interpretation is my own writing, but dozens of identically structured posts appearing on one day can look like **mass-produced content** from the outside. I assumed that was the cause.

Then something didn't add up. The tarot posts had **already been off the home feed since late August**. The site was rejected in that state. Hiding them from the home page clearly wasn't enough — so what was the reviewer looking at besides the home page?

## Outside the home page, it was still a tarot site

I opened everything outside the home feed, one page at a time.

- The **home description** (the line shown in search results and share cards) started with "A tarot card dictionary for all 78 cards, …".
- **Five of the ten trending tags** on the right of every Korean page were tarot tags — tarot, tarot card, Minor Arcana and so on.
- The **Archives** and **Categories** tabs still listed all 78 tarot posts.
- The left menu had **TAROT** as a top-level item right after HOME, ABOUT, APPS and PLAY.

The home feed said "dev blog", and everything else said "tarot site".

## The really big number was in the sitemap

Next I downloaded the sitemap I submit to Google (`sitemap.xml`) and counted the URLs by type.

| Type | Count |
| --- | --- |
| Posts (150 Korean + 150 English) | 300 |
| **Tag list pages** (389 Korean + 143 English) | **532** |
| **Screens that hand off to a store** (36 Toss + 35 Google Play) | **71** |
| Category lists | 32 |
| Other (home, about, apps and so on) | 19 |
| **Total** | **954** |

Of the 954 pages I had handed Google as "the pages of my site", **603 had no content of their own**.

- A **tag list** is a page that just lines up post titles. Because every tarot card post carried its own card-name tag (King of Pentacles, for example), there were hundreds of **tag pages holding a single post**. There were more tags than posts.
- A **hand-off screen** is the page you pass through after scanning an Instagram QR code or tapping "Install". On a phone it jumps straight to Toss or Google Play; on a PC it only shows a QR code. There is nothing to read.

The blog theme (Jekyll Chirpy) and its sitemap plugin generate these by default, so I had never looked at them. They may have been **a much bigger signal than the 78 tarot posts**.

## What I fixed

**1. Pages with no content are out of search.**
I added `noindex` to the 532 tag lists and the 71 hand-off screens and removed them from the sitemap. The pages still exist, so tapping a tag at the top of a post or scanning a QR code works as before. The sitemap went from **954 URLs to 353**.

**2. Tarot and app introductions are reached only through their hubs.**
Tarot card posts and app introduction posts are gone from the home feed, Archives, RSS, the right-hand panels and the related posts under other articles. Tarot posts are now reached from the tarot dictionary index, and app introductions from the app list pages. Every list reads one setting (`hub_only_categories: [Tarot, Products]`), so new posts need no special handling. The home feed went from **8 pages to 4**, and everything left on it is a dev log.

**3. The site now introduces itself differently.**
The home description now opens with "Honest notes from shipping apps alone after work", and TAROT and TAGS are gone from the left menu. The tarot dictionary stays; it is linked from next to the tarot apps on the app list and from the About page, as "the card-by-card companion to my tarot apps". The trending tags now start with solo developer, dev log and Apps in Toss.

**4. I merged a post nothing linked to.**
After step 2 one post was stranded. The app list links one introduction per app, but Hangul Monsters had a second, short "now on Toss too" post besides its main one. It mostly repeated the main post, so I folded it in and pointed the old address at the main post.

## What I chose not to do

**Switching to another ad network.** Some ad networks barely review sites at all, but most of them serve pop-ups or ads that redirect you to another page. This site is also the developer site of a [kids' learning app that Google Play marked "Teacher Approved"](/posts/math-monsters-teacher-approved/). A parent or teacher arriving from the app and getting hit by that kind of ad would cost far more than the ad revenue.

**Applying again with the old github.io address.** This blog used to live at `fadongkwon-soft.github.io`, and I wondered about applying with that. But every page there now forwards to `fadongkwon.com`, so the reviewer would see the same site — and AdSense needs `ads.txt` at the top of the domain, which for github.io belongs to GitHub.

## Where I got lost in Search Console

The **Manual actions** screen in Search Console mentions requesting a review, so I thought I could do something there. It said "No issues detected". Manual actions are for lifting penalties applied by hand in Google Search; with no penalty there is nothing to submit. It is **a separate system from the AdSense review**.

The bigger trap was elsewhere: the property I was looking at was the old `github.io` address. Since every page there forwards to the new domain, zero indexed pages is normal and there is almost no data. I added `fadongkwon.com` as a **domain property** and submitted the sitemap. At first it said "Couldn't fetch", though the file itself was fine, and the next day it turned into **Success · 353 discovered pages** — exactly the cleaned-up count.

## What's left

On October 12 I'll request another review. Only the result will tell whether these were the real causes. Approved or not, I'll add the outcome to the top of this post.

The biggest lesson: **the posts I wrote are not the whole site.** Every page the theme and plugins generate on their own is, to Google, "a page of this site". If you run a blog, open your own sitemap at least once and count what is in it.

My apps are on [Games](/games/) and [Apps](/apps/), and some of them [run right in the browser](/play/). I post updates here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> AdSense does not give a detailed reason for a rejection. The analysis in this post is my own reading of my own site, and a different site rejected for the same reason may have different causes.
{: .prompt-info }
