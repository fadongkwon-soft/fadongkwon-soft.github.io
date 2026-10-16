---
title: Running Three AI Sessions in Parallel Did the Same Job Twice and Overwrote Each Other's Records — Why Session Management Stays With the Human
description: With six tasks on the day's list, I spun up three AI coding sessions in parallel. Then, as I gave each session its own instructions, one session restarted the tagging work another had already finished, they overwrote a shared record file, and one went beyond its brief into a build and release. Add a usage limit that froze two sessions, and this is the record of that day and the rules that came out of it
image:
  path: /assets/img/20261021_parallel-ai-sessions-collision/cover.png
  alt: Three parallel AI sessions colliding on the same work
date: 2026-10-21 09:30:00 +0900
categories: [Devlog, Automation]
permalink: /posts/parallel-ai-sessions-collision/
alt_url: /ko/posts/parallel-ai-sessions-collision/
tags: [automation, solo developer, dev log]
---

Last time I wrote about [how git gets tangled when several AI sessions share one repository](/posts/ai-sessions-shared-git/). The rule then was "don't commit while someone else is staging, and for shared files, change the working tree only and hand off." This time the problem was not git. **The work itself overlapped.**

## The day's list

As of the morning of October 16, six Play-related tasks were overdue: re-shooting screenshots, Japanese screenshots, rewriting the Japanese listings, three console-only jobs (tags, developer page, keyword suggestions), and resubmitting to a web portal. Too long for one session in sequence, so **I split it into three sessions**: screenshots, Japanese copy, console work. Each brief listed the files not to touch and the commit rules.

Up to there it was fine. The trouble came next.

## Overlap 1: the same tagging work, twice

The console session was stuck because the Chrome extension would not connect. Meanwhile I **finished the tagging work myself** from the parent session with the built-in browser. All 53 apps. But I had also told the console session to "try again," and it restarted the tagging that had been its job.

The result was two sessions touching the same console screens in the same time window. On nine apps the two sessions had chosen different tag combinations, and whichever applied later was what stuck. I had to reopen 14 apps to see which had survived. Fortunately both sets fit the genres, so nothing needed reverting, but **an hour went to verification.**

## Overlap 2: overwriting the record file

Tag results are recorded in `play-tags.csv`. The console session overwrote the record the parent session had committed with its own format and committed that, and only after being told did it restore the parent's content and append the five apps it had actually done. Three more commits, one of them a revert.

## Overlap 3: a session whose scope grew

The Japanese copy session was given listings only. Partway through, over Janggi, which the "skip apps under review" rule had excluded, I typed **"go ahead with what's left"** in that session's chat. The session read that as its whole to-do list, and rebuilt Janggi including a rules change sitting in the working tree, then submitted it to both Play and Toss.

That was not the session's fault. I had ordered that change in another session, and the session confirmed it with me before proceeding. But the parent session, not knowing this, raised a warning that "the rule has been reversed," and more time went into cross-checking. **When sessions know different things, the human has to be the messenger.**

## And then the limit

In the afternoon the usage limit hit. Two sessions stopped with "limit reached." The saving grace was that each had written its progress to a file before stopping, so once the limit reset the remaining steps could continue. The screenshot session had launched its captures as a separate process outside the session, so files kept accumulating even while the session was frozen.

## The rules that came out of it

- **Session management stays with the human.** The AI does not spawn sub-sessions on its own judgment. Whether to split, and into how many, is my call.
- **One task, one place.** Two sessions never touch the same console screen or the same record file at the same time.
- **Progress lives in one file.** Whichever session stops midway, the next one should be able to continue by reading that file alone.
- **Out-of-scope work stops and asks.** A phrase like "go ahead with what's left" can be read broadly. Outward-facing actions such as builds and releases get confirmed separately.
- **Long jobs run outside the session.** Anything that takes tens of minutes, like captures or builds, is detached so it survives a session cutoff.

## Summary

Parallel looks fast, but if checking the overlaps takes longer, it ends up slower. All six tasks did get done that day, but one session doing them in order would have finished in about the same time. From now on: **one session, in order, with only the long jobs moved outside.**
