---
title: Apps
description: Every app from Fadongkwon Soft that is live on Google Play or Apps in Toss — generated from the shared registry, so it is never out of date.
lang: en
locale: en_US
permalink: /apps/
alt_url: /ko/apps/
---

<!-- ⚠️ 이 목록은 손으로 고치지 않는다. 루트 apps.csv(크로스 프로모션 단일 소스)를
     _plugins/apps-registry.rb 가 빌드 시점에 읽어 렌더한다. 앱을 내면 게임 저장소에서
     `pnpm publish:registry` 로 apps.csv 가 갱신·푸시되고, 그 푸시가 이 페이지를 다시 만든다. -->

Everything below is generated from the registry every app shares, so it updates itself when a new app goes live — there is no hand-written list to forget.

**{{ site.data.apps_count }} apps** are live right now.

| | App | Google Play | Apps in Toss |
| --- | --- | --- | --- |
{% for a in site.data.apps -%}
| {% if a.icon_path != '' %}![{{ a.name_en | default: a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | **{{ a.name_en | default: a.name }}**<br>{{ a.tagline_en | default: a.tagline }} | {% if a.on_play %}[Install](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}—{% endif %} | {% if a.toss_landing %}[Open]({{ a.toss_landing }}){% else %}—{% endif %} |
{% endfor %}

Some of these also run straight in a browser — see [PLAY](/play/). For the story behind each one, the [dev log](/archives/) has the details.
