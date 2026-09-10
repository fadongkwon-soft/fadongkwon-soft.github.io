---
title: 만든 앱
description: Google Play와 앱인토스에 올라가 있는 파동권소프트 앱 전체 목록입니다. 공용 레지스트리에서 자동으로 만들어지므로 항상 최신입니다.
alt_url: /apps/
permalink: /ko/apps/
---

<!-- ⚠️ 이 목록은 손으로 고치지 않는다. 루트 apps.csv(크로스 프로모션 단일 소스)를
     _plugins/apps-registry.rb 가 빌드 시점에 읽어 렌더한다. 앱을 내면 게임 저장소에서
     `pnpm publish:registry` 로 apps.csv 가 갱신·푸시되고, 그 푸시가 이 페이지를 다시 만든다. -->

아래 목록은 모든 앱이 함께 쓰는 레지스트리에서 자동으로 만들어집니다. 새 앱이 라이브가 되면 이 페이지도 같이 갱신되므로, 손으로 적어 두고 잊어버릴 목록이 없습니다.

지금 **{{ site.data.apps_count }}개**가 라이브입니다.

| | 앱 | Google Play | 앱인토스 |
| --- | --- | --- | --- |
{% for a in site.data.apps -%}
| {% if a.icon_path != '' %}![{{ a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | **{{ a.name }}**<br>{{ a.tagline }} | {% if a.on_play %}[받기](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}—{% endif %} | {% if a.toss_landing %}[열기]({{ a.toss_landing }}){% else %}—{% endif %} |
{% endfor %}

이 중 일부는 브라우저에서 바로 해볼 수 있습니다 — [PLAY](/ko/play/)에 있습니다. 각 앱을 만들며 겪은 이야기는 [개발 기록](/ko/archives/)에 적어 두었습니다.
