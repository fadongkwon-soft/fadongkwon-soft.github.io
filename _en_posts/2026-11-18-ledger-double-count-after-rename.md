---
title: I Turned Apps Into Hubs and My Ledger Counted the Same Day Twice — When the ID Stays, the Name Changes, and a Refetch Rewrites the Past
description: The day after converting nine Apps in Toss apps into hubs with an app info change, I found that in my revenue ledger four non-game hubs had the same day's revenue counted twice, once under the old name and once under the hub name, while five game hubs showed up under the wrong name. The internal ID never changed, the ledger's name table mapped one ID to one name, and every collection run re-downloads the last 14 days. Here is how a hub table with switch dates and a date-aware name function fixed it, how 2,441 rows became 2,408, and why names need validity periods
image:
  path: /assets/img/20261118_ledger-double-count-after-rename/cover-en.png
  alt: "Renamed into hubs, counted twice"
date: 2026-11-18 23:33:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/ledger-double-count-after-rename/
alt_url: /ko/posts/ledger-double-count-after-rename/
struct_exempt: [images]
tags: [revenue, apps in toss, hub app, automation, solo developer, dev log]
---

On October 26, I turned nine apps already live on Apps in Toss into hubs. The 50-app workspace cap meant I could not register the hubs as new apps, so I took the long way: an app info change that swaps an existing app's name, icon and bundle. That story is in [Moving Hub Apps onto Apps in Toss](/posts/toss-hub-conversion/).

One thing could not change in that conversion: the internal identifier Toss uses for an app (its appName). Even when the app my ledger called "Nursing Assistant" became the "FDK Certification" hub, the console and the API still know it as `nursing-quiz`.

This post is about how that "same ID, new name" tangled my revenue ledger the very next day. No amounts are included.

## The trigger: apps whose pairs no longer matched

On the evening of October 27, with a burst of new launches, some apps on my dashboard looked like their Toss and Play halves had come apart, so I had an AI agent audit the ledger. The ledger groups each app's Toss rows and Play (AdMob) rows under the same name and shows them as one line. If the names differ, one app splits into two lines.

The audit found that the mismatches came not from the new launches but from the previous day's hub conversion. And it was not just awkward to read: in some places **the same day's revenue had been counted twice.**

## Digging in: how the ledger handles names

### The name is part of the row key

The ledger (`ledger.csv`) overwrites rows keyed by date, platform and app name.

```python
def upsert(records):
    ...
    for r in records:
        k = (r['date'], r['platform'], r['app'])
        ...
        rows[k] = r
```

The Toss API reports revenue by appName, not by display name. So the collector used a name table (the `toss` section of `apps.json`) to turn each appName into a display name before writing it. That table mapped **one appName to one name**, and it knew nothing about dates.

```python
yield dict(date=d['date'], platform='toss', app=alias.get(app, app), ...)
```

### Every run re-downloads the last 14 days

Toss fills in the previous day's revenue gradually into the next morning, and values from a few days back can still change. So the collector re-downloads the whole last 14 days every time and overwrites them. Normally that is a strength. Run it as often as you like and the result is the same, and late values get picked up on their own.

Those two facts met the hub conversion, and the symptoms split two ways.

| Group | Name table state | What happened on refetch | What the dashboard showed |
|---|---|---|---|
| Four non-game hubs (certification, party, daily trivia, luck lab) | Switched to the hub name on conversion day | The previous 14 days (10/12 to 25) of the individual app's revenue came in **as new rows** under the hub name key. The rows under the old name key stayed | The same day's revenue, once on each of two lines |
| Five game hubs (puzzle cafe, brain age, arcade, head-to-head, olympics) | Still the individual app names | Hub revenue after 10/26 landed under the individual app names | The olympics hub looked Play-only, Pixel Pong looked like Toss plus Play |

The first row is the heart of it. The moment the name table switched to the hub name, the collector wrote every one of that appName's last 14 days under the new name. Since the name is part of the key, the new-name rows were "new rows," and nothing deleted the old-name rows. The refetch did not **correct** the past; it **wrote a second copy** of it.

The same thing happened in the review ledger. Five Nursing Assistant reviews collected in August had been added again under the hub name.

The second group is the same problem in the opposite direction. With the name table not yet switched, Toss revenue earned after the switch piled up on the individual app lines. One more detail: at that point the five game hubs had only their app info changed, and the updated bundles were still in review. So Toss revenue arriving under the olympics hub name after October 26 was in fact earned by the old Pixel Pong bundle. Name and content were out of step by a day.

## The fix: names now carry a switch date

The direction was clear. The name table needed to know dates. Use the hub name only from the day the appName moved to the hub, and the old name for earlier dates.

### 1. A hub table with switch dates

I added a `toss_hub` section to `apps.json` with the switch date and hub name for all nine. The existing `toss` table went back to the old individual app names.

```json
"toss_hub": {
  "nursing-quiz":  { "since": "2026-10-26", "name": "파동권자격증" },
  "juice-spinner": { "since": "2026-10-26", "name": "파동권복불복" },
  "pixel-pong":    { "since": "2026-10-26", "name": "파동권올림픽" },
  ...
}
```

(The names are the Korean display names of the certification, party and olympics hubs.)

### 2. A name function that takes a date

I added `toss_name()` to the shared library.

```python
def toss_name(cfg, app, date):
    """토스 appName 의 그날 표시명. 허브로 넘어간 appName 은 전환일(toss_hub.since)부터 허브 이름, 그 전은 옛 이름.
    토스 수집은 최근 14일을 다시 받아 덮어쓰니, 이름을 날짜와 무관하게 바꾸면 전환 전 수익이 허브 행으로 옮겨 가고
    옛 이름 행도 남아 이중으로 잡힌다(10/27 파동권자격증·간호조무사 10/12~24)."""
    h = cfg.get('toss_hub', {}).get(app)
    if h and (date or '')[:10] >= h['since']:
        return h['name']
    return cfg.get('toss', {}).get(app, app)
```

(The docstring says: the display name of a Toss appName on a given day. An appName that moved to a hub uses the hub name from its switch date and the old name before it. Because collection re-downloads 14 days, changing a name regardless of date drags pre-switch revenue onto the hub row while the old-name row stays, counting it twice.)

### 3. Applied to all three Toss collectors

Revenue was not the only place that used the name table. Reviews and promotions had the same bug hiding in them, so I changed all three at once. Each uses a different date as its reference.

| Collector | Before | After | Reference date |
|---|---|---|---|
| Toss ad revenue | `alias.get(app, app)` | `toss_name(cfg, app, d['date'])` | Revenue date |
| Toss reviews | One fixed name per app | `toss_name(names, app_name, it.get('createdAt'))` | Review timestamp |
| Promotion list | `alias.get(appName)` | `toss_name(cfg, appName, registration time)` | Promotion registration time |
| Promotion funnel | `alias.get(app_name)` | `toss_name(cfg, app_name, today)` | Today (it is a period total) |

The Play side needed nothing separate. On Play, individual apps and hubs are different packages, so the individual packages already kept their old names and the hub packages already had hub names. The one tweak was in the function that builds the name table: where a hub row in the app registry had inherited the Toss slot, it now checks the hub name first so that row is not dragged back to the old individual app name.

### 4. Cleaning up what was already there

Changing the function does not remove duplicate rows already in the ledger. I traced the old and new names of all nine conversions back to their appName, renamed each row by its date, and kept a single row wherever two rows now shared a key.

| File | Before | After | What changed |
|---|---|---|---|
| Revenue ledger | 2,441 rows | 2,408 rows | 39 row names corrected, 33 duplicate rows removed, total down about 0.04% |
| Review ledger | 48 rows | 43 rows | 5 duplicate August reviews removed |
| Promotion ledger | 838 rows | 838 rows | App name changed on 2 hub promotion payout rows from 10/26 |

What the total lost is exactly what had been counted twice. The individual apps did not earn much before the switch, so the share was small. Still, when you trust the ledger to read per-app trends, duplicates like these create the illusion that "the hub earns well right after the switch." After the cleanup, the dashboard shows "Nursing Assistant" (Toss plus Play) through October 25 and the certification hub (Toss) from October 26.

The fix went into the ledger repository as a single commit that same night (8:52 p.m. on October 27). If another hub conversion comes along, it takes one more line in `toss_hub`. Right now the table holds the nine conversions from October 26.

## Apps that are fine showing on one side only

Not every app that looked like a broken Toss and Play pair was a defect. Writing these down makes the next audit faster.

- **Play only**: apps not yet on Toss because of the workspace cap.
- **Toss only, hubs**: the four non-game hubs whose Play versions had not launched yet at the time.
- **No Play revenue line**: apps with a Play name entry but no Play ad revenue yet, so no rows exist.

## What I learned

- **Group things whose ID is fixed but whose name changes by name, and a refetch rewrites the past.** An idempotent refetch is only safe on the premise that the same key means overwrite. Put a value that can change into the key, and overwriting turns into duplicating. Where possible, key on the ID and attach the name at display time.
- **Give names a validity period.** Write it as "this ID has this name from this date to that date," and re-fetching any date before or after a switch gives the same answer. Overwriting the name table only remembers the latest switch.
- **Find every place that reads the name table.** Had I fixed only revenue, the five duplicate reviews would still be there. Everything that reads the same dictionary carries the same bug.
- **The reference date differs by data.** Revenue uses the day, reviews the time written, promotions the time registered, and period totals today. Deciding only "go by date" lets you get it wrong again on which date.
- **Write down what the platform will not change for you first.** When I wrote the hub conversion post I knew that "appName stays the same," but what that meant for my own ledger I learned a day later. When I make a change on the platform side, I now look at the list of my own tools that use that ID as a key.

The structure of the ledger itself is in [Checking 27 Apps by Hand Every Morning, Until I Built a Ledger](/posts/revenue-ledger-dashboard/) and [The Revenue Ledger, Three Weeks On](/posts/revenue-ledger-update/), which also covers the first pass at unifying Toss and Play names. News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The row counts and dates in this post come from the ledger repository's commit on October 27, 2026, the cleanup script's output and my work logs.
{: .prompt-info }
