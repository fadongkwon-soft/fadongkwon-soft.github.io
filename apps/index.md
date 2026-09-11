---
# ⚠️ layout 을 빼면 페이지가 **사이트 껍데기 없이** 나간다 —
#    head 의 CSS 도 없어서 접근성용 숨김 텍스트가 그대로 보이고 표도 무포맷이 된다.
#    HTTP 200 이라 아무 검사도 못 잡는다(2026-09-11 실제로 겪음).
layout: page
title: Apps
description: Every Fadongkwon Soft app with its live status on Google Play and Apps in Toss — generated from the shared registry, so it is never out of date.
lang: en
locale: en_US
permalink: /apps/
alt_url: /ko/apps/
---

<!-- ⚠️ 이 목록은 손으로 고치지 않는다. 루트 apps.csv(크로스 프로모션 단일 소스)를
     _plugins/apps-registry.rb 가 빌드 시점에 읽어 렌더한다. 앱을 내면 게임 저장소에서
     `pnpm publish:registry` 로 apps.csv 가 갱신·푸시되고, 그 푸시가 이 페이지를 다시 만든다.
     플랫폼별 상태를 칸마다 보여준다 — 한쪽만 라이브인 앱이 실제로 있다.
     ⚠️ 토스 칸은 **on_toss 를 먼저** 본다. 랜딩 페이지(toss/<id>.html)는 출시 전에
        미리 만들어 두는 경우가 있어서, 랜딩 존재만 보면 미출시 미니앱으로 링크가 걸린다
        (2026-09-11 실제로 3개가 그렇게 나갔다). -->

Everything below is generated from the registry every app shares, so it updates itself when a new app goes live — there is no hand-written list to forget. The two store columns track each platform separately, because an app can be live on one and still in review on the other.

**{{ site.data.apps_count }} apps** — {{ site.data.apps_play_count }} live on Google Play, {{ site.data.apps_toss_count }} on Apps in Toss. Newest first.

## Games — {{ site.data.apps_games | size }}

| | App | Released | Google Play | Apps in Toss |
| --- | --- | --- | --- | --- |
{% for a in site.data.apps_games -%}
| {% if a.icon_path != '' %}![{{ a.name_en | default: a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | **{{ a.name_en | default: a.name }}**<br>{{ a.tagline_en | default: a.tagline }} | {{ a.released }} | {% if a.on_play and a.play_landing %}[Install]({{ a.play_landing }}){% elsif a.on_play %}[Install](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}*in review*{% endif %} | {% if a.on_toss and a.toss_landing %}[Open]({{ a.toss_landing }}){% elsif a.on_toss %}live{% else %}*in review*{% endif %} |
{% endfor %}

## Everything else — {{ site.data.apps_others | size }}

Learning and exam prep, party picks, and fortune-telling content.

| | App | Released | Google Play | Apps in Toss |
| --- | --- | --- | --- | --- |
{% for a in site.data.apps_others -%}
| {% if a.icon_path != '' %}![{{ a.name_en | default: a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | **{{ a.name_en | default: a.name }}**<br>{{ a.tagline_en | default: a.tagline }} | {{ a.released }} | {% if a.on_play and a.play_landing %}[Install]({{ a.play_landing }}){% elsif a.on_play %}[Install](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}*in review*{% endif %} | {% if a.on_toss and a.toss_landing %}[Open]({{ a.toss_landing }}){% elsif a.on_toss %}live{% else %}*in review*{% endif %} |
{% endfor %}

> **Spin the Bottle** and **Juice Spinner** look like games but are registered as non-games in the stores. When I started out, releasing a game in Korea involved a much heavier process, so I avoided the game category. Later releases go to Play as games first — which earns the rating automatically — and then on to Apps in Toss.
{: .prompt-info }

Some of these also run straight in a browser — see [PLAY](/play/). For the story behind each one, the [dev log](/archives/) has the details.
