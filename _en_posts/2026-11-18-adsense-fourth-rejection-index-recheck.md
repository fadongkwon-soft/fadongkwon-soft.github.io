---
title: AdSense Rejection Number Four, and an Index Recount — I Applied Before Meeting My Own Conditions
description: On November 3 I decided to hold off on reapplying because my conditions were not met. Then I reapplied anyway, and on November 16 it came back rejected for the same reason, "low value content." This post pays off two promises from earlier posts at once, to report the next result and to fill in the same table again in two to three weeks. I remeasured index counts and search clicks for October 25, November 3 and today the same way, recounted the post mix, and wrote down what applying before meeting the conditions actually showed
image:
  path: /assets/img/20261118_adsense-fourth-rejection-index-recheck/cover-en.png
  alt: "AdSense rejection number four and an index recount"
date: 2026-11-18 23:29:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/adsense-fourth-rejection-index-recheck/
alt_url: /ko/posts/adsense-fourth-rejection-index-recheck/
tags: [seo, solo developer, dev log]
---

> **Update, November 19** — The appeal for the same publisher account was rejected on November 19. With the account closed, applying for AdSense on this site is now impossible regardless of any conditions. The reapplication conditions below no longer mean anything; the wrap-up is in [the follow-up post](/posts/google-ads-appeal-rejected/).
{: .prompt-info }

At the end of [the third rejection post](/posts/adsense-rejected-again/) I wrote that I would write up the next result, and at the end of [the index gap post](/posts/search-console-index-gap/) I wrote that I would fill in the same table again in two to three weeks. This post pays off both promises at once.

The result first. **The fourth application was rejected too.** On November 16 an email arrived titled "You need to fix issues found on your site," and the reason in the console was the same as the previous three: **low value content**.

And there is something I have to say plainly. This application was **filed before I had met the conditions I set for myself**.

## I decided to wait, then applied anyway

In the October 25 post I said I would stop the two-week resubmission loop and set the next request by conditions, not by date. On November 3, after confirming the cooldown had ended, I pinned those conditions down as numbers.

1. Search Console clicks of **at least 10 a day for two consecutive weeks**, with Korean pages (`/ko/`) making up at least half
2. **More devlog posts than app introduction posts**

The November 3 measurement fell short on both. Search clicks were 37 over 28 days, one to three a day, and there were 71 devlog posts against 88 app introductions. So that day I held off.

Then, **around November 10**, I applied again. I did not write the date down, so I do not know the exact day. The conditions were still unmet. I skipped past the bar I had announced in public myself. I will not write a long excuse for why. The result already said whether the call was right.

## The rejection email and the reason

This email's subject was "You need to fix issues found on your site." As with the third rejection, the body gave no specific reason and only pointed to the Sites page. The reason in the console was the same "low value content" as rounds one, two and three.

| Round | Result | Reason |
|---|---|---|
| 1 | August | Low value content |
| 2 | October 5 | Low value content |
| 3 | Decided October 23 | Low value content |
| 4 | November 16 | Low value content |

Four in a row with the same reason at least makes this one reason unambiguous. The technical items, the sitemap, `noindex`, the home page layout, were cleaned up after round two. What remains are the two things [the last post](/posts/adsense-rejected-again/) filed under "hard to change": the character of the site and search traffic. Those are the two things to measure this time.

## Remeasuring the index, the same way three times

On October 25 I looked at the page indexing report in the Search Console UI. Since October 28 I have used a script that checks each sitemap URL through the URL Inspection API. On November 3 and today I ran the same script over only the Korean (`/ko/`) URLs in the sitemap. These are read-only calls; I did not submit any indexing requests.

| Item | 10/25 | 11/3 | 11/18 |
|---|---:|---:|---:|
| Method | Console report | URL Inspection API | URL Inspection API |
| Korean URLs in sitemap | — | 267 | 302 |
| Indexed | — | **65 (24%)** | **213 (71%)** |
| Discovered, currently not indexed | 157 (of 200 Korean posts) | 145 | 64 |
| URL is unknown to Google | — | 56 | 25 |
| Crawled, currently not indexed | — | 1 | 0 |
| Posts (`/ko/posts/`) indexed | at most 43 of 200 | 50 of 240 | 186 of 275 |

The October 25 column comes from the console report, not a per-URL check. That report showed 157 of 200 Korean posts (79%) as "Discovered, currently not indexed." The first full per-URL check, on October 28, found 44 of 223 Korean posts indexed.

In the two weeks from November 3 to today, indexed Korean URLs went from 65 to 213, from 24% to 71%. "Discovered, currently not indexed" fell from 145 to 64. The problem the index gap post worried about, Google discovering Korean URLs but never picking them up, has largely eased. What I cannot tell is whether the increase came from the indexing requests or from Google crawling on its own over time. I never split requested and unrequested URLs into groups to compare.

What I did in between followed the plan in [the index gap post](/posts/search-console-index-gap/). I kept the URL structure, put a Korean/English pair link on the first line of every post, and submitted indexing requests starting with unindexed Korean posts. There is no API for the request button, so it has to be clicked one URL at a time in the console, and the quota runs out at around 25 a day. The request log I have kept since October 28 shows 639 successful requests covering 391 distinct URLs. Some URLs were requested more than once, which is why the two numbers differ.

## Remeasuring search clicks

More pages in the index is one thing; whether people come in is another. Performance data lags two to three days, so the latest day in today's query is November 16.

| Period (28 days) | Measured | Total clicks | `/ko/` clicks | Impressions |
|---|---|---:|---:|---:|
| 10/5–10/23 (19 days, from property creation) | 10/25 | 22 | not checked | 3,730 |
| 10/5–11/1 | 11/3 | 37 | 13 | 6,367 |
| 10/20–11/16 | 11/18 | 46 | 23 | 8,375 |

The November 3 `/ko/` value comes from querying the same period again today through the API. The October 25 post looked only at countries, so Korean page clicks were not counted separately.

Clicks over 28 days went from 22 to 37 to 46, and Korean pages now make up half. But the condition is **10 a day, two weeks in a row**. Day by day it looks like this.

| Date | 11/3 | 11/4 | 11/5 | 11/6 | 11/7 | 11/8 | 11/9 | 11/10 | 11/11 | 11/12 | 11/13 | 11/14 | 11/15 | 11/16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Clicks | 2 | 2 | 5 | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 1 | 1 | 0 | 3 |

That is 23 clicks in the last 14 days, 1.6 a day. Since October 5 there has not been a single day above 10; the best day had 5. Impressions grew from 50–100 a day in early October to 300–400 a day by mid-November, so the site shows up in results but does not get clicked.

## Recounting the post mix

The second condition is post counts. I recounted using the first category in each `_posts` front matter, excluding the devlog published alongside this one today.

| Kind | 10/25 | 11/3 | 11/18 |
|---|---:|---:|---:|
| Devlog | 56 | 71 | 77 |
| App introductions | 63 | 88 | 118 |
| Tarot card dictionary | 78 | 78 | 78 |
| Other | 3 | — | 3 |
| Total | 200 | — | 276 |

I did not record the total or "other" on November 3, so those cells are blank.

The gap did not shrink; it grew. A 17-post gap on November 3 is now 41. I shipped a run of new apps in November, and under the one-post-per-app rule, introductions grew by 30. Devlogs grew by 6 over the same period. As long as I keep shipping at this pace, the day devlogs overtake introductions will not come.

## What applying early actually showed

This rejection taught me nothing new as such. That is exactly why some things are clearer now.

**1. What changed while I waited was not enough.** Indexing clearly improved between November 3 and the application. But search clicks stayed at one or two a day, and the post mix tilted further toward app introductions. The site the reviewers saw was probably the same kind of site it was on November 3.

**2. The conditions had a reason behind them.** After the third rejection, the guidance in the console included a criterion about "real user interest at a level that supports commercial ad partnerships." That is where the search click condition came from. If I ignored that bar myself and the result was the same, that adds a reason to keep it, not a reason to doubt it.

**3. I did not write the application date down.** It sounds minor, but it was the most awkward part of writing this post. Without the date I cannot reconstruct exactly what the site looked like when it was reviewed. I cannot recount index numbers or post counts as of that day. From now on, when I apply for any outside review, I will log the date along with one line of that day's metrics.

One more note. On November 18, two days after the rejection, the app advertising account that shares this site's publisher account was disabled over invalid traffic. While the account is disabled, the site cannot carry ads either. It is unrelated to the site's content, but it means that right now there is no point talking about another AdSense review at all.

## The policy stays

To sum up:

- The fourth application, filed around November 10, was rejected on November 16 for "low value content." It went in without meeting either of my two conditions.
- Indexed Korean URLs went from 65 on November 3 to 213 today. Much of the problem the index gap post worried about has eased.
- Search clicks are 46 over 28 days, one or two a day, far from the 10 a day in the condition.
- 77 devlogs, 118 app introductions. The gap widened from 17 to 41.

The policy does not change. **I will not apply again until the conditions are met**: search clicks above 10 a day for two straight weeks, and more devlogs than app introductions. Until then I will keep repeating the same measurement the same way and keep writing as I have, regardless of AdSense. What this round taught me is not that the policy was wrong, but that the result stayed the same because I did not follow it.

My apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be played [right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> AdSense does not give specific rejection reasons. The reading in this post is my own estimate from my site's Search Console numbers and may not apply to other sites.
{: .prompt-info }
