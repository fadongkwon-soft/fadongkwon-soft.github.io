---
title: Google Rejected My Appeal — This Is Where AdSense, AdMob and I Part Ways
description: The publisher account appeal I filed on the night of November 18 was rejected at 1:04 p.m. on November 19, fifteen hours after an acknowledgment email said processing could take a week or more. Not a single line of reasoning. The account will not be reinstated, there will be no further payments, and I may not create a new account. Here are the plain facts — a process that withheld the cause while asking me to analyze it, publisher responsibility for traffic the publisher cannot see, three payment notices that contradict each other — along with my own share of the blame, what changes now, and what I would pass on to other solo developers
image:
  path: /assets/img/20261119_google-ads-appeal-rejected/cover-en.png
  alt: "Google rejected my appeal: the end of AdSense and AdMob"
date: 2026-11-19 23:22:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/google-ads-appeal-rejected/
alt_url: /ko/posts/google-ads-appeal-rejected/
tags: [admob, invalid traffic, ad policy, android, solo developer, dev log]
---

At 1:04 p.m. on November 19, the answer to my appeal arrived, from the Google Ad Traffic Quality Team. It said three things.

- Having reviewed what I submitted, "we are unable to reinstate your publisher account."
- No more money will be paid out to the account.
- I can no longer take part in any of their publisher programs, and I cannot open a new account.

**There was not a single line of reasoning.** Nothing about what was judged to be invalid traffic, which part of my analysis was not accepted, or what the decision was based on. According to Google's help pages, a rejected appeal is final.

I was stunned. This post is written by someone who is angry, but it is not a rant. I will lay out the confirmed facts and mark my own estimates and the things I do not know separately. How I went through the ledger, which hypotheses I ruled out and what I put in the appeal are all in [yesterday's post](/posts/admob-account-disabled-appeal/), so I will not repeat them here. As before, no money figures.

## Timeline

| Date and time | What happened |
|---|---|
| August 26 | First suspension. Reason: invalid traffic. Length: 29 days. No appeal form. The cause was my own development phone ([the first suspension post](/posts/invalid-traffic-suspension/)) |
| Around September 24 | Suspension lifted. Ads back on from September 27 |
| November 14–17 | Apps with impressions jumped from 32–39 a day to 85–97, and clicks ran at 6–8 times normal |
| November 16 | Fourth AdSense rejection for the site ([the fourth rejection post](/posts/adsense-fourth-rejection-index-recheck/)) |
| November 18, 08:03 | The account-disabled email and the payments-account-closed email arrive in the same minute. The AdMob reporting API returns 401 from that day |
| Night of November 18 | Appeal filed. Acknowledgment email at 10:02 p.m., saying processing may take a week or more |
| November 19, 13:04 | Rejected |

From the acknowledgment to the rejection was fifteen hours. Something I had been told could take a week or more was over in less than a day. I will not complain about the speed itself; it beats waiting all week. But nothing in the reply tells me what was reviewed in those fifteen hours.

## The numbers, looked at again after the rejection

The anomaly detector I built for yesterday's post now runs every time I update the ledger. On the November 19 update it raised the alarm again for November 17, the last day collected. Here are that day's account-level numbers against the median of the previous 28 days.

| Metric | November 17 | 28-day baseline | Multiple |
|---|---:|---:|---:|
| Apps with impressions | 97 | 30 | 3.2× |
| Clicks per day | 97 | 8.5 | 11.4× |
| CTR | 4.50% | 1.14% | 4.0× |

Widening to the last seven days tells the same story: an average of 54.4 clicks a day versus 11.3 over the 28 days before, and 65.0 apps with impressions a day versus 25.6. On that single day, 2 apps had at least as many clicks as impressions, and 3 apps with 20 or more impressions had a CTR of 15% or higher. The highest of those was 59.4%.

The detector also counted 8 apps that "showed impressions again after 28 days with none." That item, though, includes apps I launched in November that simply have a short history, so I will not use it on its own as evidence that dormant apps woke up. Yesterday's analysis is the more accurate account of that: 36 apps with zero impressions on November 7–13 had impressions on November 14–17. The November 14–17 figures are still unconfirmed estimates collected before the suspension.

Looking at these numbers again, I had one thought. This is not what people using apps looks like. And these numbers did not stop the rejection.

## Five things I found hard to believe

### 1. They withheld the cause, then asked me to analyze it

The suspension email said specific account activity could not be shared, because it could be used to get around their detection systems. The same email asked me to analyze the traffic and other causes believed to have led to the invalid activity and put the results in the form.

So I spent a day analyzing. I split the ledger into periods, ruled out five hypotheses on my side with evidence, checked the numbers against Play install stats, and trimmed everything to fit a form capped at 1,000 characters per field. What came back was a form letter with no reasoning.

I do not know whether the appeal failed because my analysis was wrong, or whether it was right and it made no difference. I do not know what I should have fixed. Normally you need to know that in order to do better next time. There is no next time, so I no longer need to know.

### 2. The responsibility is the publisher's; the data is Google's

Google's help pages say publishers are responsible for invalid traffic on their account even when a third party generated it. Whoever made it, once it lands in your account it is yours.

But the publisher could not see which countries that traffic came from, or which devices or OS versions. On the day of the suspension the AdMob reporting API returned 401, and the console was suspended too, so the detail screens were out of reach. All I had left was a ledger with two dimensions: date and app.

| Who | Can see | Has to carry |
|---|---|---|
| Google | Country, device, IP and patterns behind each impression and click | The decision |
| Me | Impression and click counts per date and per app | Every consequence of the decision |

Not collecting those dimensions in advance was my mistake, and I will come back to it below. Even so, I could not accept a setup where the moment an account stops, its own past reports close along with it. It amounts to being asked to explain traffic whose shape you are not allowed to see.

### 3. Three payment notices, three different answers

Three emails about the same account, received over two days, describe the remaining balance differently.

| Email | Received | What it says about the balance |
|---|---|---|
| Account disabled | November 18 | Amounts judged valid are paid out after a 30-day hold |
| Payments account closed | November 18 | If the balance is above a threshold, a final payment goes out in the next cycle |
| Appeal rejected | November 19 | No further payments |

I do not know which is right. I suspect I will only find out when the 30-day hold ends. Two of the three say there may be a payment; one says there will not. All three came from the same company about the same account.

### 4. By my data it was not people. Google judged otherwise

Here I will keep facts and estimates apart.

**Confirmed**
- On November 14 the number of apps with impressions went from 39 to 85 in a single day, and stayed at 85–97 for four days.
- Over the same period, new Play installs were 0–2 per app, the usual level (based on data through November 15, which was all that was available when I investigated).
- I suspected my development phone, an emulator on the new PC, work I had moved to another AI tool, weakened defensive code, and the October 24 removal of in-app ad caps, and ruled each out with evidence.

**My estimate**
- Devices that do not show up as Play installs ran release builds of about 90 of my apps and generated those impressions and clicks. I do not believe the traffic was mine.

**Unknown**
- Whose devices they were. It could have been a third party's automation scraping app catalogs, or something else.
- What Google based the rejection on. I cannot tell whether Google saw something that differs from my estimate, or whether my estimate was right and the "third-party traffic is still the publisher's responsibility" rule was simply applied.

From what I can see, it was not people. But Google makes the call, and Google sees things I cannot. My conclusion is an estimate and nothing more, and I want that on the record.

### 5. One attempt, then it is over

The appeal was a single attempt, a rejection is final, and I cannot create a new account. Even the acknowledgment email noted that if an appeal had already been filed for the account, further appeals might get no response.

The first suspension in August had no appeal form; I waited 29 days and it lifted. This time there was a form, I used it once, and that was the end. Not one app but an entire business is removed from Google's ads programs, and there is no second look at that decision.

## My share of the blame

If I stopped here, this would be a post that blames everyone else. Some of it is clearly on me.

- **I did not collect dimensional data.** Had I been storing country, OS version and ad format all along, I could have worked out for myself where the November 14–17 traffic came from, and written the appeal with data instead of estimates.
- **I did not look at the ledger for four days.** The anomaly started on November 14; I found out on the morning of the 18th, when the suspension email arrived. Knowing on day one might have left me some options.
- **The banner placement had flaws.** The wrapper kept a banner on every screen, gameplay included, and the banner overlapped the bottom gesture navigation bar. By the AdMob banner guidelines as I read them, that is a discouraged implementation. I could not establish how long it had been that way. The details are in [yesterday's post](/posts/admob-account-disabled-appeal/).
- **I hung about 100 apps on a single ad account.** I built the structure in which one decision stops everything.

I do not know whether any of these was the reason for the rejection, because no reason was given. But I cannot write "I did nothing wrong."

## What changes now

| Item | Until now | From now on |
|---|---|---|
| AdMob ads in the Play apps | Suspended, waiting on the appeal | Over. I will not apply again |
| AdSense for the site | "Not reapplying until the conditions are met" | Same publisher account, so applying is impossible regardless of conditions. The reapplication plan is dropped |
| This blog | Run partly with AdSense review in mind | Continues as a record, with no connection to ad review |
| Apps in Toss ads | Running | Not affected |
| Defensive code | Promised in the appeal | Carried over to the next ad network |

**AdSense for the site.** In [the fourth rejection post](/posts/adsense-fourth-rejection-index-recheck/) I wrote that I would not reapply until search clicks topped 10 a day for two weeks running and dev logs outnumbered app introductions. Those conditions no longer mean anything. The site's AdSense ran on the same publisher account as the app ads, and that account is closed. Meeting the conditions would leave nowhere to apply. The work around [the second rejection](/posts/adsense-low-value-content/) and [the third](/posts/adsense-rejected-again/), trimming the sitemap and adding posts, ends here as far as ad review goes.

**This blog.** I will keep writing. The dev logs were always meant to help other people make fewer of the same mistakes; passing ad review was a goal stacked on top. Only the stacked part has fallen off.

**Toss.** Ads in Apps in Toss run on a separate platform operated by Toss, so this action has nothing to do with them. In the ledger, Toss ad impressions on November 18 were 2,111, in line with the previous week (1,918–2,155 a day).

**Defensive code.** These are what I promised in the appeal and put into code on November 18–19.

| Measure | What it does | Status |
|---|---|---|
| Block non-Play installs | If the install source is not the Play Store, no live ads are requested | In code, not yet shipped |
| 20-a-day cap | 20 ads per person per day, n/20 shown on screen, play stops for the day once it is reached | In code, not yet shipped |
| Banner spacing | Bottom navigation inset, a 10dp non-interactive strip between the WebView and the banner | In code, not yet shipped |

With AdMob gone, I could throw this code away. I am keeping it. If my estimate is right, the November 14–17 traffic was not aimed at AdMob; it swept through my apps. In that case the same traffic will reach the next ad network's account too, and to avoid losing that account for the same reason, this code has to be in place first. All of it lives in the wrapper and works regardless of the ad network.

**Other ad networks.** The outlook is not great. After the first suspension in August I created an AppLovin publisher account and requested approval; on September 23 the reply said they were not accepting new signups or reactivating older accounts at this time. For now the plan is to try Unity LevelPlay on one or two apps as a pilot. Whether the Play apps will earn ad revenue again, I do not know yet.

## For other solo developers

1. **A single ad account is a single point of failure.** A hundred apps still means one account, and one decision stops all of them. And because a rejection also bars new accounts, what gets blocked is not an app but the business. Do not keep all your revenue with one company. My business did not stop this time only because Toss was separate.
2. **Collect the data before you are suspended.** Store country, OS version and ad format every day, not just date × app. The API closes the day you are suspended. By then it is too late.
3. **Watch the number of apps with impressions every day.** This anomaly showed up first, and most clearly, in that number rather than in clicks. If you have many apps, it is the cheapest alarm you have. I did not look for four days.
4. **Check the install source.** Play APKs can spread outside Play. There is no reason to request live ads from a run that was not installed through Play.
5. **Write the appeal as if you get exactly one.** State estimates as estimates, disclose unfavorable changes first, and phrase things you have not yet done as "I will." You can still be rejected. I wrote it that way, and I was.
6. **If an AI agent runs your investigation, keep the logs.** I worked through this investigation with an AI agent, and because the tool-call logs existed I could rule out one suspicion on my side within a day. But the lack of the data needed to judge the case was the same limit no matter who investigated.

> Platforms do not disclose the basis for invalid traffic decisions, and this rejection email gave no reason either. The cause analysis in this post is my estimate from my account's ledger and Play statistics, and does not describe what Google based its decision on.
{: .prompt-info }

## This is where it ends

In August, my own development phone stopped the account; I fixed it, waited, and came back. This time traffic I could not see stopped it; I investigated as far as I could, filed, and it ended with a single reply that gave no reason. I never came to accept it.

This is where Google ads and I part ways. I will not apply again.
