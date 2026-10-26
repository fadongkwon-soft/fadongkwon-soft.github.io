---
# ⚠️ layout 을 빼면 페이지가 **사이트 껍데기 없이** 나간다 — /apps/ 와 같은 함정(2026-09-11).
layout: page
title: Games
description: Every Fadongkwon Soft game with its live status on Google Play and Apps in Toss — generated from the shared registry, so it is never out of date.
lang: en
locale: en_US
permalink: /games/
alt_url: /ko/games/
---

<!-- 2026-10-09 APPS 를 GAMES · APPS 둘로 나눴다(사용자 결정). 이 목록도 손으로 고치지 않는다 —
     apps.csv 를 _plugins/apps-registry.rb 가 읽어 apps_games 로 넘긴다. 게임 판정은 tags 의 '게임' +
     사이트에서만 게임으로 보이는 SITE_GAME_IDS(병 돌리기·주스 스피너). 토스 칸은 on_toss 를 먼저 본다. -->

Everything below is generated from the registry every app shares, so it updates itself when a new game goes live. The two store columns track each platform separately, because a game can be on only one of them, or reachable on Apps in Toss only inside a hub.

**{{ site.data.apps_games | size }} games** — {{ site.data.apps_games | where: 'on_play', true | size }} live on Google Play, {{ site.data.apps_games | where: 'on_toss', true | size }} on Apps in Toss, plus {{ site.data.apps_games | where_exp: 'a', 'a.toss_hub' | size }} available inside an Apps in Toss hub. Newest first.

> On Apps in Toss, similar apps have been bundled into a single **FDK hub** since October 26, 2026. Toss changed how mini apps are surfaced, and the number of apps one account can list had hit its limit, so the existing standalone apps were turned into hubs. An entry marked "In …" in the Apps in Toss column is available inside that hub, and old links now open the hub. The full story is in [the hub conversion post](/posts/toss-hub-conversion/).
{: .prompt-info }

| | Game | Released | Google Play | Apps in Toss |
| --- | --- | --- | --- | --- |
{% for a in site.data.apps_games -%}
| {% if a.icon_path != '' %}![{{ a.name_en | default: a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | {% if a.post_en %}[**{{ a.name_en | default: a.name }}**]({{ a.post_en }}){% else %}**{{ a.name_en | default: a.name }}**{% endif %} {% include app-badge.html id=a.id %}<br>{{ a.tagline_en | default: a.tagline }} | {{ a.released }} | {% if a.on_play and a.play_landing %}[Install]({{ a.play_landing }}){: data-direct="https://play.google.com/store/apps/details?id={{ a.play_package }}"}{% elsif a.on_play %}[Install](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}coming soon{% endif %} | {% if a.on_toss and a.toss_landing %}[Open]({{ a.toss_landing }}){: data-direct="{{ a.toss_scheme }}"}{% elsif a.on_toss %}live{% elsif a.toss_hub and a.toss_hub.landing %}[In {{ a.toss_hub.name_en | default: a.toss_hub.name }}]({{ a.toss_hub.landing }}){: data-direct="{{ a.toss_hub.scheme }}"}{% elsif a.toss_hub %}In {{ a.toss_hub.name_en | default: a.toss_hub.name }}{% else %}not on Toss{% endif %} |
{% endfor %}

**Tap a game's name to read its introduction post** (games without one are not linked). Learning, exam-prep and fortune apps are on [Apps](/apps/), and the ones that run straight in a browser are on [PLAY](/play/). For the story behind each one, the [dev log](/archives/) has the details.

{% include apps-direct-links.html %}
