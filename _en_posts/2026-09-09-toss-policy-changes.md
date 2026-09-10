---
title: Apps in Toss Policy Changes for September and October — A Partner's Checklist
description: Apps in Toss announced major changes across four separate notices since late August. Promotional smart-message push ends October 1, a full compliance review of every non-game mini app starts September 30, ad abuse stays permanently enforceable, a boosting program is unveiled on September 21, and business registration is now deferred. Here is what to do and by when, from someone running 26 mini apps
date: 2026-09-09 22:40:00 +0900
categories: [Blogging, Episode]
permalink: /posts/toss-policy-changes/
alt_url: /ko/posts/toss-policy-changes/
image:
  path: /assets/img/20260909_toss-policy/cover.png
  alt: Calendar of Apps in Toss policy deadlines for September and October 2026
tags: [apps in toss, mini app, policy update, smart message, in-app ads, business registration, solo developer, dev log]
---

Apps in Toss has announced some substantial changes over the past two weeks. The problem is that they are spread across four separate notices, each describing *what* changes without making it obvious **what a partner has to do and by when**. I currently run 26 mini apps on the platform, six of which fall under the upcoming compliance review, so I put this together to plan my own schedule. Here it is as-is.

In one sentence: **the era of buying traffic with promotional push is over, and the platform is shifting toward giving exposure to apps that pass a quality bar.**

## The dates at a glance

| Date | What happens |
|---|---|
| **September 14** | You can start submitting fixes for review ahead of the audit |
| **September 21** | Policy webinar (boosting program revealed for the first time) |
| **September 30** | Last day to register and send promotional creatives / non-game audit begins |
| **October 1** | Promotional smart-message push and alerts shut down |
| **October 31** | Last day to view smart-message performance data |

## 1. Promotional smart-message push ends October 1

This is the change with the widest impact, and the first line of the notice is the whole conclusion:

> From October 1, we are ending the operation of promotional push and alerts in Smart Message.

The schedule breaks into three parts:

- **Registering and sending promotional creatives: through September 30**
- **Viewing send performance data: through October 31**
- **Functional push, alerts, and consent forms: unchanged**

The notice states plainly that once the viewing window closes, the performance data cannot be retrieved again. If your workspace ever ran promotional sends, download the numbers before October 31. I ran one promotional campaign in late August for [Tarot Fortune](/posts/tarot-fortune/) and [Tarot Ping](/posts/tarot-ping/), and those results disappear then too.

### Why they are closing it

Toss's stated reason is refreshingly candid:

> Promotional creatives kept increasing, but total send volume has a ceiling, so cases where a registered creative never got sent continued to occur.

The feature originally worked by selecting users most likely to respond to a given creative. As the number of partners grew, creatives piled up while the daily send ceiling stayed fixed — so registering a creative was no guarantee it would go out. Sends were in fact unreliable during August, and the webinar agenda promises to address that confusion first.

One footnote: the fee waiver for promotional smart messages had been **extended through September 30**. The waiver's end date and the feature's end date now land on the same day.

### Functional push is untouched

This part matters. Only the promotional side closes; **functional push, alerts, and consent forms stay exactly as they are.** Scheduled notifications like "Tonight at 8, your new puzzle is ready" remain free to use.

I have functional 8 p.m. Monday-through-Saturday alerts wired into my mini games, and nothing there changes. I wrote up [everything that went wrong](/posts/toss-push-lessons/) while adding them. With promotional push closing, now is the moment to wire in functional push if you have not — it is the only free re-engagement channel left.

## 2. Full compliance review of non-game mini apps (September 30, about one month)

The second change, and for affected partners it puts exposure on the line:

> From September 30, 2026, we will sequentially review every non-game mini app in operation for compliance with the launch guide.

The procedure:

| Item | Detail |
|---|---|
| Scope | All non-game mini apps in operation |
| Timeline | Sequential, starting September 30, over roughly a month |
| Criteria | Compliance with the non-game launch guide |
| Results | Delivered per app via console and email |
| Fix window | 14 days from the date results are delivered |
| If missed | Apps not approved within 14 days are delisted |
| Restoration | Automatically relisted once approved |

Apps already following the guide need to do nothing; the review simply completes. Only apps needing changes get an individual notice, and the 14-day clock starts then.

### Three things to do now

1. **Check your apps against the [non-game launch guide](https://developers-apps-in-toss.toss.im/checklist/app-nongame) yourself.** That document *is* the review criteria.
2. **You can submit fixes for review starting September 14.** The notice asks partners to "submit with as much lead time as possible" because requests may pile up. If everyone waits until the 30th, 14 days evaporate fast.
3. **Verify the email address registered in the console.** Results arrive by console and email, and missing the email costs you the entire fix window.

### The three violations they keep finding

The notice enumerates the cases found repeatedly across mini apps. This is effectively a checklist:

- The Toss navigation bar's back button and a self-implemented back button **both showing at once**
- Back and close buttons that **do not work**
- **Test ad keys or test promotion keys** left in place

The third one caught my eye because I had already dealt with it for a different reason. My builds branch on configuration: debug builds use test ad IDs, release builds use real ones. Since review looks at the release build, that turned out to be the right shape. If you want to avoid shipping with a test key still wired in, splitting it at the build-config level beats relying on memory.

### You cannot pre-check with support

This sentence is worth quoting directly:

> We do not provide advance judgments through the support chat on whether an individual mini app meets a specific criterion. Please request a review in the console to confirm.

So there is no path to asking "is our app okay?" and getting an answer. The only way to find out is to request a review in the console and read the result — which is precisely why requests open on September 14.

### Games are not in scope this time

Of my 26 apps, the 20 classified as games are not part of this audit. The six non-game ones are: two party-roulette apps, [Saju Lotto](/posts/saju-lotto/), [the nursing assistant exam bank](/posts/nursing-quiz/), and the two tarot apps. That said, games have their own launch guide, so being out of scope this round is not an exemption.

## 3. Ad abuse is separate from the audit

The notice nails down a point that is easy to conflate:

> Ad abuse is subject to enforcement at any time under Toss Ads policy, separately from this full review.

Passing the compliance audit and complying with ad policy are two different things, and the latter has no window — it is always in force. That is also why the webinar dedicates a session to "Ad abuse policy and where it goes next." The session blurb explains the motivation well:

> Abnormally inflated ad impressions have been reducing the opportunity and revenue of mini apps that operate normally.

I have something to say here. Different platform, but in August I had an account suspended for a month over invalid traffic on another ad network. Digging into the cause, it was not malicious clicking — the likely culprit was **builds carrying real ad IDs installed on my development phone and run repeatedly**. "Ad abuse" sounds like a heavy accusation, but most of it starts with carelessness like that. I plan to write that incident up separately.

## 4. The boosting program and exposure criteria (first revealed September 21)

This is what Toss says it is preparing to replace smart messages:

> We are preparing new ways to help mini apps get discovered by the right users.

It gets its first public airing at the September 21 webinar. According to the agenda, Toss will disclose the metrics and criteria by which it judges mini app quality, explain how those criteria apply to the All tab, recommendations, search, and newly opening surfaces, and then unveil what qualifying mini apps receive — plus a boosting program for the standouts among them.

Put together, the direction of this whole set of changes becomes clear. The platform is closing the path where you pay for push to manufacture traffic, and moving to one where **the platform itself grants exposure to apps that clear a quality bar**. The audit and the boosting program are separate notices but really one piece: clearing the bar becomes the qualification for getting exposure.

Webinar details:

- When: Monday, September 21, 2026, 3:00–4:30 p.m. KST
- Who: partners currently operating mini apps on Apps in Toss
- Format: online (Zoom); everyone who registers gets the recording, Q&A included
- Structure: four sessions over 60 minutes, plus 20 minutes of live Q&A
- [Register here](https://cloud.business.toss-mkt.im/policy-webinar-2609)

You can submit questions in advance when registering. Only nine days remain between the webinar and the effective date, so it is worth writing your questions down early.

## 5. Announced alongside — ad monetization without business registration (effective August 28)

If the four items above tighten things, this one lowers the barrier. For anyone just starting out, it may be the biggest news here.

Previously you had to register business and settlement information and get it approved *before* receiving an ad ID. Since August 28, you can **issue an ad ID and earn revenue without business registration, up to 5,000 KRW in cumulative estimated earnings.**

The conditions are tight, though:

- Once cumulative estimated earnings **reach 5,000 KRW** without registration, you get a **five-business-day grace period**.
- If registration and approval are not complete within it, **the mini app is temporarily delisted**. It is relisted once approved.
- To be **paid out for a given month, approval must complete by the end of that month.**
- Earnings accrued during the grace period are paid at the **end of the month following** the month registration completes.

So this is not "5,000 KRW of freedom" — it is "get ready before you hit 5,000." Registration takes review time, and five business days is not generous if you are starting the paperwork from scratch. The minimum payout for in-app ads is also 5,000 KRW, which means the moment you qualify for a first payout and the moment registration becomes mandatory effectively coincide.

It is also notable that the notice spells out the tax exposure. Korean VAT law requires business registration **before** commencing business, and continued delay can bring a late-registration penalty (1 percent of supply value), unfiled VAT returns, and penalties for failing to issue tax invoices. A platform deferring a requirement is not the same as tax law deferring it.

## What I am actually doing

My own schedule ended up like this:

1. **This week**: compare all six non-game apps against the launch guide. Verify duplicate back buttons and close-button behavior on a real device.
2. **Week of September 14**: submit reviews early for any app needing fixes. Not waiting for the 30th.
3. **After September 21**: I have registered for the webinar, but the time does not work for me, so I plan to watch the recording — everyone who registers gets it, Q&A included. The first things I will look for are the selection criteria for the boosting program and how ad abuse is judged.
4. **Before October 31**: save the promotional smart-message performance data.
5. **Functional push**: wire it into the apps that still lack it. Once promotional push closes, this is the only free re-engagement channel.

## Closing

Reading this purely as "the rules got stricter" leaves value on the table. Closing the path where money buys push traffic also means **there is more room for a well-made app to be rewarded with exposure.** For a solo developer with no ad budget, that may well be the favorable direction. Of course, the definition of "well-made" gets published on September 21, and that is where it will be decided.

Once I have gone through the webinar recording I will write up the actual contents of the boosting program and the exposure criteria. By then I can work from published standards rather than guesses.

My apps are on [Google Play and Apps in Toss](/posts/apps-in-toss-launch/), and some can be [played right in the browser](/play/). Updates go out here and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> This post summarizes Apps in Toss console notices as of September 9, 2026. Policies can change, so check the original notices in the console before acting on anything here.
{: .prompt-info }
