---
title: "Three Agents That Work Every Night: Toss Reviews, Google Indexing, and Threads"
description: "How we automated three daily solo-dev chores—collecting Toss app reviews, submitting Google Search Console indexing requests, and posting app promos to Threads—using Antigravity scheduled sidecars with least-privilege access grants."
image:
  path: /assets/img/20261126_midnight-automation-agents/cover.png
  alt: "Three scheduled Antigravity automation agents"
date: 2026-11-26 01:20:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/midnight-automation-agents/
permalink: /posts/midnight-automation-agents/
tags: [automation, indiedev, devlog]
---

Once you maintain over 100 apps as a solo developer, daily operations drain more energy than coding. Checking the Toss console for new reviews, clicking "Request Indexing" in Google Search Console up to the daily quota, and posting unpromoted apps to social media each eat 10 to 20 minutes every single day.

Since mid-November, we moved all three routines into **Antigravity scheduled automations (sidecars)** managed from a single installer script (`install_automations.py`) and three self-contained prompt files.

## 1. The Three Daily Agents

All three run on `Asia/Seoul` cron schedules under `~/.gemini/config/sidecars/<id>/sidecar.json`:

| ID | Schedule | Job | Tools Used |
|---|---|---|---|
| `daily-threads-posts` | 00:00 daily | Pick unposted top-performing apps and publish videos/images to `@fadongkwon.soft` on Threads | `threads_picker.py`, `threads_post.py` |
| `daily-toss-reviews` | 00:03 daily | Scrape ratings and reviews across all Toss mini-apps into `revenue-ledger` and rebuild the dashboard | `chrome-devtools` MCP, `toss_reviews.py`, `dashboard.py` |
| `gsc-daily-index-requests` | 18:11 daily | Work through the `fadongkwon.com` unindexed URL queue in Search Console until the daily quota | `chrome-devtools` MCP, `gsc_rec.py`, `tools/gsc.py` |

Because each scheduled run starts with zero conversation history, every prompt under `prompts/<id>.md` specifies the exact steps, stop conditions, and output paths.

## 2. Why Agents Instead of Plain Cron Scripts

Everything deterministic stays in plain Python (`toss_reviews.py`, `threads_picker.py`, `gsc_rec.py`). The agent only bridges the parts where **no official API exists and web console UIs shift over time**:

- Toss review pages and Search Console's "Request Indexing" button require an authenticated browser session.
- Using `chrome-devtools` MCP against a dedicated Chrome profile, the agent reads DOM snapshots, handles minor UI changes or dialogs, and hands structured results back to Python scripts.

## 3. Least-Privilege Isolation via `access_grants`

Unattended jobs need strict guardrails. Each `sidecar.json` whitelists only the exact directories, commands, and URLs required:

- **`daily-toss-reviews`**: read/write `revenue-ledger`, access `apps-in-toss.toss.im`, run only three ledger scripts.
- **`gsc-daily-index-requests`**: read the blog repo, write only to `tools/out`, access `search.google.com` and `fadongkwon.com`.
- **`daily-threads-posts`**: write only inside `antigravity-automations` and run the picker/poster scripts.

The installer defaults to a dry run and requires `--write` to emit configs, and automations still have to be toggled on manually in the dashboard.

## 4. The Payoff

The biggest win has been tightening the feedback loop: reviews scraped at 00:03 show up on the morning dashboard automatically, which is how a single 4-star review turned straight into [our Gomoku beginner AI update](/posts/gomoku-beginner-ai-from-review/).
