---
# ⚠️ layout 을 빼면 페이지가 **사이트 껍데기 없이** 나간다 — /ko/apps/ 와 같은 함정(2026-09-11).
layout: page
title: GAMES — 만든 게임
description: 파동권소프트 게임 전체와 Google Play·앱인토스 각각의 출시 현황입니다. 공용 레지스트리에서 자동으로 만들어지므로 항상 최신입니다.
alt_url: /games/
permalink: /ko/games/
---

<!-- 2026-10-09 APPS 를 GAMES · APPS 둘로 나눴다(사용자 결정). 이 목록도 손으로 고치지 않는다 —
     apps.csv 를 _plugins/apps-registry.rb 가 읽어 apps_games 로 넘긴다. 게임 판정은 tags 의 '게임' +
     사이트에서만 게임으로 보이는 SITE_GAME_IDS(병 돌리기·주스 스피너). 토스 칸은 on_toss 를 먼저 본다
     (랜딩만 있고 미출시인 앱이 있다 — /ko/apps/ 의 주석 참조). -->

아래 목록은 모든 앱이 함께 쓰는 레지스트리에서 자동으로 만들어집니다. 새 게임이 라이브가 되면 이 페이지도 같이 갱신됩니다. 스토어 두 칸은 각각 따로 표시합니다 — 한쪽은 출시됐고 다른 쪽은 심사 중인 게임이 실제로 있기 때문입니다.

**게임 {{ site.data.apps_games | size }}개** — Google Play {{ site.data.apps_games | where: 'on_play', true | size }}개, 앱인토스 {{ site.data.apps_games | where: 'on_toss', true | size }}개 라이브입니다. 최근 출시 순입니다.

| | 게임 | 출시 | Google Play | 앱인토스 |
| --- | --- | --- | --- | --- |
{% for a in site.data.apps_games -%}
| {% if a.icon_path != '' %}![{{ a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | {% if a.post_ko %}[**{{ a.name }}**]({{ a.post_ko }}){% else %}**{{ a.name }}**{% endif %} {% include app-badge.html id=a.id %}<br>{{ a.tagline }} | {{ a.released }} | {% if a.on_play and a.play_landing %}[설치]({{ a.play_landing }}){: data-direct="https://play.google.com/store/apps/details?id={{ a.play_package }}"}{% elsif a.on_play %}[설치](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}*심사 중*{% endif %} | {% if a.on_toss and a.toss_landing %}[열기]({{ a.toss_landing }}){: data-direct="{{ a.toss_scheme }}"}{% elsif a.on_toss %}출시됨{% else %}*심사 중*{% endif %} |
{% endfor %}

**게임 이름을 누르면 그 게임의 소개 글로 갑니다**(소개 글이 아직 없는 게임은 링크가 없습니다). 학습·시험 대비·운세 앱은 [APPS](/ko/apps/)에, 브라우저에서 바로 해볼 수 있는 것은 [PLAY](/ko/play/)에 있습니다. 각 게임을 만들며 겪은 이야기는 [개발 기록](/ko/archives/)에 적어 두었습니다.

{% include apps-direct-links.html %}
