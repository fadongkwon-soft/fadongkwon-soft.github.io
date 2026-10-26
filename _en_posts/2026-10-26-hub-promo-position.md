---
title: I Moved One Coordinate Instead of Rebuilding 43 Apps — Getting the Hubs into "You Might Also Like"
description: My apps introduce each other through a "You might also like" list at the bottom of the screen. I wrote a rule that puts the hubs at the top, but the 43 standalone apps already live on Apps in Toss predate it and need a rebuild to pick it up. Instead I moved only the hubs' place on the one-dimensional similarity coordinate every app carries, to the middle of the apps each hub contains. In simulation the number of apps whose own hub lands in the nearest five slots rose from 13 to 19 of 38, and the limit showed too, since one point cannot cover a widely spread group
image:
  path: /assets/img/20261026_hub-promo-position/cover.png
  alt: Moving hub positions on the similarity coordinate instead of rebuilding apps
date: 2026-10-26 22:31:00 +0900
categories: [Devlog, Automation]
permalink: /posts/hub-promo-position/
alt_url: /ko/posts/hub-promo-position/
tags: [apps in toss, hub app, cross promotion, solo developer, dev log]
---

My apps show a "You might also like" list at the bottom of the screen to introduce each other. There is no server: every app downloads one app list file from the site each time it starts. After the [hub conversion](/posts/toss-hub-conversion/), the hubs belong at the top of that list, because each hub holds a dozen similar games. This post records how far I could get toward that without rebuilding the apps.

## How the list is chosen

Every app carries one number between 0 and 999. It comes from computing similarity between apps by how much their tags overlap and then laying them out on a single line so that similar apps get nearby numbers. The list has ten slots.

- Five slots are the **five apps nearest** to my coordinate.
- Five slots are a **random pick fixed for the day** from the rest.

The new rule that lifts hubs to the top went into the code early on October 26. If there are hubs, all of them go on top, and the rest fills in as before. But the rule lives in each app's code, so only apps built afterwards carry it. All 43 standalone apps live on Apps in Toss were built before it.

## Why not rebuild

Rebuilding 43 apps means 43 reviews. The bigger problem is that the working tree also holds other changes that have not been verified yet, and a rebuild for a list rule would ship those along with it. So I chose to let each app pick the rule up at its next regular update.

While looking for something to do in the meantime, the user asked a question: "Instead of rebuilding everything, can't we just move the hubs' coordinates close to the similar apps?"

## Move only the hub coordinates

Under the old rule, hubs are chosen by coordinate distance like any other app. If a hub's coordinate sits in the middle of its apps, it lands in those apps' "nearest five". Only the nine hubs' numbers change. The distances between individual apps stay the same, so the similarity is not distorted.

If anything, this was a correction. The hub coordinates had been set by hand, and Daily Quiz sat at 790 while Daily Korean History, one of its own apps, was at 215. The hub was standing far away from the trivia apps it contains.

**Before** (registry apps.csv, relevant columns only)

```csv
id,…,pos
hub-edu,…,790
daily-history,…,215
```

**After**

```csv
id,…,pos
hub-edu,…,215
daily-history,…,215
```

The new coordinate is **the median coordinate of the hub's apps that are live on Toss as standalone apps**, because those apps' lists are exactly where the hub needs to appear. Using every app in the hub from the registry mixed in Play-only apps, pulled the center off, and gave a smaller effect in simulation.

| Hub | Before | After |
| --- | ---: | ---: |
| Puzzle Cafe | 727 | 666 |
| Brain Check | 478 | 377 |
| Arcade | 518 | 337 |
| Board Duel | 654 | 707 |
| Olympics | 391 | 307 |
| Lucky Lab | 940 | 946 |
| Daily Quiz | 790 | 215 |
| Lucky Pick | 148 | 153 |

## Simulation

For each standalone Toss app I computed the old rule's "nearest five" (two kids' apps are excluded because their list follows a different rule).

| | A hub anywhere in the five | Its own hub in the five |
| --- | ---: | ---: |
| Hand-set coordinates | 23 of 41 | 13 of 38 |
| Median of all apps in the hub | — | 15 of 38 |
| Median of the hub's Toss apps | 29 of 41 | 19 of 38 |

The other five slots are random, so hubs can still show up day by day in apps where they do not land in the nearest five.

## The limit

The coordinate is a single line, so a hub whose apps are spread widely cannot be covered by one point. Puzzle Cafe's apps run from 530 to 733, and Board Duel's sixteen board games from 629 to 716. With the hub in the middle, apps at either end have other similar apps closer by, which fill the five slots first. Nineteen apps, including Reaction, Tap Bird, 2048 and Janggi, fall into this group, and for them the hub only reaches the top once a build with the new rule ships.

## Keeping it through recomputation

The coordinates are recomputed by a script whenever tags change or apps are added. A hub coordinate fixed by hand would vanish at the next run. So I turned the rule, "a hub's coordinate is the median of its Toss apps' coordinates", into a small script that the recomputation script calls at the end. New hubs will not need hand-set values either.

**After** (core of registry/hub-pos.py)

```python
def apply(rows, header):
    col = {k: i for i, k in enumerate(header)}
    pos = {r[col["id"]]: r[col["pos"]] for r in rows}
    toss = {r[col["id"]] for r in rows if r[col["toss"]].strip() == "1"}
    for hub, games in hub_members().items():        # games listed in hubs/<id>/hub.json
        live = [g for g in games if g in toss]       # member apps live on Toss on their own
        ms = [int(pos[g]) for g in (live or games) if pos.get(g, "").isdigit()]
        if hub in pos and ms:
            set_pos(rows, hub, int(statistics.median(ms)))   # hub coordinate = median
```

```python
# end of compute-pos.py — after re-placing everything by tags, overwrite only the hubs
subprocess.run([sys.executable, os.path.join(HERE, "hub-pos.py")], check=True)
```

Before this there was no such step. The recomputation script placed hubs by their tags like everything else, and any hand-set value was overwritten on the next run.

## One dedicated card outside the list

One more thing got fixed along the way. The four lotto apps show a separate card under the "my luck" result that leads to [Save Instead of Lotto](/posts/lotto-saving/). On Toss, that app now lives inside the Lucky Lab hub and has dropped out of the list as a standalone app. The card was set to appear only when that app is on Toss, so it disappeared entirely. Now Lucky Lab takes its place and the card opens the hub.

**Before** (findSavingsApp in the promo package)

```ts
const app = csv ? parseAppsCsv(csv).find((a) => a.id === SAVINGS_APP_ID) : undefined;
if (!app || !(platform === 'toss' ? app.toss : app.play) || !supportsLang(app, lang)) return null;
return app;
```

**After**

```ts
const all = csv ? parseAppsCsv(csv) : [];
const ok = (a: PromoApp | undefined): a is PromoApp =>
  !!a && (platform === 'toss' ? a.toss : a.play) && supportsLang(a, lang);
const app = all.find((a) => a.id === SAVINGS_APP_ID);      // 'lotto-saving'
if (ok(app)) return app;
const hub = all.find((a) => a.id === SAVINGS_HUB_ID);      // 'hub-fortune'
return ok(hub) ? hub : null;
``` This is app code, so it ships with the lotto apps' next builds.

## Summary

- The rule that lifts hubs to the top is in the code, but the 43 apps already out get it at their next build.
- In the meantime I did what data alone could do: moving hub coordinates to the middle of their apps raised the apps whose own hub appears near the top from 13 to 19.
- The coordinate is one-dimensional, so it cannot cover widely spread groups. That part is solved by builds in the end.
- Hand-set values get wiped by recomputation, so the rule now lives in a script.

The apps are listed under [GAMES](/games/) and [APPS](/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> The figures are simulation results from the registry as of October 26, 2026. The actual list differs a little each day because of the daily random slots.
{: .prompt-info }
