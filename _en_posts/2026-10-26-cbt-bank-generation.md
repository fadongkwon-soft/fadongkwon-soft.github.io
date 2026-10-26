---
title: How I Built a 7,200-Question Exam Bank with AI Agents — Separate Writers and Reviewers, and the Source Documents I Should Have Read First
description: I wrote 7,200 original practice questions for five Korean certification exams, care worker, cosmetologist, cook, baker and forklift or excavator operator. This covers the copyright call to avoid past papers, running twenty writer agents and twenty cross-review agents in parallel, the defect types the review actually caught, the gap of designing without the official exam standards at first and then fetching the standards, statutes and textbooks to reconcile, and what is still on hold
image:
  path: /assets/img/20261026_cbt-bank-generation/cover.png
  alt: Building a 7,200-question certification exam bank with AI agents
date: 2026-10-26 01:41:00 +0900
categories: [Devlog, Automation]
permalink: /posts/cbt-bank-generation/
alt_url: /ko/posts/cbt-bank-generation/
tags: [certification, question bank, solo developer, dev log]
---

[Nursing Exam Bank](/posts/nursing-quiz/) is an app built on 2,400 original questions. I decided to extend the same shell to other certification exams, and between October 22 and 24 built question banks for five exam families. The result is 7,200 questions. This post is a record of how they were written, how they were reviewed, what turned out wrong, and what is still open. The apps themselves are not released yet, so their introductions come later.

## Why no past papers

Copyright came first. Q-Net does not publish questions from its on-demand exams and forbids copying them onto your exam slip. The National Health Personnel Licensing Examination Board states that care worker questions and answers are non-public copyrighted works. Reconstructed past questions floating around online have unclear provenance, so I ruled them out. The one exception is the driver's license written test, whose question bank the Korea Road Traffic Authority publishes as open data, so that one is used as is.

So the scope comes from the Q-Net exam standards and the public standard textbooks, and every question is newly written. The care worker textbook is under a no-derivatives public license, so I reference its content without copying sentences.

## Structure: family, block, question

Each exam family starts with a design file: subjects, topics, the concepts under each topic, and "what to be careful about in this topic." Generation then runs per block. A block is 30 questions with a fixed difficulty mix of 9 easy, 15 medium and 6 hard. Care worker uses five choices, the rest four.

| Family | Blocks | First pass (Oct 22) | Expansion (Oct 24) |
| --- | ---: | ---: | ---: |
| Care worker | 7 written + 9 practical, then expanded | 480 | 1,500 |
| Cosmetologist, 4 tracks (general, skin, nail, makeup) | 6 common + 3 per track, then expanded | 540 | 1,800 |
| Cook, 4 tracks (Korean, Western, Chinese, Japanese) | 8 common + 2 per track, then expanded | 480 | 1,500 |
| Confectioner and baker | 8 common + 3 + 3, then expanded | 420 | 1,200 |
| Forklift and excavator operator | 8 common + 3 per track, then expanded | 420 | 1,200 |
| Total | | 2,340 | **7,200** |

The question schema has seven fields, subject, topic, stem, choices, answer, difficulty and explanation. A validation script checks the schema, duplicates, missing difficulty and **clue bias**, the share of questions where the correct answer is the longest choice. Models that write questions tend to pad the correct choice with explanation, so a family does not pass if that share exceeds 34 percent. The final figures sit between 13 and 21 percent per family.

## Why writing and reviewing went to different models

A fast model writes, a larger model reviews, and the two run **separately on the same block**. If a model reviews its own questions, its own misconceptions pass straight through. The coordinator builds a generation prompt and a review prompt per block and hands them to agents, and the review report comes back as one of three verdicts per question: patch, delete or hold. The tool that applies the reports re-applies against backup files, so running it any number of times yields the same result.

The scale was up to twenty agents at once. Generating a block took four to six minutes, reviewing one took 30 to 90 seconds, and the reviewer used more tokens per block. The first thing to run out was not the agents but the coordinator's weekly quota. I bundled blocks two at a time to cut the number of turns, and hit the five-hour limit twice, resuming in between. State was written to files from the start so that resuming meant simply re-reading a progress file.

## What the review actually caught

Across the 78 first-pass blocks, the review touched roughly 25 questions. By type:

- **Answer number disagreeing with the explanation.** Five cases landed in one block. The explanation describes choice 3 while the answer says 2. I re-checked the other blocks from the same batch on suspicion.
- **Factual errors in explanations.** The properties of insoluble fiber, the heat resistance of norovirus, spore formation in yeast, the classification of salmon. The stem and answer were right but the explanation was wrong, which is more dangerous for someone studying from the explanations.
- **Multiple correct answers.** General-statement stems like "which pairing is correct" where another choice also held, developmental tasks overlapping across two choices, differing readings of the scope of skin care.
- **Outdated legal terms.** The honorary food inspector title was renamed to consumer food hygiene inspector long ago, and the exemption scope for medical aid co-payments had changed.

The second-pass review, done against the statutes directly, caught more: a license return obligation deleted from the Public Health Control Act enforcement rules, pre-amendment purpose wording of the Food Sanitation Act, the switch from sell-by to use-by dating, the separate notice of long-term care insurance premiums, questions where two choices were both right under the Road Traffic Act's five-meter hydrant and headlight clauses, and a relocation registration requirement abolished in November 2024. All of these are "knowledge that used to be correct." The model was not wrong so much as stale, and you cannot catch that without the source text.

## The limit of the first design, and the late reconciliation

There was a limitation in the first design that has to be stated plainly. The design agents could not open the Q-Net exam standard PDFs or the table of contents of the 2026 revised care worker textbook. So the blocks were laid out from study-guide tables of contents and general knowledge. The validity periods I had confirmed covered only cosmetologist (2022 to 2026), baking (2026 to 2027), forklift and excavator (2025 to 2027) and cook (2023 to 2025).

In the second pass I obtained the sources.

- **Q-Net exam standards.** I read the report number from each exam page and paged through the report viewer in a browser to collect the text. Command-line tools could not do it because the parameters are encrypted. It turned out that the four cook tracks have had **new exam standards in force since January 2026**, so the first design was based on the old edition, and the 2027 revision for cosmetologist was already published.
- **Statutes.** The Ministry of Government Legislation's open API returns current statute XML without a key. I pulled 30 statutes and stored them with their promulgation and effective dates.
- **Care worker textbook.** I downloaded the 2026 revised edition and the 2024 edition PDFs from the Ministry of Health and Welfare's postings and summarized the table of contents and the changes. No existing question turned out wrong because of the revision.
- **NCS learning modules**, 32 of them, mainly for forklift, excavator and nail. There are no modules yet for hair, skin and makeup, so review in those tracks still relies on model judgment.

With the sources in hand I wrote a gap report per family comparing the exam standard against the bank, and expanded to 7,200 questions in the direction of closing those gaps. The generation prompt now includes the block's standard wording and existing stems on the same topic to reduce duplication.

## What is left

- Among the review holds, items whose basis I could not confirm remain: 15 for forklift and excavator, 2 for cosmetologist, 2 for baking, 2 for cook. They get resolved against textbooks before release.
- Hair, skin and makeup lack NCS modules, so their review basis is weaker.
- The driver's license test uses the public bank as is, minus the video-type questions that need footage, on the edition in force since March 2026.
- The apps are prepared with ads enabled and store materials for both Play and Apps in Toss, and release is next week when the Play new-app quota resets. On Apps in Toss they live inside the [FDK Exam Bank](/posts/toss-hub-conversion/) hub alongside the nursing exam.

## Summary

- 7,200 original questions across five families, with no past papers. Only the driver's license test uses a public bank.
- Writing and reviewing went to different models and different agents so every block was seen twice. The main defect axes the review caught were answer-explanation mismatches and stale legal knowledge.
- The first design ran without the official standards, and the second pass fetched the Q-Net, legislation and ministry sources to reconcile. The cook standards had changed in between.
- Mechanical checks like clue bias cannot catch factual errors. A pass with the source documents in hand was necessary.

The apps are listed under [GAMES](/ko/games/) and [APPS](/ko/apps/), and some can be [played right in the browser](/play/). Updates go out on this blog and on [Instagram (@fadongkwon.soft)](https://www.instagram.com/fadongkwon.soft/).

> These banks are practice questions for study support and not actual exam questions. Statutes and exam standards change, so always check the latest notice from the administering body before sitting an exam.
{: .prompt-info }
