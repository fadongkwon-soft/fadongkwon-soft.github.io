---
title: Apps in Toss Is Changing How Mini Apps Get Found — Notes From the PO Webinar
description: On 21 September three Apps in Toss product owners spent ninety minutes on what is changing. A quality sweep of every non-game mini app, the end of promotional push, why ad rates fell, and a three-tier exposure policy starting 22 October. Several details were said out loud that never made it into the written notices
date: 2026-09-23 01:30:00 +0900
categories: [Devlog, Platform]
permalink: /posts/apps-in-toss-exposure-policy/
alt_url: /ko/posts/apps-in-toss-exposure-policy/
tags: [apps in toss, toss, mini app, app review, ad policy, solo developer, dev log]
---

## Info
> On 21 September 2026, three Apps in Toss product owners spent ninety minutes explaining what is changing on the platform. Mini apps grew fifteen times in eight months, so discovery is being reallocated from app count to whether a single user comes back. A quality sweep of every non-game mini app starts 30 September, promotional push ends the same day, and a three-tier exposure policy takes effect on 22 October. Several details were said out loud in the webinar that never appeared in the written notices.
{: .prompt-info }

We run more than thirty mini apps, so none of this was somebody else's problem. We went through the deck and the full replay, then checked what actually applies to our own apps before writing this up.

## Background — two numbers

Toss opened with growth. Between January and August 2026, the number of published mini apps grew **15.2 times**, and the time from creating a workspace to shipping dropped by **70.6%**. Published mini apps passed thirteen thousand.

The trouble starts right after that. As the barrier to building dropped, more apps shipped without a baseline user experience, and as the count rose, each app got a smaller share of exposure. The loop Toss drew looks like this: mini apps explode, average quality falls, individual exposure shrinks, good apps stop being seen, users drift away.

So they set two directions. One is the platform stepping in to guarantee a minimum bar. The other is building a structure where a valuable app is rewarded in proportion to that value.

## The dates

| When | What |
| --- | --- |
| 30 September | Sweep of every live non-game mini app begins (about a month, in batches) |
| 30 September | Promotional push and alerts via Smart Send end (functional push stays) |
| 22 October | New exposure policy fully in effect |
| 31 October | Last day to pull Smart Send performance data |
| Early November | Toss native ads roll out gradually |

## The non-game sweep

The scope is **every live non-game mini app**. Games are not in this round.

The bar is not new. It is the non-game launch guide that has existed since the service opened. Early on some criteria were applied loosely so partners could ship fast; now, Toss says, the same standard applies to everyone.

The process: results arrive per app through the console and by email, and if changes are needed you have **fourteen days from the day you are notified** to fix, pass review, and ship. Miss it and the app is delisted.

Two things are easy to misread here. First, **delisting is not deletion.** The app drops out of search and the browse tab, and old shared links land on a blocked screen, but the app and its data remain, and exposure resumes automatically once it is approved later. Second, fourteen days is not a deadline to finish editing. It is a deadline to be **live again**, review approval included.

They named four things partners get caught on most.

- In-app ads appearing at a moment the user could not anticipate
- Pushing users toward installing your own app or your own services
- Showing a login the instant someone enters, before they know what the service does
- Back navigation behaving differently from screen to screen

The written notice singled out three concrete violations: the Toss navigation bar back button and an app's own back button both showing at once, back and close buttons that do nothing, and **test ad units or test promotion keys left in the build**.

The rule about not showing a login on entry came with data attached. Of 14 million login attempts, 6.9 million completed — a **49.6% completion rate**. Treat it as a retention tip rather than a restriction, was how Toss put it.

The most practical piece of advice was about timing. **Since 14 September, pre-review has been running against the exact same criteria as the sweep.** Submit a bundle now and pass, and the sweep has nothing to catch. Once it starts, resubmissions pile up and approval may not land inside fourteen days. Note also that support chat will not tell you in advance whether a specific app meets the bar. Requesting review in the console is the only way to find out.

## Exposure splits into three tiers

This is the core change landing on 22 October.

| Tier | Where it shows | How it is selected |
| --- | --- | --- |
| Published | Search, shared links, public app detail, promotion slots | Every app that passes review |
| Recommended | Store curation, browse tab recommendations, priority in search | Passes all four criteria |
| Boosted | Top slot of the browse tab, the Toss home screen | Top of its category among Recommended, plus editor review |

The recommendation area on the browse tab matters most. Until now every published app rotated through it; from here it opens only to Recommended apps. Far fewer apps appear there, so the traffic each one gets goes up sharply.

The boost was measured at roughly **20 times what a Recommended app gets**. The speaker was explicit that the baseline is Recommended, not Published, so it is worth not mixing those up.

There is no application process. Selection runs continuously and apps move in and out of the candidate pool. They also said they will not build a screen telling you which tier you are in. Watch the acquisition-path breakdown in the console dashboard and see whether traffic from the Recommended or Boosted slots starts arriving.

## The four criteria for a Recommended mini app

| Criterion | What it looks at |
| --- | --- |
| UX | Whether the app is easy to understand and use (five principles) |
| Real usage | Whether it leads to return visits and conversions — called the most important |
| Reviews | Count and spread, recurring complaints, and whether they were fixed afterwards |
| Performance | Whether it crashes on open or freezes |

On real usage the repeated point was that **entering the app is not the metric**. The two things measured are retention and conversion rate. Retention is the return rate; conversion is how often users take the core action they came for. Buying or adding to cart for shopping, completing a booking for a reservation service, continuing to play for a game.

Criteria differ by category. A daily journaling app is judged on whether people keep coming back; a travel eSIM app cannot expect short-term return visits, so it is judged on how many visitors buy. To support that, **categories were split internally into roughly three hundred buckets, and Toss maps every mini app into one**. Which means the category you see in the console may not be the unit you are judged in.

That is why they asked three separate times for partners to **register a custom conversion metric**. The feature is already live in the console and many partners simply have not noticed it. If the metric you want is not among the options, answering that none of them fit feeds back into what gets added.

They also cleared up one misconception about reviews. **Having few reviews is not a penalty.** Usage is judged by retention and conversion; reviews are read to find what users complain about repeatedly and whether the next bundle actually fixed it.

## Cold start for new apps

This produced the best answer of the session. The question was how a new app with no traffic is supposed to prove anything.

Two parts. First, **about 5% of the traffic in the browse tab recommendation area is held back for cold start.** Clear the minimum UX bar and you get shown there so your numbers can be judged. Second, **judging does not need much traffic.** Fifty to a hundred users a day, or around a thousand over a longer stretch, is enough.

If you want to shorten that window, the official answer was to lean on promotions and sharing outside the platform.

Someone asked whether solo developers are at a disadvantage. The answer was that what happens inside the app — how people actually use it — is weighed ahead of brand or track record, and that solo-built apps already showed up among boost candidates in their internal runs.

## Why ad rates fell

eCPM was the topic partners asked about most. Toss gave two causes. Impressions and clicks kept growing while advertiser conversions did not follow, and some impressions and clicks were manufactured in ways that violate policy.

When advertisers do not get the results they expected, they cut budgets or lower bids, and that lands back on partner eCPM. So delivery logic now weighs per-placement conversion performance more heavily, and average eCPM on those placements rose by **about 30%** as a result.

Three things for partners to check.

1. **When the ad appears** — is it interrupting something the user was doing? In a fortune app, an interstitial thrown up while someone is still entering their details gets closed, not watched. The handoff from input to result is a better spot.
2. **How often one user sees them** — how many ads repeat in a single visit? Too frequent and response drops, which means cheaper ads get served.
3. **How many people see them** — two people watching six ads each and six people watching two each are both twelve impressions, but the second earns more. When you add impressions, ask whether the same person is watching more or more people are watching.

None of the three are recommended numbers, and they said so explicitly. Every app has its own balance to find in operation.

From early November, **Toss native ads** designed around conversion start rolling out. The catch is that placements with no history of policy violations go first. They expect the eCPM recovery to become noticeable within the fourth quarter.

## What replaces Smart Send

Promotional push and alerts end on 30 September. Functional push and the notification consent form are unchanged. Performance data is readable only until 31 October, so pull anything you need before then.

The reason given: targeting model training fell behind, which made it impossible to predict when or how much would be sent, and since there is a ceiling on how many notifications a person will tolerate, scaling volume to meet demand was not sustainable.

Two replacements are in the works. A **viral SDK** wraps messenger invites, automatic reward payout, and post-invite funnel analysis into something you can run without writing the plumbing — closed beta in October, wider release during the fourth quarter. **Promotion 2.0** walks a visitor through staged missions toward your core feature, with details coming at the end of October. Its precursor, the browse-and-earn-points slot, has been live since 21 September.

## One thing we checked ourselves

This was mentioned almost in passing, but it turned out to matter more than it sounded. **A non-game mini app is shown only to adults from the moment it launches.** Games inherit the rating issued by a ratings board or a self-rating distributor, but for non-games Toss has to decide itself, so it starts conservative and reviews age ratings for a small number of apps at a time.

Checking our own console confirmed it. Every live non-game app of ours was adults-only, while the games were rated for fourteen and up. An app that serves one Korean history question a day was adults-only too. If your app's content clearly belongs in the all-ages bracket, that is a meaningful slice of reach you are losing, and it is worth asking support to review the rating.

## What you can do now

Toss closed with three items.

1. **Check the UX principles** — the checklist is published in the developer center and the console
2. **Read your reviews** — start with the complaints that keep repeating
3. **Register a conversion metric** — decide your app's core action and register it in the console

One more worth adding: **submit for pre-review now**. It has been running against the sweep criteria since 14 September, and fourteen days is shorter than it sounds if you only start fixing after the verdict arrives.

## Links

- Full replay, unedited: [Apps in Toss webinar on operational changes](https://www.youtube.com/watch?v=agLEu1Z-od0)
- [Non-game mini app launch checklist](https://developers-apps-in-toss.toss.im/checklist/app-nongame)
- [Exposure policy guide](https://developers-apps-in-toss.toss.im/guide/exposure)

Questions they did not get to will be collected and published on the Apps in Toss blog.
