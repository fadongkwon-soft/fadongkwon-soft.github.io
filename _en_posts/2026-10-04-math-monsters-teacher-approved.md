---
title: Math Monsters Is Now a Google Play 'Teacher Approved' App
description: We never applied, yet a congratulations notice was waiting in the Play Console. Teachers and specialists reviewed Math Monsters and approved it as a good app for children aged 6 to 12, so it now carries the Teacher Approved badge on Google Play and can be featured in the Kids tab. What the reviewers noted, and how the fixes we made after two store rejections pointed the same way
date: 2026-10-04 21:35:00 +0900
categories: [Devlog, Retrospective]
image:
  path: /assets/img/20261004_math-monsters-teacher-approved/play-badge.png
  alt: Math Monsters on Google Play with the Teacher Approved badge
permalink: /posts/math-monsters-teacher-approved/
alt_url: /ko/posts/math-monsters-teacher-approved/
tags: [math monsters, teacher approved, google play, early education, elementary math, parenting, solo developer, dev log]
---

## Info
> Math Monsters, our arithmetic game for kids, has joined Google Play's Teacher Approved program. We never applied: apps made for children are reviewed by teachers and specialists automatically, and the approval arrived as a notification on 30 September 2026. The app now shows the Teacher Approved badge on Google Play and can be featured in the Kids tab. Here is what the reviewers noted, and why the fixes we made after two store rejections turned out to point the same way.
{: .prompt-info }

## A Congratulations Notice We Never Applied For
While going through my Play Console notifications, I found one that had arrived on 30 September.

![Play Console notification — your app has been included in the Teacher Approved program](/assets/img/20261004_math-monsters-teacher-approved/notice.png){: w="420" }

**"Congratulations. Your app has been included in the Teacher Approved program."** (The console shows it in Korean.)

We had never applied for anything or asked anyone to recommend the app. Because it came out of nowhere, it made me all the happier.

## What the Teacher Approved Program Is
Google Play started the program in 2020. **Teachers and children's education and media specialists** try out apps for kids themselves and pick the ones worth recommending to children.

- **There is no application.** Apps made for children are put up for teacher review automatically. All we did was state honestly that Math Monsters is meant for children.
- **What they look at**: according to Google, language and sound suited to the age group, screens a child can use alone, visual quality, whether the app delights children, whether it supports healthy development and creativity, whether any content is inappropriate, and **whether ads, in-app purchases and promotion of other apps, if present, are appropriate for children.**
- **What approval brings**: the **Teacher Approved badge** on Google Play, eligibility to be featured in the Google Play **Kids tab**, and a section on the app's details page with what teachers and specialists said.

## What the Reviewers Said
This is the Teacher Approved program page in our Play Console.

![Play Console Teacher Approved program page — status approved, with notes from teachers and specialists](/assets/img/20261004_math-monsters-teacher-approved/program.png){: w="760" }

**The status is "Approved"**, the target age groups are 6–8 and 9–12, and the last review was on 29 September. The public store page says the app was "Approved by teachers for: Ages 6-12".

The notes from teachers and specialists read as follows (translated from the Korean console).

| Area | Notes |
| --- | --- |
| Age appropriate | Ages 6–8 |
| Delight and engagement | Popular theme, characters |
| Designed with children in mind | Words and sound, easy to use, art and animation |
| Creativity and imagination | Innovative |

It is a simple game in which you solve arithmetic problems to catch monsters, and it was rated "innovative" for creativity.

If you open the Math Monsters page on Google Play now, the **Teacher Approved** badge sits right under the title.

![Math Monsters on the Google Play store — Teacher Approved badge](/assets/img/20261004_math-monsters-teacher-approved/play-badge.png){: w="760" }

## Looking Back: What We Fixed After Being Rejected
Reading the criterion that ads, in-app purchases and promotion of other apps must be appropriate if present, I thought back over the past month. Math Monsters is an app that Google Play rejected twice.

- **Late August, the first rejection.** The "other apps" cards inside the app also showed apps for adults, such as tarot and saju. Google treats promotion of other apps inside a kids' app as advertising. So kids' apps now show only apps that suit children, and we removed the ad SDK from the build entirely.
- **Early September, the second rejection.** The website and privacy policy links in the store listing led to the blog home page, where tarot posts are visible. We made a plain information page just for the kids' apps and linked that instead.
- **On 5 September**, we [removed every paid product](/posts/monsters-go-free/) and opened all modes for free.
- **In late September**, [when we added a rating prompt](/posts/review-prompt-toss-play/), we switched it off in the kids' apps.

At the time we made these changes to get through review, and because it seemed obvious for an app children use. I cannot know how much they had to do with the approval. But we were clearly looking the same way as the teachers' criteria, and that makes those rejections feel worthwhile.

## An App Whose Icon Was My Son's Photo
Math Monsters was never meant for the store at first. After my eldest stopped doing Kumon math, I built a practice app so he could keep drilling arithmetic at home, and **its icon was a photo of my son** ([that story](/posts/kumon-to-math-monsters/)).

So an app made for one child has been judged by teachers and specialists as worth recommending to other children too. My eldest still boasts that he was the app's "original monster" — and that app now carries a Teacher Approved badge.

## Get It
No ads, no paid products. No sign-up — just start.

- Google Play: <https://play.google.com/store/apps/details?id=com.fadongkwon.math_monsters>
- Apps in Toss: <https://fadongkwon.com/toss/math-monsters/> — open it on your phone and it goes straight to the Toss app.

The app introduction and gameplay video are in [the Math Monsters post](/posts/math-monsters/). News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
