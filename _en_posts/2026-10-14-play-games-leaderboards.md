---
title: Adding Google Play Games Leaderboards to 25 Games That Used Toss Rankings — One Place in Code, 60 Clicks per App in the Console
description: I am adding Google Play Games leaderboards to the Google Play versions of 25 minigames that already use the Toss game center ranking. Game code stays untouched; one shared platform module switches the ranking button. The console setup took nine steps per app. Here is where I got stuck, from Cloud project quotas and two signing keys to sort orders you cannot change after publishing
image:
  path: /assets/img/20261014_play-games-leaderboards/cover.png
  alt: Google Play Games leaderboards for 25 minigames, progress as of October 10
date: 2026-10-14 09:00:00 +0900
categories: [Devlog, Platform]
permalink: /posts/play-games-leaderboards/
alt_url: /ko/posts/play-games-leaderboards/
tags: [google play, android, minigame, solo developer, dev log]
---

A month ago I [added record tabs to my minigames](/posts/leaderboard-record-tabs/). Daily, weekly, monthly and all-time records stay inside the app, and the global ranking that compares you with others is handed off to the Toss game center.

The problem was the **Google Play version**. The same games are also on the Play Store, and there is no Toss game center there. Play users could see their own records but had nowhere to compare with anyone else.

So I decided to add **Google Play Games Services (PGS) leaderboards** to all 25 games that use the Toss ranking. There was a suggestion to try one or two first, but I went with adding it to every game that keeps a score. This post is a progress report on that work.

## The game code stays untouched

Changing the ranking code in each of 25 games means 25 chances to make a mistake. So the switch happens in **one shared platform module**, the same one I built for the record tabs.

- When the app starts, it asks the Android side whether a PGS leaderboard is configured.
- If it is, the existing Toss ranking button turns into **"🏆 Play Games ranking"**, and tapping it opens the PGS leaderboard screen.
- If not, everything works as before.

Games still just call "save record" when a round ends. The platform module decides whether that record goes to Toss or to PGS. Each app's leaderboard ID lives in a single table (app name, sort order, format, ID), and **PGS is switched on at build time only for apps whose ID is filled in.** Apps whose console setup is not finished have an empty ID, so they automatically ship as before.

## Two things done differently from Toss

**Submit every round.** On Toss I only submit a score when it is a new personal best. PGS keeps the best score for today, this week and all time on its own, so I submit every round, best or not. That is what fills the "today" and "this week" tabs.

**Upload the old best score once.** Someone who played a lot before the update would not show up in the ranking until they beat their own best. So the first time the app connects to PGS, it uploads the best score already stored on the device, **once**. The Toss side has the same mechanism, but the two are tracked separately so they never affect each other.

There are two score formats. Games where a higher score is better (Snake, 2048 and so on) submit a number, and games where finishing faster is better (Minesweeper, Sudoku and so on) submit a time in milliseconds. **A leaderboard's sort order cannot be changed after publishing,** so I checked the table against the console values before creating each one.

## Nine console steps per app

The code was a one-time job, but the console setup has to be done for every app. Trying it once with Snake gave this order, at about 60 clicks per app.

1. Create a Google Cloud project
2. In Play Console, create a Play Games Services project and link it to the project from step 1
3. Set up and publish the OAuth consent screen in Cloud (app name, support email, homepage, privacy policy)
4. Create an Android OAuth client with the SHA-1 fingerprint of the app signing key
5. Register that client as a credential in Play Console
6. Create the leaderboard
7. Fill in the game properties (display name, description, category, icon, feature graphic)
8. Publish the Play Games Services project
9. Add the PGS items to the Data safety form

I got stuck in four places.

- **One Cloud project per PGS project.** Every app needs its own Cloud project, and my account's project quota was smaller than the number of apps left. I have requested a quota increase and am waiting for a reply.
- **Apps with two signing keys.** In August and September I upgraded the signing key of almost every app. People on versions signed with the old key also need to sign in, so I had to create **one more OAuth client and one more credential, using the SHA-1 of the previous key** as well as the current one. The previous key's fingerprint is inside the "previous app signing key" menu on the app signing page in Play Console.
- **Do not upload a logo to the consent screen.** Uploading a logo to the OAuth consent screen triggers Google's app verification review. I filled in only the name and links and left the logo empty.
- **The Data safety form.** Using PGS means declaring that you collect a user ID and app activity (score submissions). I added those two items as app functionality and optional. I made one form with the common items for my ad-supported apps plus these two lines, and uploaded the same form for each app.

I did this by clicking through the console in a browser, and **when the browser tab went into the background, its timers slowed down**, so dropdowns would not open and the work stalled. During console work, that tab had to stay in front.

## Where things stand

As of October 10, when I am writing this:

| Stage | Games |
| --- | ---: |
| Console done, update submitted for review | 9 |
| Console done, app not built yet | 5 |
| Waiting for Cloud project quota | 11 |
| Total | 25 |

Snake, the first one, I checked on a real phone (Galaxy S23). Opening the app signs in to Play Games automatically, the old best score of 220 is uploaded once, and the ranking button opens the PGS leaderboard screen. After that I submitted updates for 8 more: Brick Breaker, 2048, Hangul Word Guess, All Lights Off, Pixel Pong, Sky Jump, Tap Bird and Tower Stack. The remaining 11 will follow as the quota increases.

## New games get it from the start

Having added this to 25 games after the fact, I decided that any new score-based game will **include PGS from the start**. I added a PGS item to the release checklist, and the release check script now fails when "the app is live on Play but its leaderboard ID is empty." A new app has only one signing key, so one client is enough.

Once all of them are done, I will look at how often Play users actually open the ranking and whether the return rate changes, and write that up separately.
