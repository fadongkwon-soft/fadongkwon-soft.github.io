---
title: "Moving a 100-App Solo Studio to a New PC and Antigravity: Our Handoff Playbook"
description: "How we migrated 7 repositories, 120+ app configs, signing keystores, 3 scheduled automations, and operating rules to a new PC running Antigravity without breaking builds or leaking secrets."
image:
  path: /assets/img/20261126_new-pc-antigravity-migration/cover.png
  alt: "Solo studio PC and Antigravity migration handoff"
date: 2026-11-26 01:24:00 +0900
categories: [Devlog, Retrospective]
pin: false
alt_url: /ko/posts/new-pc-antigravity-migration/
permalink: /posts/new-pc-antigravity-migration/
tags: [workflow, android, automation, indiedev, devlog]
---

Migrating a solo studio with over 100 apps to a new PC is never just `git clone`. Alongside seven repositories, you have upload keystores, 120+ gitignored ad config files, service-account JSONs, wireless ADB keys, scheduled automations, and months of hard-won operational rules.

On November 20, we moved our entire workflow to a new PC running **Antigravity** using a dedicated handoff document (`antigravity-handoff-new-pc-2026-11-20.md`). Here is the checklist that kept the move smooth.

## 1. Start With a Read-Only Verification Prompt

Before building anything on the new machine, we ran a read-only audit prompt to produce a status table:

1. **All 7 core repositories**: `.claude`, `apps-in-toss`, `apps-in-toss-games`, `quiz-apps`, `revenue-ledger`, `tarot-content`, and `fadongkwon-soft.github.io`.
2. **Secrets & signing keys (existence only—never print contents)**: `.jks` keystores, `keystore.properties`, 121 `admob-*.properties` files, `play_service_account.json`, OAuth tokens, `.env`, and `.git/hooks` secret-scanning hooks.
3. **Toolchain health**: `git`, Node 24 + `pnpm`, Python 3.14, `ffmpeg`, `adb`, `checklist_state.py`, `play.py`, and Gradle sync.
4. **Automations & MCP**: 3 scheduled sidecars under `~/.gemini/config/sidecars/` and `apps-in-toss-console` MCP.

## 2. Three Windows Build Traps to Fix Immediately

- **Gradle 8.11.1 vs. JBR 25**: Bundled JBR 25 breaks Gradle 8.11.1; pinning `JAVA_HOME` to JDK 18 fixes it.
- **Stale `local.properties` SDK path**: The old machine had a sandboxed SDK path. Pointing `local.properties` and `ANDROID_AVD_HOME` to clean host paths prevented silent build failures.
- **PowerShell 5.1 UTF-8 BOM**: Always run Python with `-X utf8` and avoid BOM-writing cmdlets on Jekyll pages or wrapper scripts.

## 3. Carry Over Operating Rules Explicitly

A new agent environment forgets past lessons unless you write them down:

- Never run `git add -A` or `git add .`—stage explicit paths and check `git diff --cached --stat`.
- Never push `--no-verify`; never disclose exact revenue numbers in public posts.
- Always rerun `hub-build` before building Play hub AABs (Toss wrapper builds overwrite `dist-hub`).
- Clear division of labor: the agent handles builds, checks, and submissions; the human handles physical-device checks, final Toss Console publish clicks, and third-party signups/payments.

## 4. Lock In P0–P3 Priorities Before Day One

Having a written P0–P3 queue (uncommitted cleanup → policy deadlines → 114-app approval check → LevelPlay pilot → unreleased 7 apps) let us jump straight into shipping the LevelPlay pilot the very next day.
