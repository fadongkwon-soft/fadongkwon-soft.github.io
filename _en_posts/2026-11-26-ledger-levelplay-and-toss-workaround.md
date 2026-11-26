---
title: "Wiring Unity LevelPlay Into Our Revenue Ledger and Bypassing Toss Report Timeouts"
description: "How we added Unity LevelPlay v6 reporting with daily USD-to-KRW FX caching to our local ledger, and switched Toss IAA collection to per-app queries with rate-limit backoff after workspace-wide reports started timing out."
image:
  path: /assets/img/20261126_ledger-levelplay-and-toss-workaround/cover.png
  alt: "Revenue ledger LevelPlay API and Toss per-app collector"
date: 2026-11-26 01:28:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/ledger-levelplay-and-toss-workaround/
permalink: /posts/ledger-levelplay-and-toss-workaround/
tags: [automation, api, apps-in-toss, indiedev, devlog]
---

Just days after [removing headless AI from our Toss ledger collector](/posts/ledger-without-headless-ai/), our local `revenue-ledger` needed two more upgrades: pulling stats from our new **Unity LevelPlay** mediation account, and fixing persistent timeouts on Toss's workspace-wide ad report. *(As usual, we share the architecture and code patterns without disclosing revenue figures.)*

## 1. `levelplay_fetch.py`: Pulling LevelPlay v6 Stats Into a KRW Ledger

- **Token exchange**: Reads gitignored `Secret Key` and `Refresh Token` from `levelplay_api.json` and requests a bearer token from `platform.ironsrc.com/partners/publisher/auth`.
- **14-day window through yesterday**: Calls `mediation/applications/v6/stats` up to yesterday so daily totals stay aligned across platforms (today's in-progress UTC numbers print only to the console unless `--today` is passed).
- **Daily USD → KRW cache**: Fetches the USD/KRW rate once per day from `open.er-api.com/v6/latest/USD` into `fx_usd_krw.json`, falling back to the last cached rate or `1400.0` if offline.
- **Unified app names**: Maps each `appKey` and Play `bundleId` via `levelplay-*.properties` and `apps.csv` so Toss and Play rows merge cleanly under one display name.

## 2. Making Toss Per-App Fetching the Default

As our Toss mini-app count grew, `iaa_workspace_dashboard_report_v2` began timing out consistently after 60 seconds. Previously, `toss_fetch.py` wasted a minute waiting for the workspace report to fail before falling back.

In commit `b61159e`, we made per-app querying (`fetch_per_app`) the default and hardened `toss_mcp.py`:

- Lowered default concurrency (`TOSS_MCP_PARALLEL`) from **4 to 2**.
- Classified JSON-RPC rate-limit phrases (`Too Many Requests`, `rate limit`, Korean equivalents) as `TransientError` instead of fatal `RpcError`.
- Bumped retries from **3 to 4** with `(2, 5, 10)`-second backoff.

## 3. Refreshing Every Platform With One Command

Now a single `update.cmd` run refreshes Toss IAA, Unity LevelPlay, promotions, reviews, and the HTML dashboard without manual intervention. Adapting to a new ad network only required swapping in one collector module rather than rebuilding the pipeline.
