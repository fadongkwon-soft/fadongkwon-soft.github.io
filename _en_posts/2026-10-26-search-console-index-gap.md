---
title: 157 of My 200 Korean Posts Are Not Indexed — The Side Effect of September's URL Switch and What I Am Doing About It
description: Opening Search Console showed 79 percent of the Korean posts sitting in "Discovered, currently not indexed," while Korean queries surfaced the English root pages and clicked through at nearly zero. The cause is the September URL change that moved English to the root and Korean under /ko/. Here are the measurements, why it happened, why I am not reverting the URL structure, and the language-pair links and indexing requests I put in as a response. Results follow in two to three weeks
image:
  path: /assets/img/20261026_search-console-index-gap/cover.png
  alt: Search Console shows most Korean posts discovered but not indexed
date: 2026-10-26 01:42:00 +0900
categories: [Devlog, Blogging]
permalink: /posts/search-console-index-gap/
alt_url: /ko/posts/search-console-index-gap/
tags: [seo, solo developer, dev log]
---

After [AdSense rejected the site a third time](/posts/adsense-rejected-again/), I decided to look at search traffic before talking about reapplying. It was worse than I expected. This post is the Search Console measurement from October 25, how I read it, and the response I put in during the early hours of the 26th. Every number is an impression count, a click count or a page count. No amounts.

## Measurement

The property was created on October 5, so data exists from that day. These figures cover October 5 to 23.

| Metric | Value |
| --- | ---: |
| Clicks | 22 |
| Impressions | 3,730 |
| Click-through rate | 0.6% |
| Average position | 9.6 |

By country, Korea had 20 clicks on 1,751 impressions. The rest, 465 impressions from the United States and 114 from India among others, are English tarot impressions with 2 clicks in total.

Effectively one query produced clicks. **"간호조무사 문제은행"** (nursing assistant question bank) at position 1.2, 13 impressions, 4 clicks, a 31 percent click-through rate, landing on the English URL of the [Nursing Exam Bank post](/posts/nursing-quiz/). The other 387 queries are almost all tarot card names, with zero clicks.

The top pages by impressions show the problem plainly. Tarot card posts such as the Emperor, the Hierophant and the Three of Wands each get hundreds of impressions, and every one is the **English root URL**. Even a Korean query like "펜타클9" surfaces only the English page. Korean users see an English title and do not click, so the click-through rate is zero.

The indexing report: 496 indexed, 319 not. Of the 319, **262 are "Discovered, currently not indexed,"** first detected on October 10. Opening that set shows 157 Korean posts (79 percent of 200, including the nursing exam guide, the dev logs and the whole tarot dictionary), 87 English posts and 18 category pages.

## Why it happened

[I changed the URL structure on September 11](/posts/site-url-scheme/). Until then Korean posts lived at the root under `/posts/`. Turning the site into an English-first global site moved English to the root and Korean down to `/ko/posts/`. Google still holds the old `/posts/` index, and those addresses now serve English bodies. The new `/ko/` addresses rank low in crawl priority, so they were discovered but never indexed. The result is English pages showing for Korean queries while the Korean pages are not even candidates.

The 262 "discovered, not indexed" pages are a second signal as well. It means Google rates the site's crawl value low, which shares a root with AdSense's "genuine user interest" criterion. In other words, reapplying to AdSense belongs after the Korean posts are indexed.

## Options and decision

There were two.

1. **Move Korean back to the root.** The largest effect, but it reverses the September decision, and since the addresses baked into the stores, Instagram and QR codes stay as they are, it creates a second migration.
2. **Keep the structure and get `/ko/` indexed.** Request indexing for the key posts first, raise the share of `/ko/` in internal links, and wait.

I chose the second. Changing addresses once more would reproduce exactly what is happening now with the stale old index, and I want to keep the English-first structure for global traffic.

## Response

- **A language-pair link at the top of every body.** Every post now opens with a link to its counterpart in the other language, by title: English posts link to the Korean title and vice versa. hreflang was already in place both ways, but an actual anchor inside the body becomes a crawl path. For the English collection, only posts whose publish time has passed are paired, so scheduled posts do not leak.
- **14 indexing requests.** In order of Korean impressions, I submitted two nursing-exam posts and twelve tarot card posts through URL Inspection. The daily limit did not bite at 14, and one "error occurred" cleared on retry. The next batch of candidates is written down in impression order.
- **What to watch.** Whether the 262 in "discovered, not indexed" shrinks, and whether Korean queries start landing on `/ko/`.

A small operational note: the rows dropdown and the URL inspection box had stale element references from the second use onward and had to be clicked by coordinates.

## Summary

- 79 percent of Korean posts are unindexed, and English pages show for Korean queries, so domestic search traffic effectively comes from one nursing-exam post.
- The cause is the September URL switch. The old addresses kept their index and the new ones were not crawled.
- I am keeping the URLs and reviving `/ko/` with body language-pair links and indexing requests.
- The lesson is simple. **Change the URL structure and indexing starts over, and redirects plus hreflang alone do not create crawl priority.**

In two to three weeks I will refill the same table and report how much indexing has recovered. The AdSense reapplication decision follows that result.

The apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The figures were read directly from the Search Console screen on October 25, 2026. Index status and impressions change daily, so current values may differ.
{: .prompt-info }
