---
title: Why I Shelved My Festival Calendar App — I Should Have Counted the Data's Future Before Building It
description: "I finished building a festival calendar app on Korean public data for my Weekend Life hub, then found that only 36 of its 1,095 festivals were still ahead. This post covers a dataset that gains rows only after festivals end, the stop criterion I had written into the design doc, how I tested an AI agent's suggestion to fill the calendar with last year's dates against 74 pairs of the same festival and withdrew it, and the switch to a recreation forest map. The point is to count rows dated after today, not rows in total"
image:
  path: /assets/img/20261118_festival-calendar-dropped/cover-en.png
  alt: "Why I shelved my festival calendar app"
date: 2026-11-18 23:38:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/festival-calendar-dropped/
alt_url: /ko/posts/festival-calendar-dropped/
tags: [travel, korea travel, app development, solo developer, dev log]
---

On November 13 I finished a festival calendar app and decided not to ship it. Every screen was there, and type checks, tests, the build and my pre-launch checks all passed. The problem was not the code but the **dates** in the data. Almost no upcoming festivals were in it.

This post covers why I built it, what made me shelve it, and how I tested and threw out the alternative that came up just before I did. The numbers were re-checked against the app folder's status doc (`games/festival-calendar/STATUS.md`), its data report and that day's session log.

## What I set out to build

Weekend Life is a hub app that gathers tools for weekends into one place (the [intro post](/posts/hub-weekend/) describes its first lineup). The planning doc compared three candidates for a new tool, and my first pick was a festival calendar.

| | Festival calendar (pick) | Recreation forest map (fallback) |
|---|---|---|
| Core screens | This weekend's festivals → calendar → details → visited stamps | Region / nearby → details (fees, facilities) → stamps |
| Reason to come back | The list changes every week ("this weekend") | Collecting stamps (weak) |
| Data | Public Data Portal, "National Cultural Festival Standard Data" | Public Data Portal, "National Recreation Forest Standard Data" |
| Difficulty | Medium (add a date axis) | Low |

I picked the calendar because its list changes every week. Once you have seen the forests, you are done, but festivals open every weekend. I expected to reuse the region, nearby and stamp structure of my [museum map](/posts/museum-map/) almost unchanged and just add a date axis.

Looking back, the planning doc already carried a one-line warning: "Local governments update on different schedules, so some festivals will not have this year's dates yet." But I wrote the response as "show past dates labeled as last year's timing" and moved on. I wrote that some would be missing. I never counted **how many**.

## Cleaning the data: from 1,372 rows to 1,095

An AI agent did the implementation. It downloaded the source from the public download endpoint (no key needed) and built the bundle with a cleaning script.

| Step | Rows | Rule |
|---|---:|---|
| Source | 1,372 | Downloaded 2026-11-13 |
| Excluded | -23 | 2 with an end date before the start date, 21 running longer than 120 days |
| Duplicates | -52 | Same name and same start date: keep only the row with the latest reference date |
| Same festival across years | -202 | Strip "Nth edition" and the year from the name, group with the district into one id, keep the latest edition and store the previous date separately |
| **Bundle** | **1,095** | 211 rows without coordinates kept, coordinates left blank |

I dropped rows longer than 120 days on the theory that they were year-round events entered as festivals. But that rule also dropped genuine long-running events: 8 of the 21 source rows overlapping this weekend fell out because of it (long theater festivals, puppet festivals, walking tours and the like). Whether to keep that rule was left undecided.

I also spot-checked. I took five festivals from this weekend's list and compared their start date, end date and venue with the source rows, and all five matched. The data was not wrong.

## Why the agent stopped: the future was empty

After finishing the implementation, the agent reported its gate results along with "the data does not match the design's assumptions." Split by date as of that day (Nov 13):

| Group | Rows |
|---|---:|
| Whole bundle | 1,095 |
| Past | 1,050 |
| In progress | 9 |
| Upcoming | 36 |
| Overlapping this weekend (Nov 14–15) | 13 |
| Next 30 / 90 days | 28 / 42 |

By start month, the 36 upcoming festivals were 15 in November, 14 in December, 4 in January 2027, 1 in February, 1 in August and 1 in October. The past was dense by comparison: 228 in October, 128 in September.

The cause was how the data accumulates. Local governments often upload a year's festivals **after they end**, so the past is dense and the future is empty. People open a calendar app to see next month, and from next month on it was nearly blank.

The design doc had a line for exactly this: "If there are fewer than 10 upcoming festivals in a month, report mid-implementation (the basis for deciding on the fallback, the recreation forest map)." Every month from December on fell under it. Because the agent brought that criterion back instead of stopping at "gates passed," I could stop before moving on to launch prep.

## The AI agent's suggestion, and my pushback

In that report, the AI agent leading the session recommended reinforcing the app, not shelving it. The gist:

> Most local festivals happen around the same time every year, so fill the future calendar cells with "festivals held around this time last year" in a faded style and add "This year's schedule has not been posted yet."

The argument was that the 1,050 past rows would become useful and the calendar would stay full all year. I asked back whether last year's dates would hold, since they are past data and this year is likely to differ. And I asked whether the forest map was a new idea it had just come up with.

The second answer was in the record. The forest map was not new: the original planning doc listed it as the fallback, "if the festival calendar is blocked, the recreation forest map." The first question I answered with data.

## Do last year's dates hold this year? Measured on 74 pairs

Collecting festivals that had both a previous and a latest edition date gave 74 pairs. I moved the previous date into the same year as the latest one and counted the difference in days.

| Difference | Pairs | Share |
|---|---:|---:|
| Within 3 days | 36 | 48% |
| Within 7 days | 49 | 66% |
| Within 14 days | 63 | 85% |
| Within 30 days | 71 | 95% |
| More than 30 days | 3 | 4% |

The median was 5 days. The gap between the two editions was one year for 66 pairs, two years for 6 and three years for 2.

"Roughly which month" holds up well: 95% land within 30 days. But this app is about "this weekend," and only half the pairs landed within 3 days, close enough to pick the right weekend. One in three was off by more than a week. On top of that, about 300 of the past rows were from before 2025, with no way to filter out festivals that had since ended or moved to every other year. With only 74 pairs these shares are a rough guide, but that accuracy was not acceptable for a calendar.

Seeing these numbers, the agent withdrew its recommendation, noting that it "was a judgment made before seeing the numbers above." The decision: shelve the festival calendar and switch to the fallback, the recreation forest map.

## How I shelved it

I did not delete anything. The app folder and store assets stay, and a "shelved" section went at the top of the status doc:

- **Do not ship.** Remove it from hub inclusion, build config and registry work.
- **Reason**: almost no future data. The reinforcement idea (a last-year's-timing calendar) was dropped after the 74-pair check.
- **When to revisit**: at each quarterly data refresh, if the monthly "upcoming" count is in the dozens or more for each of the next three months, raise it for review. Until then, do not propose shipping it.

That same evening I built the recreation forest map on the same structure. It holds 169 forests after merging duplicates from 186 source rows, and it passed the gates. Forest data has no dates, so this kind of problem cannot happen. The planning doc's note that its reason to come back is weak still stands.

## What I learned

- **Count rows dated after today, not total rows.** 1,095 looked like plenty, but what the app would actually show was 36. For dated data, a table of future rows by month takes a few minutes at the planning stage. I made it after building the app.
- **If you write "some will be missing," write the share too.** The risk was in the planning doc, but without a size. A risk with no size slips through whenever its mitigation sounds plausible.
- **Write the stop criterion as a number, in the design doc, in advance.** The single line "report if fewer than 10 upcoming in a month" is why the implementing agent stopped, and it made shelving a matter of checking a criterion rather than a feeling. Having the fallback written down in advance sped up the decision too.
- **Test recommendations against data, and withdraw them when they fail.** "Fill it with last year's timing" sounded reasonable, but measured, it was right to the weekend only half the time. Whether the idea comes from an AI agent or from my own hunch, measuring accuracy against the app's core use was the cheapest check available.
- **Shelve, do not delete.** With the revisit condition written down as a number, a data change next quarter will not mean starting the decision from scratch.
