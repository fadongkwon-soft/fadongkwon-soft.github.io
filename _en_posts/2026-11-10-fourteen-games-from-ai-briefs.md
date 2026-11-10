---
title: How I Built 14 Games at Once from AI-Written Briefs — Mixing Two Genres and Splitting the Work Across Agents with Two Briefs
description: In one evening I took fourteen two-genre mashups to a prototype and a release shell. Here is the rule against using original names and art, why the prototype brief and the shell brief are separate, where the orchestrator and the parallel agents drew their boundaries, why the 10-minute device gate became an automated gate, how the English names were redone after searching, and what did not go well
image:
  path: /assets/img/20261110_fourteen-games-from-ai-briefs/cover.png
  alt: Building fourteen games at once from AI-written briefs
date: 2026-11-10 23:14:00 +0900
categories: [Devlog, Automation]
permalink: /posts/fourteen-games-from-ai-briefs/
alt_url: /ko/posts/fourteen-games-from-ai-briefs/
tags: [minigame, hub app, apps in toss, automation, solo developer, dev log]
---

On the evening of November 7 I made fourteen new games in one go. More precisely, I finished one game end to end first, then used it as the model and handed the other thirteen to several AI agents at the same time. This post is about what the briefs looked like, who did what, how pass and fail were decided, and where the games ended up. The briefs themselves were written by AI too. My part was picking the direction, confirming the default proposals and reviewing what came back.

First, the count. The decision document in the work log is titled "14 mashup games", and the gate table has exactly fourteen rows. That is Mahjong Quest, built first, plus the thirteen built in parallel.

## The starting point: mix genres instead of taking games apart

It started somewhere unexpected. The question was whether a reverse-engineering tool could be useful for the business, and alongside it I looked at the popular list on the web game portal CrazyGames. The conclusion was not to use the tool. The moment you pull code or art out of someone else's game, it becomes infringement. Instead, popular genres would be used only as **ingredients**. Rules (mechanics) are not covered by copyright, so mixing two different genres gives you an original that does not exist anywhere.

That produced fourteen mashups. Mahjong Quest came first. My existing strategy notes put users in their 30s to 50s ahead of teenagers, mahjong skews strongly toward people in their 50s, a roguelike structure brings people back, and existing card game code could be reused.

| Order | Korean name | Genres mixed | English name | Toss hub |
| --- | --- | --- | --- | --- |
| 1 | 마작 원정 | mahjong solitaire × deck-building roguelike | Mahjong Quest | Puzzle Cafe |
| 2 | 번호 낚시 | fishing × number draw | Number Ball Angler | On hold (Play only) |
| 3 | 띠 운세 공방 | idle tycoon × Chinese zodiac fortune | Zodiac Fortune Workshop | Arcade |
| 4 | 합체 수비대 | merge × tower defense | Merge Gate Guards | Arcade |
| 5 | 숫자 뱀 | snake × 2048 | Doubling Snake | Arcade |
| 6 | 나사 퍼즐 블록 | screw unscrewing × block filling | Bolt Drop Fill | Puzzle Cafe |
| 7 | 역사 지도 찍기 | location guessing × Korean history and geography | History Map Pin | Daily Quiz |
| 8 | 오목 카드 대국 | gomoku × roguelike ability cards | Gomoku Card Duel | Board Duel |
| 9 | 당구 공성전 | billiards × castle toppling | Cue Ball Siege | Siege |
| 10 | 분식집 머지 | serving × merge | Bunsik Snack Merge | Puzzle Cafe |
| 11 | 한글 연금술 | element combining × Hangul letters | Hangul Alchemy | Daily Quiz |
| 12 | 윷 땅따먹기 | territory grab × yut nori | Yut Land Grab | Board Duel |
| 13 | 박자 두더지 | rhythm × whack-a-mole | Drum Beat Moles | Arcade |
| 14 | 버드 서바이버 | survivor-like × tap bird | Wingbeat Survivors | Arcade |

Some things were dropped along the way. The reverse-engineering tool was never used, and the names of the reference games appear nowhere in game code or on screen. In a later review, a search of the whole source for about ten original titles returned zero hits, and none of the fourteen folders contains a single image or audio file. Everything is drawn with CSS and canvas. Even the mahjong tiles are drawn as text, not pictures.

## The brief was split into two documents

### How the prototype brief is organized

The first brief the agents received is a one-page document called "the common mashup brief". It was not written per game; all thirteen agents got the same document. The only game-specific input is one row of the mashup table and the folder name. Everything else is shared rules. It has six sections.

1. **Reference implementation** — it points at the Mahjong Quest folder, built first, and says to "follow the structure as is". Rules and scoring go in one file with no UI code, and tests go in a file that loads it and simulates balance. It even spells out which import path keeps the tests from breaking.
2. **Scope of this stage** — "a playable prototype (Korean only)". Home, play, result, records and a daily run only. Ads, hearts, translation, push, sharing, rankings and cross-promotion are pinned down as "do not attach". Spots where a rewarded ad might fit only get a note in the status file.
3. **Must follow** — "an original that mixes only the rules (mechanics)", no translationese, no gambling language, keep bottom-fixed UI above the Toss banner, never redraw the first screen after boot. Most of these lines came from earlier apps that were actually rejected or had screens covered.
4. **Forbidden** — the section title is "12 other agents are working in the same repository at the same time". Do not create or edit anything outside your own game folder, no package installs or git commands, no browser tools.
5. **Verify before finishing** — rule tests, zero type-check errors, a successful build, a written status file. All four must pass to be done.
6. **Report** — "250 characters or fewer, in Korean". Done or not, test count, build size, what to check on screen, what got stuck.

The last section is short for a reason. If thirteen agents each send a long report, the receiving end cannot read them all. The report is kept short and the details go into the status file in each game folder.

### Why the shell brief is separate

The second document is the "shell brief". The shell is the release wrapper around the game. Ads, hearts, leaderboards, push consent, sharing, cross-promotion, nine-language translation and back navigation all live there.

There are two reasons it was not folded into the first brief. First, whether a game is fun and whether it follows release rules are different problems, and one agent doing both at once blurs both. That is also why ads were banned at the prototype stage. Second, shell rules are Toss review criteria, so every sentence has to be exact. The rewarded-ad section of the shell brief is titled "these are Toss rejection criteria, so be precise". Lines like these:

- Rewarded ads are "exchange type only". Watch the ad to the end and the action (a hint, an extra try) happens immediately. One or two spots per game, with a per-run cap.
- The ad button gets a TV mark before its label and a one-line notice "directly under that button". Direction words like below or above are banned, and announcing it only in a toast is banned too.
- On the web, where there are no ads, the ad button and the notice are hidden. The brief gives the reason in parentheses: "on the web the notice is a lie".
- Never show an interstitial directly. The hearts module attaches it on its own, so they would overlap.

Translation covers all nine languages, except Hangul Alchemy and History Map Pin, whose content is Korean itself, so they stay Korean only. The pre-finish checks include a one-line command that counts Unicode escapes and banned words in the translation file, and the result has to be `0 0`.

## Splitting the work into three roles

The actual work split into three roles.

- **Orchestrator (the main session)** — wrote the mashup table and both briefs, built Mahjong Quest end to end as the reference implementation, launched the agents, opened what came back in a browser, ran the check scripts and committed.
- **Thirteen prototype agents** — each took the first brief and one game, and built rules, tests and screens inside its own folder.
- **Thirteen shell agents** — each took the shell brief and added a shell to one of the same thirteen games. They connect to the previous stage by reading the "rewarded-ad candidates" the prototype agent left in the status file and picking one or two.

Models were chosen per role as well. Design and judgment went to a higher-tier model and implementation to another, and work with tightly written rules, like the shell, ran on a single lighter model. Counting web research and translation, 29 sub-agents were launched that day.

| Stage | Owner | Input | Output | Done when |
| --- | --- | --- | --- | --- |
| Mashups | Orchestrator | popular genre list, strategy notes | 14 mashups and an order | user says "start from number one" |
| Reference build | Orchestrator | the top mashup | Mahjong Quest prototype and shell, 7 tests | automated clicks from run one to the result at 375×812 |
| Prototype | 13 agents | common brief | 13 game folders, status files | tests, type check, build, status file |
| Shell | 13 agents | shell brief, status file | nine languages, ads, hearts, rankings, sharing | the four above plus banner audit plus escape and banned-word count `0 0` |
| Decisions | User | default proposals D1 to D17 | hub placement, names, ad swaps | defaults confirmed |
| Gate | Orchestrator | the 14 games | gate table | all five checks pass |
| Hub inclusion | Orchestrator | six hub configs | Toss and Play hub bundles | zero hub audit errors, review requested |

The brief's forbidden section drew the boundary. Agents cannot touch anything outside their game folder, and only the orchestrator edits shared packages, the app list, hub configs and tools. Checking the screen is also the orchestrator's job, so agents had browser tools blocked. This boundary is the rule from the time [three AI sessions did the same job twice and overwrote each other's records](/posts/parallel-ai-sessions-collision/), moved down to the level of a single game.

It still leaked once. The Cue Ball Siege shell agent ran another agent's patch script that was sitting in a shared scratch folder, and the Bolt Drop Fill file got patched a second time. The repository boundary held, but the scratch folder was never fenced off. I confirmed there was no duplicated code, but never fully diffed whether the patch had overwritten something else.

## The 10-minute device gate, and why it was skipped

The gate I first planned was a human one. The handoff document's order was "a 10-minute play gate on a real device (dev phone over wireless adb), only passing games move on, failing ones get a fix list", and decision D13 also said "starting from the games that pass the 10-minute device gate". The rule is to ship all fourteen, but the order would be by quality.

In practice the gate was skipped. On November 8 I decided "skip the device test results and move to the next step. If needed I'll ask for fixes even after release", and instead of ten minutes of human play, five automated checks were run.

- zero type-check errors
- every per-game rule test passing (219 in total across the fourteen)
- a successful build
- hearts audit passed (the hearts gate and the remaining-hearts badge are wired correctly)
- banner audit passed (no bottom-fixed UI is hidden behind the Toss banner)

All fourteen passed, one of them only after a fix. Zodiac Fortune Workshop had no remaining-hearts badge and failed the hearts audit, so a badge was added next to the reset button. Why these audit tools exist is in [the post on 21 launch incidents](/posts/launch-incidents/).

Content got its own check. History Map Pin gives full marks within 3 km, and the six coordinates that had gone in as rough values (Ugeumchi, Dabudong, Gobu, Gwansanseong, Gibeolpo, Cheonghaejin) were checked against the real locations and all fell within about 1 km. Hangul Alchemy's 381 words came from the list in an existing initial-consonant quiz app, so the whole list was read through, and the one doubtful word, 달걀판 (egg tray), was confirmed as a headword in the Standard Korean Language Dictionary.

To be honest, this gate catches "does it run" but not "is it fun" or "does it fit the hand". None of the 219 tests says that a gomoku cell is about 22 px and hard to tap with a finger. Device checks remain open after release, through Toss test bundles and debug APKs.

## Naming: Korean from the agents, English from searching

The Korean names are the ones each prototype agent came up with, unchanged. English names were different. Searching the agents' provisional English names on Play, the App Store and web game portals turned up many overlaps.

- Bolt Drop Fill's provisional name "Screw Block Puzzle" had several games with similar names, so it was changed.
- Merge Gate Guards was "Merge Defense", which already existed on both a web portal and Play.
- For Wingbeat Survivors, another candidate name was also taken, so it was dropped too.
- Cue Ball Siege had no overlap under its provisional name but was renamed anyway, and one intermediate candidate was dropped because it sounded like a well-known game.
- Number Ball Angler keeps the word lotto out of its English name.
- Zodiac Fortune Workshop, Gomoku Card Duel, Yut Land Grab and Hangul Alchemy had no same-name games and stayed as they were.

Searching for Mahjong Quest showed several games with the same name already. An alternative was proposed, but the name had already been confirmed, so it stayed. The document also records the scope of the check as is. Only web search results were reviewed, and no trademark search was done.

## Into the hubs

On Toss there is no room to register new apps one by one, so the rule is that new games go inside an existing hub app. How the hubs were built is in [the post on bundling fifty games into nine hubs](/posts/hub-shell-devlog/). Placement follows the table above. Puzzle Cafe got three, Arcade five, and Board Duel and Daily Quiz two each. Zodiac Fortune Workshop has fortune in its name, but it is an idle game, so it went to Arcade rather than the non-game fortune hub.

There are two exceptions. Number Ball Angler is a number-draw game, so given past gambling-related rejections it is on hold for the Toss hub and went only into the Play version of a hub. All nine languages keep the notice "this has nothing to do with winning". Cue Ball Siege first went into the Olympics hub, then moved when a Siege hub for landscape-only games was created.

Inside the hubs, each game was also wired into hub features. The Arcade weekly league normalizes scores against a per-game par: 1,500 points for Doubling Snake, 120 seconds for Wingbeat Survivors, 20 waves for Merge Gate Guards. Drum Beat Moles' par of 15,000 is marked "estimated" in the document itself. For the Board Duel combined rank, Gomoku Card Duel and Yut Land Grab send a result signal at the end of each game.

## What did not go well

Only the larger items from the review document.

- **Nobody played a game through by hand.** Thirteen games were built in parallel in a little over an hour, and after the shells went on, History Map Pin was the only one where the ad button was actually pressed. Touch sizes such as about 40 px for a mahjong tile and about 22 px for a gomoku cell were never checked on a device.
- **Balance notes remain.** Bolt Drop Fill's generated levels may be too easy because they solve without search, and Drum Beat Moles' top grade is tight.
- **Some places drifted from the plan.** The checklist note for Yut Land Grab said "compete against other people's recorded runs", but it was built as a match against two or three AI players. The note for Hangul Alchemy said "real dictionaries only", but the words came from an existing app's list. Gomoku Card Duel swapped one boss ability for another because of win rates, and Bunsik Snack Merge used a different leaderboard value from the brief. These changes were in the agents' reports but dropped out of the main summary. In my view, that was the cost of capping reports at 250 characters.
- **Report numbers disagreed.** The test count for the thirteen was 186 in the commit message and 198 in the main report. Adding up the individual reports, 198 was right.
- **An unneeded task was left over.** The shell agents wrote that per-game ranking sort order had to be set in the Toss console, but inside a hub, per-game Toss leaderboard submission is turned off. It was taken off the to-do list.
- **Three of the first ad spots were changed.** The rewarded ads in Merge Gate Guards, Doubling Snake and Wingbeat Survivors were revive-type, and based on measured records from earlier apps they were replaced with a wave retry, a food swap and a starting-boost pick.

However carefully you write a brief, gaps appear. This time the gaps were "the scratch folder" and "what must go in the report". The next brief gets a line banning shared scratch folders and one saying that any design change goes on the first line of the report.

## Where things stand

- Toss: the thirteen games other than Number Ball Angler are inside five hubs (Puzzle Cafe, Arcade, Board Duel, Daily Quiz, Siege).
- Google Play: none of the fourteen has shipped as a standalone app yet. They go out one at a time, by quality starting with Mahjong Quest, within the weekly new-app limit.
- Real-device play checks continue after release, through test bundles and debug builds.

The apps I've made are on [GAMES](/games/) and [APPS](/apps/). News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> This post is based on the work documents from November 7 to 10, 2026 (the common brief, the shell brief, the decision log and the review notes). Hub placement and names may change later.
{: .prompt-info }
