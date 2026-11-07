---
title: My App's Lunar Calendar Was China's — Checking 36,890 Days of Lunar Conversion and Why Whole Months Shift by a Day
description: Before switching the saju (Four Pillars) calculation in Saju Lotto and Zodiac Pet to a manseryeok library built on the Korea Astronomy and Space Science Institute (KASI) calendar, I compared the old converter day by day over 36,890 days from 1930 to 2030. 1,319 days (3.6%) differed, all in 44 stretches where an entire lunar month started one day early. Computing the new moon separately showed that in 42 of them the new moon fell between midnight and 1 AM Korea time, still the previous evening in Beijing. The old converter was effectively a Chinese lunar table; the remaining two stretches were leap-month placement differences in 2012 and 2017. Year and month pillars differed in only 35 of 442,680 cases, all within minutes of a solar term
image:
  path: /assets/img/20261108_lunar-calendar-kasi/cover-en.png
  alt: "My lunar calendar was China's"
date: 2026-11-08 01:29:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/lunar-calendar-kasi/
alt_url: /ko/posts/lunar-calendar-kasi/
struct_exempt: [images]
tags: [saju, fortune telling, solo developer, dev log]
---

[Saju Lotto](/posts/saju-lotto/) and [Zodiac Pet](/posts/zodiac-pet/) show a saju (Four Pillars) card from your birth date. Many Korean users enter their birthday in the lunar calendar, so the app converts it to a solar date and then finds that day's stem-branch pair (the day pillar). Get the date wrong by a single day and the day pillar changes, and so do the five elements shown on the card.

This week I switched the saju calculation to `manseryeok` (MIT), an open-source library that carries the lunar calendar and solar-term table of the Korea Astronomy and Space Science Institute (KASI). Before switching, I wanted to know how wrong the old converter had been, so I compared a hundred years day by day. The result was cleaner than I expected, and the cause was more fundamental.

> The fortune-related parts of this post are about the calculation accuracy of entertainment content. Whether any saju interpretation is right is outside its scope.
{: .prompt-info }

## What was compared

The old converter is a port of the Dart package `lunar_calendar_converter_new` 2.0.0. It started in an app I first built in Flutter and was later ported to Kotlin and TypeScript, with all three kept producing identical results. It works from two tables: lunar month lengths and the solar date of each lunar new year.

I ran two comparisons.

- **Solar to lunar**: every day from January 1, 1930 to December 31, 2030 (36,890 days), comparing the lunar date (year, month, day) from the old converter and the new library
- **Year and month pillars**: the same 36,890 days × 12 two-hour birth periods = 442,680 cases, comparing the old saju code's year and month pillars with the new library's

## Results at a glance

| Item | Value |
|---|---|
| Days compared | 36,890 |
| Days with a different lunar date | **1,319 (3.6%)** |
| Continuous stretches they form | 44 (43 of 30 days, 1 of 29 days) |
| Years with a different Seollal (lunar new year) date | 8 |
| Years with a different Chuseok date | 1 (1942) |
| Cases with different year/month pillars | 35 of 442,680 |

The 1,319 days were not scattered. There were 44 stretches in which **an entire lunar month was shifted by one day**, and together they made up the 1,319 days. For example, for the 30 days from February 7 to March 8, 1997, the old converter counts from "lunar 1997, month 1, day 1" while the new library counts from "lunar 1996, month 12, day 30." In the old converter, that month started a day early.

The years with a different Seollal date are 1944, 1954, 1958, 1966, 1988, 1997, 2027 and 2028. In all eight, the old converter was one day early. For 1997, the old converter says February 7; the Korean calendar says February 8.

## Why whole months shifted — the new moon fell just after midnight

A lunar month begins on the day that contains the new moon (the moment the moon lines up with the sun and cannot be seen). But the clock that decides "which day" differs by country. Korea uses standard time based on 135°E (UTC+9); China uses 120°E (UTC+8). One hour apart.

So trouble arises when the new moon happens **between midnight and 1 AM Korea time**. In Korea it is already the next day, but in Beijing it is still 11 PM the previous evening, so the Chinese calendar starts that month a day earlier.

For each of the 44 stretches I computed the new moon near the start date separately, using the new moon formula from chapter 49 of Meeus's *Astronomical Algorithms*.

| Stretch start (solar) | New moon (Korea time) | New moon (Beijing time) | Old converter | Korean calendar |
|---|---|---|---|---|
| 1997-02-07 | Feb 8, 00:06 | Feb 7, 23:06 | lunar 1997, month 1, day 1 | lunar 1996, month 12, day 30 |
| 1988-02-17 | Feb 18, 00:54 | Feb 17, 23:54 | lunar 1988, month 1, day 1 | lunar 1987, month 12, day 30 |
| 2027-02-06 | Feb 7, 00:56 | Feb 6, 23:56 | lunar 2027, month 1, day 1 | lunar 2026, month 12, day 30 |
| 1942-09-10 | Sep 11, 00:52 | Sep 10, 23:52 | lunar 1942, month 8, day 1 | lunar 1942, month 7, day 30 |

**42 of the 44 were exactly this case.** The new moon fell between midnight and 1 AM Korea time, between 11 PM and midnight the previous day in Beijing. The old converter was effectively a Chinese lunar table. If the original package was built on the Chinese calendar, every number lines up. The new library's documentation also says "KASI canonical lunar calendar, with Korea-China differences corrected."

For one stretch (December 1, 2005) the computed new moon came out at exactly 00:00 Korea time. The formula is accurate to a few minutes, so I left that one undecided.

## The other two — a different leap month

The remaining two stretches were not about the new moon time. The leap month was in a different place.

- **2012**: Korea has a leap 3rd month (from April 21 solar); China has a leap 4th month. So for a month from April 21 the old converter says "month 4" and the Korean calendar says "leap month 3."
- **2017**: Korea has a leap 5th month (from June 24 solar); China has a leap 6th month. For 29 days from June 24 the old converter says "month 6" and the Korean calendar says "leap month 5."

Leap months are decided by the order of solar terms and new moons. Shift a new moon by a day and the month that lacks a principal term (zhongqi) can change, which moves the leap month. The cause is the same one-hour difference.

## What changes for users

If someone entered a lunar birthday that falls on one of those 1,319 days, the old app picked the wrong solar date by a day. That changes the day pillar, so the day stem (the character that represents "you") and the element counts change. Pick any day between 1930 and 2030 and the chance is 3.6%. Someone born on Seollal 1997 who entered lunar month 1, day 1 got it wrong 100% of the time.

People who entered a solar birthday are unaffected, because the day pillar depends only on the solar date.

## Year and month pillars — differing only minutes around a solar term

Year and month pillars are decided by solar terms, not the lunar calendar. The year pillar changes at Ipchun (start of spring), and the month pillar changes at each major solar term. The old code judged solar terms by computing the sun's longitude with Meeus's low-precision formula, which is off by about 15 minutes in time. The new library uses a solar-term table matched to KASI to the minute.

Across all 442,680 cases with the 12 birth periods, 35 differed. Every one was within minutes of a solar term.

| Input (Korea time) | Solar term (new library) | Old verdict | New verdict |
|---|---|---|---|
| 1997-06-06 00:30 | Mangjong 00:33 | O month (after the term) | Sa month (before the term) |
| 1994-02-04 10:30 | Ipchun 10:31 | Gapsul year (after Ipchun) | Gyeyu year (before Ipchun) |
| 2000-04-04 20:30 | Cheongmyeong 20:32 | Jin month (after the term) | Myo month (before the term) |
| 1936-02-05 08:30 | Ipchun 08:29 | Eulhae year (before Ipchun) | Byeongja year (after Ipchun) |

Unlike the lunar conversion, this is a precision issue in an approximate formula and rarely shows. Still, for someone born on Ipchun day the year pillar (the zodiac animal) can change, so when a solar term falls inside the chosen birth period the new app adds one line: "if before this time, year X; if after, year Y."

## What changed and what stayed

- **The saju card now follows KASI.** Lunar input is converted to a solar date by the new library, and year and month pillars are judged by the solar-term table.
- **A leap-month checkbox was added.** It appears only when that year has a leap month after the chosen month. The old app never asked about leap months at all.
- **Lottery numbers did not change.** Saju Lotto's numbers come from a seed built from the birthday, and that seed keeps using the old lunar key. Changing the seed would have changed the numbers of every existing user who entered a lunar birthday overnight. I chose to keep the promise that the same birthday always gives the same numbers.

## What I learned

- **Lunar conversion has a nationality.** The lunar calendar is an astronomical phenomenon, but the clock that cuts it into days is a country's standard time. If you serve Korean users a lunar calendar, check which country's calendar your library follows.
- **The edge cases were everything.** For most of a year, any converter agrees. The errors cluster at boundaries: a new moon just after midnight, a few minutes around a solar term. A handful of sample dates passes every test.
- **Exhaustive comparison is cheap and decisive.** Running a hundred years day by day needed no special equipment. Once the mismatches showed up in 30-day blocks, tracing the cause was quick.

The apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The figures come from my own comparison on November 8, 2026 of the old conversion code (a port of lunar_calendar_converter_new 2.0.0) and manseryeok 2.0.0 over the same period. New moon times are approximations from the Meeus new moon formula (accurate to a few minutes), and the Korean lunar calendar follows the KASI data carried by the library.
{: .prompt-info }
