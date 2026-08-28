---
title: What I Learned Shipping 8 Apps as a Solo Dev with a Day Job
description: Eight apps built after work, and what actually went wrong — review rejections, yearly API bumps, and why releasing takes far longer than building
image:
  path: /assets/img/20260826_devlog/apps-grid.jpg
  alt: Icons of the eight apps I have shipped so far
date: 2026-08-26 20:00:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/solo-dev-8-apps/
alt_url: /posts/solo-dev-8-apps/
---

It has been a year and a half since I wrote about [the road to my first app release](/en/posts/ready-to-open/). Back then, getting even one app onto a store was unknown territory, and my goal was "one app every two weeks." Today there are eight apps on the stores. That is nowhere near the pace I aimed for, but along the way I learned things I could not have imagined at the start.

This is not a success story. Revenue is still barely keeping up with running costs. What it is, instead, is a record of how different "building an app" turns out to be from "shipping an app and keeping it alive."

## Releasing takes longer than building

This is the prediction I got most wrong. My first app, [Spin the Bottle](/en/posts/spin-the-bottle/), was a working app three hours after I sat down to write it. Getting that app onto a store took a few weeks. Here is what sat in between.

- Developer account registration and business information verification
- App icon, feature graphic, and screenshots in several required sizes
- A privacy policy page (which means you need a website)
- Content rating questionnaire, data safety section, target age declaration
- Store listing copy, and then waiting for review

Almost none of it is code. And the whole list **repeats once per app.** Saying I built eight apps means I walked through that process eight times. It gets faster after the second one, but it never goes away.

The lesson here is simple. If you have ten ideas and start all ten, you will ship none of them. Even for an app that takes three hours to build, budget days for the release. Then your plan holds.

## What blocks a review is usually not your code

The rejection that stung most was the first review of [Reaction Challenge](/en/posts/play-minigames/). The stated reason was an invalid privacy policy. There was nothing wrong with the app's code. The problem was on my website. A GitHub Pages misconfiguration had left the privacy policy page returning a 404, and the reviewer opened the link and rejected the app.

App review does not look only at the app. It looks at your developer account details, the web pages you link to, and your store copy. Things outside the app are what block the app. That is where my habit of opening every URL I put in a store listing myself, in a private window, came from.

The second rejection reason I hit most often was load time and external resources. When you ship a web-based app that pulls fonts or a rendering engine from an external CDN, those requests get blocked in the review environment and the first screen never appears. Working on my machine and working in the review environment are two different problems.

## The real work starts after you ship

A release is not the end. It is the start of maintenance. Stores raise the required target API level every year. Leave an app you built a year ago untouched and one day you get a notice telling you the app will no longer be shown to new users. With eight apps, that is eight rounds of this work as well.

So a strategy of adding more apps carries a hidden cost. What each new app adds is not development time but a **fixed amount of work that comes back every year**. To cut that cost down I spent a fair amount of time restructuring things so that several apps share one code base. Multiple games now live in a single repository, and the parts that go into every app — ads, sharing — are bundled into shared packages. Building one app still takes the same time, but I can update all eight at once.

## Not betting everything on one platform

The best decision I made this year was putting apps on [Apps in Toss](/en/posts/apps-in-toss-launch/). It is a mini app platform that runs inside the Toss app with no install, and I could publish nearly the same web-based code as it was. Meeting people through store search and being surfaced inside an app where people are already gathered are completely different kinds of traffic.

Every platform has its own review criteria and policies, of course, and that means more things to keep track of. But if you stake everything on a single store algorithm, the day that algorithm changes there is nothing you can do. Adding a second channel is less about doubling your reach than about securing a floor of traffic that will not vanish.

## The apps my kids use are the ones that stay

The apps that were the most fun to build, and that I still keep coming back to, are the ones I made for my children. [Hangul Monsters](/en/posts/hangul-monsters/) came out of watching my child work through learning Hangul, the Korean alphabet, and [Math Monsters](/en/posts/math-monsters/) out of watching my oldest get bored with arithmetic drills. When the actual user is sitting next to you, feedback is immediate. Several bugs got fixed because I heard "this button doesn't work."

The apps I built from an idea alone, by contrast, I rarely touched again after release. If you cannot picture the face of the person using it, you cannot picture what to fix either. When I built [Nursing Assistant Mock Exam](/en/posts/nursing-quiz/), an app for Korea's nursing assistant licensing exam, I settled the question count and the wrong-answer review structure by picturing someone actually studying for the test, and the features I chose that way still had obvious reasons behind them when I came back to them later.

## What's next

I threw out the original "one every two weeks" goal. I replaced it with two rules. The first is to build only apps I will still want to work on. The second is to keep a structure where adding one more app does not add to the fixed workload.

In the next post I will walk through publishing an app on Apps in Toss, from registration to review, in order. There is still not much written about it in Korean, so I suspect a fair amount of it will help anyone trying it for the first time, as I did.

---

The apps I have shipped so far are written up in their own posts — [three Play mini games](/en/posts/play-minigames/), [Saju Lotto](/en/posts/saju-lotto/), [Juice Spinner](/en/posts/juice-spinner/), and the rest. News goes out on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
