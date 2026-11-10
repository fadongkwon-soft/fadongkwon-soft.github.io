---
title: Why I Threw Out 300 Korean Pun Riddles — From Writing Originals to Collecting the Ones People Actually Tell
description: "I wrote 300 original Korean nonsense riddles while deliberately avoiding the famous ones, then rebuilt the bank from 410 riddles people actually trade, with my own hints and explanations, cross-review, and a clear sourcing policy"
image:
  path: /assets/img/20261110_nonsense-quiz-rebuild/cover.png
  alt: Why I threw out 300 Korean pun riddles
date: 2026-11-10 23:12:00 +0900
categories: [Devlog, Automation]
permalink: /posts/nonsense-quiz-rebuild/
alt_url: /ko/posts/nonsense-quiz-rebuild/
tags: [quiz, puns, riddles, question bank, solo developer, dev log]
---

[Nonsense Quiz](/posts/nonsense-quiz/) is a Korean pun riddle app. A host can read riddles aloud for a group to shout out answers, or you can play solo with four choices. The bank inside it now holds 320 riddles, but it did not start that way. The first version, built on October 26, was 300 riddles I wrote from scratch. On November 7 I threw out the principle behind it and rebuilt the bank.

The title says I threw out all 300. Strictly speaking, I dropped 189 and reworked 111 that were worth keeping. What I threw out completely was not the riddles but the rule I had used to write them. This post is about why that rule was wrong, what replaced it, and how I handled sourcing and copyright along the way. The general pipeline for building question banks with AI agents is in my [certification exam bank devlog](/posts/cbt-bank-generation/). This one is about where that approach broke down for a different genre.

## The first rule: leave out the famous ones on purpose

The rule for the first version went like this. Do not copy from online or printed riddle collections. Take only **the mechanics of wordplay** (homonyms, number sounds, letter shapes, reading backwards, re-spacing words, onomatopoeia, splitting words, English sounds, reading proverbs literally) and write new sentences. Leave out the classics everyone knows, such as 열바다, 킹콩, 후다닭 and 자원봉사자, because they might be someone else's sentences.

The reason was caution about copyright. I applied the same judgment I had used for the certification banks, where I wrote every question myself instead of using past exam papers. As a result, only two of the 300 riddles were well-known classics: 문 turned upside down looks like 곰 ("bear"), and 토마토 ("tomato") reads the same backwards. Even those two were flagged as "a classic" in their explanations.

The cross-review at the time pushed in the same direction. One of its checks was "does this reuse a famous sentence," and four riddles, 고등어 (mackerel, "the fish that goes to high school"), 참외 (Korean melon, "the lonely fruit"), 참치 (tuna) and 화가 (painter), were rewritten precisely because they were "almost the same as the version going around." Looking back, the review was carefully erasing the very thing that makes nonsense riddles fun.

## The verdict: riddles nobody actually tells

Right after launch I made a gameplay Short and watched it back, and the problem was obvious. None of the riddles produced that "ahh" moment. The verdict, in short, was that **these were not the riddles people actually trade**. The conclusion came just as fast: go search the web if necessary, and put in the nonsense riddles Koreans really use.

Re-judging the first version one riddle at a time showed why. Counting the reasons behind the 189 dropped riddles, the biggest groups were proverb fill-in-the-blank (36), forced compounds made by chopping letters apart (31), the same "it is X and also Y" homonym template over and over (27), and grouping the meanings of a verb (22). These were Korean language exercises more than riddles. Here are a few of the dropped ones as they were.

- "글씨도 하고, 약 맛도 하고, 모자도 하는 것은?" ("Handwriting does it, medicine's taste does it, a hat does it too. What is it?") — answer 쓰다. In Korean you 쓰다 (write) a letter, medicine is 쓰다 (bitter), and you 쓰다 (put on) a hat. It is correct, but it is a polysemy question from a language class. There were 22 verb riddles like this.
- "소를 잃고 나서야 고친다는 곳은?" ("What do you fix only after losing the cow?") — answer 외양간 (the cowshed), from the proverb about mending the barn after the cow is gone. It tests whether you know the proverb. It is a blank to fill, not a pun. There were 36 proverb riddles like this.
- "머리에 쓰기도 하고, 엄마와 아들을 함께 부르기도 하는 것은?" ("You wear it on your head, and it also means mother and son. What is it?") — answer 모자. 모자 means a hat, and 母子 (mother and son) is pronounced the same. Almost nobody says 母子 in daily life, so even getting it right is not funny.

The mechanics are all sound. The homonyms are real and so are the proverbs. But the fun of a nonsense riddle does not come from the mechanics. It comes from someone bringing up a riddle everyone knows and the room going "oh, that one!" By leaving out the famous riddles on purpose, I had left out the center of the fun.

## The switch: collect the riddles people actually tell

The new rule is the reverse. **Questions and answers stay exactly as people trade them. Hints, explanations and wrong choices are written by me.**

First I collected candidates. I read riddles from the Namuwiki list of nonsense quizzes, collection posts in three Daum cafes, a recreation-oriented riddle blog, and nonsense quiz card PDFs from a parenting education site, then merged them. If two questions were worded a bit differently but shared the same answer and mechanism, they became one candidate, and I recorded how many source pages carried it. The result was 410 candidates from 15 distinct sources. Of the 410, 155 appeared in two or more sources.

I wrote down the limits of those numbers alongside them. The search tool kept returning the same sites, and some collection sites showed clear signs of copying from the cafes and Namuwiki, so the source count can overstate how well known a riddle is. The sources that look independent are the three cafes, Namuwiki, the collection blog and the parenting site. The 99 candidates that came only from the parenting site's cards might be that company's own creations, so I marked them separately (more on this in the copyright section below).

A few examples of what the collection looks like. All of these are classics that showed up in several sources.

- "도둑이 가장 싫어하는 아이스크림은?" ("What ice cream do thieves hate most?") — 누가바. Nugabar is a Korean ice cream bar, and the name sounds like "누가 봐!" ("someone's watching!"), the words a thief fears most. It appeared in five sources in the candidate file.
- "차도가 없는 나라는?" ("Which country has no roads for cars?") — 인도 (India). Take away the 차도 (roadway) and only the 인도 (sidewalk) is left, which is also the Korean name for India.
- "왕이 넘어지면?" ("What happens when a king falls over?") — 킹콩 (King Kong). The king goes "kong," the Korean sound of a thud.
- "세상에서 가장 뜨거운 바다는?" ("What is the hottest sea in the world?") — 열바다. "열받아" ("I'm so mad," literally "getting heated") sounds like 열 바다, "heat sea."

These are exactly the riddles the first version had avoided.

Some things were cut at collection time. Riddles that need a picture or a sound, riddles whose answer is a real person such as a celebrity or politician, profanity, sexual content, body shaming, and jokes about disability or nationality were all excluded. When moving riddles into the app I cut further: religion, the military, executions and war, bathroom humor, gender and appearance, and riddles whose answer is a character name.

## Riddles whose answer differs by source were left out

When you collect nonsense riddles, you run into famous ones you still cannot use: riddles whose answer changes from source to source. "What happens when a banana laughs?" is 바나나킥 (a snack brand) in one place and 빙그레 (a word for a smile, also a company name) in another. "감은 감인데 먹지 못하는 감은?" ("Which 감 can't you eat?" — 감 means persimmon) accepts 영감, 옷감, 대감 and 장난감, all words ending in 감. "Which 개 can't you catch?" (개 means dog) works for 안개 (fog), 번개 (lightning) and 무지개 (rainbow).

Out loud in a group, you just say "that works too" and move on. But the moment an app picks one answer and grades against it, someone who answered correctly gets told they are wrong. So these stayed out no matter how famous they were. "What happens when a strawberry runs away?" (strawberry jam or strawberry syrup) and "What are four trees?" were dropped for the same reason.

## Cross-review: solve first, refute the wrong choices, distrust the hints

After the rebuild, all 320 riddles went to a separate reviewer agent. The review has three steps.

1. **Solve from the question alone.** Before seeing the answer, the reviewer comes up with its own and checks whether it matches. A mismatch means the riddle does not narrow down to one answer.
2. **Refute the wrong choices.** Argue adversarially that each of the three wrong choices really is wrong. Nonsense riddles are about twisted thinking, so a wrong choice often makes sense if you twist it too.
3. **Check whether the hint gives the answer away.** A hint should point a direction, not effectively state the answer.

Here is what came back.

| Review result | Count |
| --- | ---: |
| No change | 216 |
| Revised (parts of the same riddle fixed) | 99 |
| Replaced (a different candidate in the same slot) | 5 |
| Revision detail — hint gave the answer away | 43 |
| Revision detail — wrong choice replaced | 42 |
| Revision detail — explanation fixed | 7 |
| Revision detail — question narrowed because answers split | 5 |

_A riddle can have several revision details, so they do not add up to 99._

The most common defect was **a hint that simply states the answer**. A riddle whose answer was 파 (fa, the musical note) had the hint "도레미○솔" (do re mi _ sol). Others had the same shape, "○○ 먹이다" or "나의 ○○은," where filling the blank gives you the answer. The instruction "help the player think of the answer" had slid into "give a sentence that contains the answer." All 43 were rewritten to point a direction only.

The second was **a wrong choice that is actually right**. A riddle asking for the coldest sea had the Arctic and Southern Oceans among its wrong choices, which are not puns but the real answer. A riddle about "the biggest nose" had to be narrowed to "among country names," because an elephant really does have the biggest nose. In this type, plain fact sneaks into a wrong-choice slot and threatens the intended answer.

The typed-answer mode got checked too. To accept slightly different spellings of correct answers, 40 accepted variants were added across 20 riddles. The correct answer is the longest choice in 11.9% of riddles, and the average length ratio of correct to wrong choices is 1.033, so length gives almost no clue to the answer.

## The result: 320 riddles, 111 kept and 209 newly collected

Each of the first version's 300 riddles was judged keep, fix or drop. 84 were kept as they were. 27 kept their mechanism but were reworded into real riddle phrasing, or swapped for the more famous version of the same pun. This is where 고등어 ("the fish with the best education") and 참외 ("the loneliest fruit"), which the earlier review had erased, came back in their famous forms. The 189 dropped slots plus 20 new numbers were filled with 209 new riddles.

| | First version (Oct 26) | New version (Nov 7) |
| --- | --- | --- |
| Riddles | 300 | 320 |
| How they were made | All original (mechanics only) | 111 kept from the first version + 209 newly collected |
| Well-known classics | 2 | 82 in the classics section alone |
| Questions and answers | My own sentences | As commonly told (tone adjusted only) |
| Hints, explanations, wrong choices | Written by me | Written by me |
| Source of new riddles | Not applicable | 175 web candidates · 16 education cards · 18 classics outside the candidate file |

By difficulty there are 108 easy, 164 medium and 48 hard. By category there are 82 classics, 118 sound puns, 49 letter play, 27 lateral thinking, 42 numbers and English, and 2 others. Automated tests guard the count and numbering, duplicate questions and answers, four distinct choices, wrong choices never being accepted as correct in typed mode, and answers of two or more characters never appearing whole in the hint.

## Sourcing and copyright policy

Once you decide to collect riddles, you are back at the question the first version was trying to avoid: is it fine to use what other people made? I cannot substitute for legal advice, so here I describe what we actually did and what we hold as our operating policy, separating what was done from what we commit to going forward.

**What we actually did this time**

- **Questions and answers were collected as widely shared folk material.** Nobody knows who first came up with riddles like 누가바 or 열바다, and the same question and answer pass through countless cafes and collection posts. For these, the question and answer are used as is, with only the wording adjusted to the app's polite riddle style.
- **Every hint, explanation and wrong choice was written by us.** This rule is written at the top of the question bank file, and even the one-line notes attached while collecting candidates were set to be written fresh instead of copied from the sources.
- **No single site's list was copied wholesale.** Candidates were merged from fifteen sources into single entries, and the order inside the app follows our own categories (classics, sound puns, letter play and so on) and the slot numbers from the first version. The structure does not reproduce any one site's selection or order.
- **Riddles that may have an author were marked and pushed back.** The 99 candidates found only in the parenting site's card PDFs could be that company's own work, so they were not treated as "widely known." Candidates from posts where people trade riddles were used first, only 16 card riddles were added as filler, and the audit sheet lists exactly which 16 they are.
- **Source records were kept in the question bank folder.** The candidate file stores, for every riddle, the list of source URLs, how many sources carried it, and whether it came from posts people write or only from the cards. A separate notes file lists the 15 sources with how many riddles were read and used from each, along with the collection criteria and limits. The audit sheet records, for each new riddle, whether it came from the web candidates, the cards, or classics outside the candidate file.
- **Most puns tied to real people or trademarks were cut.** Riddles whose answer is a celebrity's name (such as one pairing an eraser with an actor's name), a four-character idiom reworked around a politician's name, and puns built on apartment, car, restaurant or medicine brands were excluded at collection time. The exception is a case like 누가바, where an ice cream name is itself the answer to a long-standing classic.

**Limits and going forward**

- **We did not adopt only riddles confirmed by multiple sources.** Of the 410 candidates, 155 appeared in two or more sources. The source count was recorded but not used as an acceptance rule. When adding riddles from now on, I intend to look harder at single-source riddles and card-sourced ones.
- **Riddles and sources are not linked character for character.** During review, 225 riddles could not be matched to the candidate file by machine because their wording had been polished. And the 18 classics not in the candidate file were added from memory, judged to be widely known, so they have no source URL. Re-attaching per-riddle sources for both is still to do.
- **Gags and catchphrases with a clear creator stay out.** This time I did not set up a separate check for it, but going forward the policy is that wordplay with an obvious author, such as a TV comedy segment or a particular comedian's catchphrase, is not treated as folk material.
- **How to show sources inside the app is not decided yet.** For now the records live only in the repository.

## What is still open

- The rebuilt 320 riddles have not yet had a human review. The 48 hard riddles that mix in English and Chinese characters, and the 18 added from memory, need another look in particular.
- A few puns that are close to forced remain. Whether they land on first hearing is something to sort out from real play.
- For riddles with open-ended answers, more accepted variants were added, but in typed mode a player may still answer correctly and feel marked wrong.
- I have not yet checked on screen that the longest answers and long choices fit.

## Knowledge quizzes and nonsense riddles are different genres

The lesson comes down to one thing. **Some genres suit original writing and some do not.**

Knowledge quizzes, Korean history, economics, certification exams, suit original writing. Their value is in "do you know this," and asking the same fact in a new sentence keeps that value intact. Copying past papers is what would raise copyright problems. So for knowledge quizzes, taking only the mechanism (the exam standards and concepts) and writing fresh questions worked well.

Nonsense riddles, folk riddles and dad jokes are the opposite. Half the fun comes from "everyone knows it." When the host asks "What ice cream do thieves hate most?", people who already know shout the answer with a grin, and people hearing it for the first time go "ahh" when they hear it. Both are fun. A newly invented riddle is unknown to everyone, so both reactions disappear and you are left with a language exercise built on mechanics.

So the rule for nonsense-style question banks became this. Collect riddles that actually circulate on the web, leave out answers that differ by source, and limit what we write to explanations, hints and wrong choices. Even when the task is the same "build a question bank," I should have started by asking what that genre treats as fun.

## Summary

- The first version was 300 original riddles written under the rule "leave out famous riddles, borrow only the mechanics," and it was judged to be riddles nobody actually tells. Most dropped riddles were proverb blanks, forced compounds, repeated templates and verb-meaning groupings.
- The new version collected 410 candidates from the web, kept questions and answers as commonly told, and wrote only the hints, explanations and wrong choices. Riddles whose answer differs by source were left out.
- The defect cross-review caught most often was a hint that gives away the answer (43), followed by replaced wrong choices (42).
- The result is 320 riddles, 111 kept from the first version and 209 newly collected. Source records exist, but per-riddle source links and a human review are still to do.

The app introduction and where to get it are in the [Nonsense Quiz post](/posts/nonsense-quiz/). The full pipeline for building question banks with AI agents is in the [certification exam bank devlog](/posts/cbt-bank-generation/). News comes through this blog and [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).
