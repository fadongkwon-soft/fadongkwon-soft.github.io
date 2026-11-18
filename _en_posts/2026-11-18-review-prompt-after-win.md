---
title: "One-Star Reviews Suddenly Piled Up — So the Rating Prompt Now Waits for a Win"
description: "Three text-less one-star reviews landed on my Toss Gomoku mini app within three days. Lining the review dates up against traffic showed they fell on the three heaviest days of a growth-program inflow, and the shared rating gate was asking for a rating 1.5 seconds after every result screen, win or lose. This is how I changed the contract so each game passes good or bad and losses never trigger the prompt, rolled it into 65 games, and why I still cannot show the effect in numbers"
image:
  path: /assets/img/20261118_review-prompt-after-win/cover-en.png
  alt: One-star reviews suddenly piled up — the rating prompt now waits for a win
date: 2026-11-18 23:31:00 +0900
categories: [Devlog, Troubleshooting]
permalink: /posts/review-prompt-after-win/
alt_url: /ko/posts/review-prompt-after-win/
tags: [apps in toss, toss, in-app review, gomoku, solo developer, dev log]
---

On the morning of November 6 I was scrolling through the reviews of my [Gomoku](/posts/gomoku/) mini app on Toss when the one-star ratings jumped out. Two on November 2, one on November 4. All three were stars only, no text. Gomoku launched in September, and until then it had never received a single one-star review.

My first thought was simple: "Are people losing to the AI and rating it one star out of spite?" This post starts from that suspicion, follows the data to what looks like the actual cause, and ends with a change to the shared rating gate so that it only asks after a good result. To be upfront: I never managed to confirm the first suspicion, and I cannot yet show in numbers that the change worked. I still think the reasoning and the process are worth writing down.

The rules I set when I first added the rating prompt are in [When to ask for a review](/posts/review-prompt-toss-play/). This post is about one condition those rules were missing.

## Lining up review dates with traffic

First I listed every Toss review of Gomoku from my ledger, a tool that pulls reviews from the console every day and keeps them in a CSV. The dividing line is 11:00 on October 26, when Gomoku entered the [Apps in Toss growth program](/posts/toss-growth-program-gomoku/).

| Period | Reviews | 1 star | 2 stars | Note |
|---|---:|---:|---:|---|
| 10/7–10/25 (before the program) | 8 | 0 | 0 | lowest was a single 3 |
| 10/26–11/5 (during the program) | 9 | 3 | 1 | all four 1–2 star reviews had no text |

The three one-star reviews came in around 11 a.m. and 10 p.m. on November 2 and around 7 p.m. on November 4. The two-star review was on November 3. I laid those dates over the daily "incoming users" numbers from the growth program's performance screen.

| Date | Program inflow (all) | New users | Gomoku 1–2 star reviews that day |
|---|---:|---:|---|
| 10/31 | 2,272 | 2,183 | - |
| 11/1 | 2,565 | 2,415 | - |
| 11/2 | 2,837 | 2,656 | two 1-star |
| 11/3 | 2,732 | 2,509 | one 2-star |
| 11/4 | 3,040 | 2,763 | one 1-star |
| 11/5 | 1,087 | 968 | - (budget ran out at 10:53) |

The low ratings arrived on November 2–4, the three days with the most new users out of the program's eleven. The last Gomoku bundle before that went live at 9 p.m. on October 28, so there was no release that could have suddenly broken something on November 2.

## The people coming in were not there to play

Growth-program traffic comes in through paths like "browse a mini app and get 5 won" on the Toss benefits tab. Stay a moment, collect the reward. These are not the same people as regular players, and the console metrics showed it plainly.

| Metric | Before (10/19–25) | During (10/26–11/4) |
|---|---:|---:|
| Average session length | 140–223 s | 45–64 s |

On November 2 alone there were 4,518 game-start events and 2,121 game-end events. More than half of the games that started were closed before they finished.

There was also a control. [Tap Bird](/posts/toss-growth-program-tap-bird/) entered the same program on the same day at the same scale. It also took in more than 2,000 new users a day on November 2–4, yet my ledger recorded zero Tap Bird reviews during the whole program. So the difference between the two apps was not the traffic but what happened inside the app.

## When the rating prompt was firing

So I reread the shared gate that requests the rating dialog. My mini games live in one monorepo and share packages, and the decision to ask for a rating is made in one place, `packages/platform/src/review.ts`. Every game calls `pushConsent.noteRun()` when a round ends, and that call evaluates both the push-consent sheet and the rating gate.

At the time, the gate looked like this.

| Condition | Value |
|---|---|
| Total plays | at least 5 |
| Days used | at least 2 different days |
| This session | from the 2nd play (a sheet right after entry is a review rejection reason) |
| Timing | 1.5 s after the result screen is drawn |
| Spacing and cap | 60 days after a request, at most 3 per device |
| Outcome (win or loss) | **not considered** |

The last row was the problem. Win or lose, once the conditions were met, Gomoku asked Toss for a rating 1.5 seconds after the result screen. Toss decides on its own, under its fatigue policy, whether to actually show the dialog, but the request was going out right after losses too.

I also looked at who could meet those conditions. Of the program inflow, "all minus new" — people coming back — was 180 to 280 a day on November 2–4. They are the candidates for the two-day, five-play condition. On October 27 I had changed Gomoku's first screen to drop you straight into a game, so the app was built to take people from entry to a result screen quickly. That likely made them rating-prompt candidates more easily.

## The first suspicion stayed unconfirmed

At this point "people who just lost saw the rating dialog and gave one star" sounds plausible. But to confirm it I needed the win, loss and difficulty breakdown of program traffic. Gomoku logs an event with `result` and `diff` parameters at the end of every game, so the data existed.

There was just no way to get it out.

- The console query tool (MCP) returns daily counts per event and a list of parameter names, but no breakdown by parameter value.
- I had an AI agent go through the console's web screens read-only. The event screen also showed only daily counts, and there was no per-value aggregation anywhere.
- The remaining option was to create a new conversion metric with a `result=lose` condition under "Core metrics" and read it a day later. That changes console settings, so I did not do it.

And none of the three one-star reviews had text, so there is no way to ask the reviewers why. What I can actually claim as cause is this: the ratings coincided with the inflow peak, that inflow had short sessions and left games unfinished, and the rating prompt was being requested regardless of outcome. "They were angry about losing" stays an unconfirmed hypothesis.

One more thing worth noting: other games also got text-less one-star reviews in the same period, one for Quick Go on November 1 and one for Sequence Memory on November 3. That suggests this was not unique to Gomoku, and fixing it meant changing the shared gate, not just one game.

## The new rule: pass the outcome, let the gate filter

Even without a fully proven cause, there was enough reason to change it. Right after a loss is the worst possible moment to ask for a rating. The decision was to show the rating prompt only after a won game.

The implementation took one turn. My first idea was to call `noteRun()` only on wins, but then losses would not be counted at all. `noteRun()` also increments the rating gate's play count, the hub home screen's "today's mission" progress and the push-consent decision, so dropping losses would throw all of those off. Instead I changed the contract so that **every game is still counted, the outcome is passed as an argument, and the gate does the filtering**.

Here is the change in the shared gate (`review.ts`).

```ts
// before
const noteRun = (totalRuns?: number, blocked = false): void => {
  sessionRuns++;
  // ... record total plays and days used ...
  if (sessionRuns < minSessionRuns) return;
  if (s.runs < minRuns || s.days.length < minDays) return;
  // ... past the conditions, request a rating after 1.5 s
};

// after
const noteRun = (totalRuns?: number, blocked = false, positive = true): void => {
  sessionRuns++;
  // ... record total plays and days used (losses count the same) ...
  if (!positive) return; // loss, failure or quit: keep the count, save this session's chance
  if (sessionRuns < minSessionRuns) return;
  if (s.runs < minRuns || s.days.length < minDays) return;
  // ...
};
```

When `positive` is false, the gate records the play and the date and returns. This session's single request opportunity stays unused, so if the player wins later in the same session, the request can happen then.

On the game side the call became `noteRun(mood?: 'good' | 'bad')`. Leaving the argument out keeps the old behaviour, so tool-style apps without winners or losers, such as fortunes and random draws, needed no changes. Gomoku's call site now looks like this.

```ts
// before: the same call, win or lose
pushConsent.noteRun();

// after: mood uses the same formula as the result log (gm_game_end)
const mood: RunMood | undefined = puzzle
  ? lastPuzzleWon ? 'good' : 'bad'          // daily puzzle: only when solved
  : mode === 'ai'
    ? holdMs !== 0 && winner !== null && winner === mePlayer() ? 'good' : 'bad'  // vs AI: only on a win
    : undefined;                             // two players: old behaviour
pushConsent.noteRun(mood);
```

In Gomoku, `holdMs === 0` means the player resigned. A resignation is not a win, so it counts as 'bad'.

The fifteen board games already received the result from a shared shell, but each game was throwing it away with `onResultShown: () => pushConsent.noteRun()`. I added one function to the shell and changed one line per game.

```ts
export function resultMood(r: MatchResult): RunMood | undefined {
  if (r.mode !== 'ai') return undefined; // same-device two-player: someone always wins
  return r.winner === r.me ? 'good' : 'bad'; // loss, draw or resignation is bad
}
```

This is what counts as 'good' for each kind of game.

| Kind | good | bad |
|---|---|---|
| vs AI (board games, Gomoku, billiards, pong, rock-paper-scissors and so on) | a win | loss, draw, resignation |
| Completion games (Minesweeper, cards, Sudoku and so on) | cleared | quit midway |
| Score games (Tap Bird, Snake and so on) | new personal best | any other game over |
| Daily quiz | correct | wrong |
| Two-player and party modes | old behaviour | - |
| Fortune and tool apps | argument omitted (old behaviour) | - |

Choosing "new best only" for score games was a judgement call. Score games have no win and every round ends in game over, so a new best is the closest thing to "after a win". I noted that it can be rolled back if the prompt ends up appearing almost never. The kids' apps (the Math, Hangul and English Monsters) have the rating prompt switched off anyway, so they are not affected.

The change went into a single commit on November 6. It touched 72 files, 65 of them game sources. The rating gate tests went to 17, three of them new, and the board shell got one more test. I also added a line to the launch checklist: games with an outcome must pass it. Three days later I filled the gaps. Merge Pop had been a candidate after every round and now asks only on a new best; Tap Bird's endless and daily adventure modes now ask only when the course record is beaten; and the seven certification quiz apps and the nursing assistant quiz, which live outside the monorepo, now ask only after passing a mock exam or scoring at least 60 percent in practice.

## Fixing the code does not ship it

I almost missed this one. Changing a shared package does nothing for users until each game's Toss bundle is rebuilt and passes review; until then their phones run the old code. When I checked on November 9, only Gomoku and a few rebuilt hubs actually had the change.

I rolled it out in order of how likely each group was to collect one-star reviews.

| Order | Target | Status |
|---|---|---|
| 1 | Gomoku (Toss) | bundle submitted 11/6, approved and live at 23:35 that day |
| 2 | Board-game hub (FDK Board Duel) | Toss review requested 11/7, Play update sent for review |
| 3 | 10 Toss board games vs AI | review requested 11/9 |
| 4 | 12 Toss score games | review requested 11/9 |
| 5 | 9 Toss puzzle games | review requested 11/9 |
| 6 | Individual Play apps | as of 11/9, 81 apps still had their last AAB from before 11/6; rolling out in batches |

Of the 31 submitted on November 9, I rechecked the live version today for three board games (Reversi, Janggi, Mancala), three score games (Reaction Challenge, Tap Bird, 2048) and three puzzle games (Sudoku, Solitaire, Block Fill). All nine had the November 9 bundle live. I did not recheck the other 22 or the Play side one by one for this post, so I will just call those "rolling out".

The release notes taught me something too. The first draft listed "check the rating dialog after a win" in the reviewer's test steps. But the rating dialog needs five plays over two days, so it will almost never show on a reviewer's device. To avoid it being flagged as a defect, I changed the note to "the rating dialog may not appear during review."

## The effect is not confirmed in numbers yet

This is the part I most want to state carefully.

There is a number in the ledger that looks good. After the new Gomoku bundle went live at 23:35 on November 6, nine Gomoku reviews came in through November 14, all of them 4 or 5 stars. But that cannot be called an effect.

- **The traffic mix changed.** Gomoku's program budget ran out at 10:53 on November 5, and inflow dropped to about a third the next day. The people who had been leaving one-star reviews started arriving in far smaller numbers at the same moment the rating rule changed.
- **The samples are tiny.** Both before and after are single-digit counts, so one or two one-star reviews swing the ratio wildly.
- **The comparison window is not complete.** The plan is to compare the one-star share and average rating for two weeks before and after the live date, with the call made after November 20. The review list tool was returning an "unregistered request" error during this period, so that has to be read from the console screen.

So what I can say today is only that the rating prompt is no longer requested after losses. Whether one-star reviews went down, I do not know yet.

## What is left

- After November 20, compare Gomoku two weeks before and after. Do the same per app for each batch (board, score, puzzle).
- Redeploy the individual Play apps. About 50 have an outcome, so they go out in batches with a version code bump each.
- The checklist item "pass the outcome" is a manual check for now. The plan is an automated check that warns when a file with win, loss or score variables still calls `noteRun()` with no argument.
- I still have no win/loss breakdown for program traffic. Next time the same question comes up, it is better to set up a conditional conversion metric from the start.

## What I learned

- **Line review dates up with traffic.** When one-star reviews went up I suspected the app first, but what had changed first was who was coming in.
- **"When to ask" needs the outcome, not just counts and dates.** I had specified five plays, two days and the second play of a session, and never looked at whether the player had just won or lost.
- **Keep counters separate from requests.** Had I fixed this by calling only on wins, the play count, missions and consent logic would all have broken together. Always count the event; filter only the action.
- **On the day you change shared code, make the rollout table too.** Between a commit and users seeing it there are as many builds and reviews as there are apps.
- **Measure after the confounder has passed.** When the rule change and the traffic change land on the same day, even a good-looking number tells you nothing yet.

I did the data queries, code changes and bundle builds for this together with AI agents; what to change and when to ship it were my calls.

My apps are listed under [GAMES](/games/) and [APPS](/apps/). Updates are posted on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
