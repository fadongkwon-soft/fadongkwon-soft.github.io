---
title: AdSense Rejected Again — I Fixed the Sitemap and Wrote 51 More Posts, and the Result Was the Same
description: After the October 5 "low value content" rejection, I cut the sitemap from 954 URLs to 353, cleaned up the home page, menu and site description, and added 51 posts. The October 12 re-request was rejected again, and this time the email did not even name a reason. What changed in between, why the outcome could be the same anyway, what causes remain, and why I am stopping the two-week resubmission loop
image:
  path: /assets/img/20261025_adsense-rejected-again/cover.png
  alt: Google AdSense rejection email for the third time
date: 2026-10-25 10:25:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/adsense-rejected-again/
alt_url: /ko/posts/adsense-rejected-again/
tags: [solo developer, dev log]
---

At the end of [the last post](/posts/adsense-low-value-content/) I wrote that I would re-request on October 12 and add the result. The result is in. **Rejected again.**

This email is a little different from the last one. Last time there was a reason, "low value content." This time it only says this:

> We reviewed your site and unfortunately it is not ready to show ads at this time. There are issues to resolve before ads can appear on your site. See the Sites page in your account for details.

The reason is in the console, not the email. Since the first application in August, that is **three resubmissions, three rejections.**

## What changed in between

Everything I did between the last rejection (October 5) and this request (October 12) is in [the previous post](/posts/adsense-low-value-content/). In short:

- Sitemap URLs **954 → 353.** I added `noindex` to 532 tag pages and 71 store hand-off pages and removed them from the sitemap.
- Tarot card posts and app announcement posts were taken out of the home feed, archives, RSS and related-posts lists, reachable only from their own hub pages. The home page now shows only dev logs.
- The site description and the left menu dropped tarot, and the site now introduces itself as "a record of what I learn building and shipping apps alone after work."
- I registered `fadongkwon.com` as a domain property in Search Console and submitted the sitemap. Discovered pages: 353, exactly the cleaned-up count.

And since that request, **the post count grew by 51** (including today's posts). The Korean post count went from 149 on October 9 to 200 now. The second batch of five board games, the retro five retrospective, the CrazyGames rejections and shutdown, the Japanese store listing rewrite, week one of the 1-won promotion, D+1 and D+7 checks on 14 games, the 50-app workspace limit, the first hub app launch. Most are dev logs over 2,000 characters, each with an English edition published alongside.

## What "the same result" means

Either what I fixed was not the problem, or it was reviewed before the fix was picked up. One of the two.

**Review before the changes took effect is quite possible.** The sitemap and `noindex` changes went live on October 9; the request was on the 12th. `noindex` only takes effect once Google recrawls those pages, and it is unlikely it revisited 603 of them within three days. I have no way of knowing which snapshot of the site the reviewer saw.

**It is just as possible the fix was not the cause.** As I wrote last time, "low value content" is the broadest reason there is. That empty sitemap pages fall under it was my guess, and there is no evidence the actual review criteria looked at that.

Not being able to tell which is what struck me most across three rejections. The rejection email gives one line of reason, or none as it did this time, and the reasons page in the console attaches the same help link to every rejection. It does not tell you what to fix; it does not even tell you **what the problem was**. Every resubmission is a bet on a guess.

## What remains

Everything fixable is fixed, so what is left are the things that cannot be changed easily.

**1. The nature of the site.** Here is how the 200 Korean posts break down.

| Type | Posts |
| --- | ---: |
| Tarot card dictionary | 78 |
| Announcements of my own apps | 63 |
| Dev logs | 56 |
| Other | 3 |

A reviewer skimming the whole site could read it as "an app developer's promo site with a tarot dictionary attached." The 56 dev logs are the posts I put the most into, but by count they are under a third. App announcements are one per app, structurally similar, and some are in the 1,000-character range. AdSense does not forbid promoting your own products, but if the whole site reads that way it is hard to be recognised as "content for readers."

**2. Almost no search traffic.** This domain moved here in August. Naver Search Advisor registration was late September, the Google domain property October 9. Indexing has only just begun, and search visitors are barely a trickle. AdSense has no official traffic threshold, but there is also no reason to put ads on a site nobody arrives at.

**3. One post, two URLs.** Every post exists in Korean (`/ko/posts/…`) and English (`/posts/…`), pointing at each other with `hreflang`. By Google's documentation that is not duplicate content, but I do not know how the review automation counts it. It is unverifiable, so it stays on the list as a candidate only.

**4. Site age.** Two hundred posts, but as a domain it is three months old. Nothing to do about that except wait.

## What I decided

**I am stopping the two-week resubmission loop.** Rejected → fix by guesswork → re-request two weeks later → rejected, three times around, and each time I took the site apart through a reviewer's eyes. The cost of this loop is not the rejection itself. At current traffic, approval would earn almost nothing anyway. The cost is **spending writing time guessing at a review.**

So the next request is tied to a condition, not a date. When Search Console shows **people arriving from search**, and when dev logs outnumber app announcements, I will request again. Until then I keep writing dev logs as before. I was never writing them for AdSense.

**Still no other ad network.** The reasons are the same as in [the last post](/posts/adsense-low-value-content/). This site is also the developer page for a [children's learning app](/posts/math-monsters-teacher-approved/) with a Teacher Approved badge on Google Play.

**Writing down what the site is for.** This site's job is to be a home for the apps. To say what did not fit in the store listing, and to be a trustworthy place when someone taps "developer website" inside an app. AdSense would be nice on top of that; it is not the purpose. Three rejections had the order upside down.

## Summary

- The October 12 re-request was rejected too. This time the email gives no reason and points to the console.
- In between: sitemap 954 → 353, home, menu and description cleaned up, posts 149 → 200. Same outcome.
- Whether the fix was wrong or the review ran before it took effect is **unknowable.** AdSense does not say.
- Remaining candidates: the site's makeup (63 app announcements plus 78 tarot posts), no search traffic, one post at two URLs, a three-month-old domain.
- The two-week loop stops. I will request again **once search traffic appears and dev logs outnumber app announcements.**

I hope this is the last AdSense post, but when the next result comes I will write it up.

My apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played in the browser](/play/). Updates come through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> AdSense does not give specific rejection reasons. The candidate causes in this post are inferences from my own site and may not apply to other sites.
{: .prompt-info }
