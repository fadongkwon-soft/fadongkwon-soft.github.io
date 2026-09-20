---
title: Turning 27 Games Into Reels — 1.5x Speed, 9:16, and Links That Do Not Click
description: Our Instagram account had 27 posts and not one video. The gameplay clips recorded for YouTube Shorts were already sitting there, so we re-cut all of them into Reels. Here is what mattered — why 1.5x, where a vertical video gets cropped, and the fact that a link in an Instagram caption is not clickable
date: 2026-09-24 09:00:00 +0900
categories: [Devlog, Retrospective]
permalink: /posts/instagram-reels-27/
alt_url: /ko/posts/instagram-reels-27/
tags: [instagram, reels, ffmpeg, marketing, solo developer, devlog]
---
## Info
> Our Instagram account had 27 posts and not a single video. The gameplay clips we had already recorded for YouTube Shorts were sitting unused, so we re-cut all of them into Reels. This post covers the three things that mattered: 1.5x speed, keeping the original 9:16 frame, and the fact that links in an Instagram caption are not clickable.
{: .prompt-info }

## Not a single video

Opening the account, all 27 posts were image carousels — three app cards bundled together each time. Reels: zero.

But 25 gameplay clips recorded for YouTube Shorts were already on disk. This was not something to make. It was **inventory that only needed a change of format**.

## 1. 1.5x speed

The originals run 35 to 47 seconds. That is fine for Shorts, but a silent 30-second gameplay clip is long for Reels. The thumb moves first.

At 1.5x they became 23 to 31 seconds. Same content, different feel.

```bash
ffmpeg -i gameplay.mp4 \
  -filter:v "setpts=PTS/1.5" -an \
  -c:v libx264 -preset medium -crf 23 \
  -pix_fmt yuv420p -movflags +faststart \
  reels/snake.mp4
```

`-an` drops the audio. Game captures either have no sound or nothing worth keeping, and viewers add their own music anyway. Instagram's editor even labels it "video without sound".

## 2. Keeping 9:16 is not the default

This is where we got it wrong once.

Upload a video and the crop screen appears with **1:1 selected by default**. Click straight through and a 1080×1920 vertical video loses its top and bottom — exactly where the score panel and the buttons live.

You have to open the ratio picker on the crop screen and choose **"Original"**. The preview then returns to 0.56, which is 9:16. We clicked through on one clip and had to walk back from the edit step to fix it.

## 3. The clips were not all in one place

Twenty-five of them followed our `store-assets/<app>/gameplay.mp4` convention. So we scanned the file list and concluded that two party apps had no video. Wrong.

Those two predate the convention, and their **iOS simulator recordings** lived in a completely different folder. Assets created before a rule exists cannot be found by that rule.

They turned out to be 1206×2622 — taller than 9:16, with an iOS status bar on top and empty space at the bottom. We cropped the status bar away and landed on 9:16.

```bash
ffmpeg -i preview.mp4 \
  -filter:v "crop=1206:2144:0:180,setpts=PTS/1.5,scale=1080:1920" -an \
  -c:v libx264 -crf 23 -pix_fmt yuv420p -movflags +faststart \
  reels/spin-the-bottle.mp4
```

`crop=1206:2144:0:180` takes 180px off the top (the status bar) and 298px off the bottom (empty space) to make 9:16. A 90MB source shrinking to 5MB was a bonus.

## 4. Links in a caption do not click

We put three store lines at the end of every caption.

```
Google Play: https://play.google.com/store/apps/details?id=com.fadongkwon.snake
Toss Mini App: https://fadongkwon.com/toss/snake/
Homepage: https://fadongkwon.com
```

Worth knowing: **a URL in an Instagram caption is not a link.** The only clickable link is the one in the profile. We include them anyway for two reasons — to say in words where the app can be found, and to let someone read the address and type it.

There is also a reason only Toss goes through our own site. **A Toss mini app has no public web address.** It opens inside the Toss app and nowhere else. So we keep a `fadongkwon.com/toss/<app>` landing page that hands off to Toss on a phone and explains itself on a desktop.

## The part we could not finish

The plan was to add the same three lines to the captions of the 27 existing image posts. **Caption edits do not stick.** The edit request comes back `200 OK` and the caption is unchanged. Even appending 40 characters behaves the same way.

On the same account at the same hour, 27 new posts went up without a hitch. So this is not a blocked account — it is **a restriction on editing specifically**. We moved the link work to the Reels side and will revisit the old posts when the restriction lifts.

## Takeaways

- If clips already exist, a format change alone can open a channel
- 1.5x fits the Reels rhythm without hurting the content
- Vertical video survives only if you **pick "Original" on the crop screen yourself**
- Assets made before a convention cannot be found by that convention
- Instagram caption links do not click. Write them anyway
