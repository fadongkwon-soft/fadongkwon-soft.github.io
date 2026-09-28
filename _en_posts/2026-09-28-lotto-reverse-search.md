---
title: Searching Backwards for the Birth Charts and Plates That Made Last Week's Lotto Numbers
description: Two of our lottery number apps now look backwards. Every week a job searches for the birth charts and license plates whose generated numbers exactly match the real winning six. The two apps behave in opposite ways, and the wording had to follow the arithmetic. Birth charts come up empty most weeks; plates match about two hundred times every single week
date: 2026-09-28 23:40:00 +0900
categories: [Devlog, App]
permalink: /posts/lotto-reverse-search/
alt_url: /ko/posts/lotto-reverse-search/
tags: [lottery, lotto, saju-lotto, automation, apps in toss, solo developer, dev log]
---

## Info
> Two of our lottery number apps now look backwards. Every week a job searches for the birth charts and the license plates whose app generated numbers exactly match the real winning six. The two apps behave in opposite ways: the birth chart space is smaller than the number of lotto combinations, so most weeks produce nothing, while the plate space is forty two times larger, so roughly two hundred plates match every single week. The wording had to change with the arithmetic.
{: .prompt-info }

Both apps turn an input into lottery numbers. The same birth chart always produces the same numbers in the same week. So the question can be asked in reverse. **Was there an input that would have produced last week's winning numbers exactly?**

## One thing first

This is not prediction. The draw happens, then we search backwards for something that matches it. It also does not mean anyone actually bought that ticket. That is why the word "jackpot" appears nowhere in either app. One word like that turns arithmetic into a claim we did not earn.

## The two apps are opposites

A Korean 6/45 draw has **8,145,060** possible combinations. Comparing that number with each app's input space splits them cleanly.

| App | Input space | Versus lotto combinations |
|---|---|---|
| Saju Lotto | 816,686 | 0.1x |
| Car Number Lotto | 346,500,000 | 42x |

The birth chart space is every birth date times the hour of birth times gender. The plate space is the leading digits times one Hangul syllable times the four trailing digits.

**Birth charts run short.** Running every draw from round 1231 to 1243 produced a match in only seven of thirteen weeks. So when a week comes up empty, the app keeps showing the most recent week that did produce one.

**Plates overflow.** With forty two times more combinations than the lottery itself, no week comes up empty. An exhaustive scan of round 1243 found 206 of them. Writing that up as a rare event would be a lie, so the wording stays plain and the card explains why there are always several. Without that explanation a reader assumes the numbers are invented.

## Plates get one digit hidden

A plate identifies one real vehicle. A birth date is shared by thousands of people; a plate is not. So one digit is replaced before display, and which digit is hidden changes every week and differs row to row.

There are only ten candidates for the hidden digit, so anyone can find it by trying. That is weak concealment, and that is the point. **A claim nobody can check is a claim nobody should believe.** Type the plate into the app and the winning numbers come out of exactly the game the card names.

The Hangul syllable is never hidden. Thirty five candidates would be cruel to anyone who wanted to verify.

## Why this does not run on the phone

An exhaustive plate search covers 346,500,000 plates. Using the app's own generator unchanged, that takes five hours. Not something to run on a handset.

So a GitHub Actions job computes it once every Sunday morning and the app only downloads the result. The winning numbers themselves were already being refreshed weekly by another job, so this one runs right after it.

The scan prunes. It draws numbers in the same order the app does, but abandons a candidate the moment a number appears that is not in the winning set. There is no need to finish all six, so hashes per candidate drop from about thirty five to six.

The work is then split across cores. Forty five minutes on one thread became nine minutes and twenty three seconds on eight. Running both ways over the same draw produced result files identical down to the byte, apart from the timestamp.

| Method | Speed | Full scan |
|---|---|---|
| App code unchanged | 18,700 plates/s | 308 min |
| With pruning | 121,000 plates/s | 45 min |

Pruning is a hand written copy of the app's logic, which can drift. So **everything it finds is re-checked with the app's own code.** There are only a few hundred hits, so that costs nothing. A differential test came first: fifty seven plates including three known answers, plus three million random ones, produced identical results from both paths.

## Revealing the digit is the app's own calculation too

The answer is not shipped in the data file. That file sits at a public address, so putting the answer in it would defeat the hiding entirely.

Instead the app tries digits zero through nine itself and keeps the one that works. It is exactly the calculation a person would do by hand ten times. That is why the result can be trusted.

## What is left

The first plan was to hide the plate and leave it hidden. The objection that came back was that hiding it makes the whole thing unverifiable, and therefore less believable, not more. Concealment and verification looked mutually exclusive until the candidate pool was narrowed to ten. Hidden enough not to name one car, open enough to check.

Star Lotto and Name Lotto did not get the feature. The zodiac version forces two of three lucky numbers into every set, which makes the winning combination structurally unreachable in about sixty percent of draws. Names are not blocked, but eighty thousand plausible Korean names produce zero matches; reaching one expected match would need millions of names, and most of those would not be names anyone actually has.
