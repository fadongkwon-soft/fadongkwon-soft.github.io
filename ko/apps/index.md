---
# ⚠️ layout 을 빼면 페이지가 **사이트 껍데기 없이** 나간다 —
#    head 의 CSS 도 없어서 접근성용 숨김 텍스트가 그대로 보이고 표도 무포맷이 된다.
#    HTTP 200 이라 아무 검사도 못 잡는다(2026-09-11 실제로 겪음).
layout: page
title: APPS — 만든 앱
description: 파동권소프트의 학습·시험 대비·운세·모임용 앱과 Google Play·앱인토스 각각의 출시 현황입니다. 공용 레지스트리에서 자동으로 만들어지므로 항상 최신입니다.
alt_url: /apps/
permalink: /ko/apps/
---

<!-- ⚠️ 이 목록은 손으로 고치지 않는다. 루트 apps.csv(크로스 프로모션 단일 소스)를
     _plugins/apps-registry.rb 가 빌드 시점에 읽어 렌더한다. 앱을 내면 게임 저장소에서
     `pnpm publish:registry` 로 apps.csv 가 갱신·푸시되고, 그 푸시가 이 페이지를 다시 만든다.
     플랫폼별 상태를 칸마다 보여준다 — 한쪽만 라이브인 앱이 실제로 있다.
     ⚠️ 토스 칸은 **on_toss 를 먼저** 본다. 랜딩 페이지(toss/<id>.html)는 출시 전에
        미리 만들어 두는 경우가 있어서, 랜딩 존재만 보면 미출시 미니앱으로 링크가 걸린다
        (2026-09-11 실제로 3개가 그렇게 나갔다). -->

아래 목록은 모든 앱이 함께 쓰는 레지스트리에서 자동으로 만들어집니다. 새 앱이 라이브가 되면 이 페이지도 같이 갱신되므로, 손으로 적어 두고 잊어버릴 목록이 없습니다. 스토어 두 칸은 각각 따로 표시합니다 — 한쪽에만 나와 있거나, 앱인토스에서는 허브 안에서만 이용하는 앱이 있기 때문입니다.

**앱 {{ site.data.apps_others | size }}개** — Google Play {{ site.data.apps_others | where: 'on_play', true | size }}개, 앱인토스 {{ site.data.apps_others | where: 'on_toss', true | size }}개 라이브이고, 앱인토스 허브 안에서 이용하는 앱이 {{ site.data.apps_others | where_exp: 'a', 'a.toss_hub' | size }}개 더 있습니다. 최근 출시 순입니다. 게임은 [GAMES](/ko/games/)에 따로 모았습니다.

학습·시험 대비, 모임용, 운세 앱입니다.

<!-- 타로 사전 입구(2026-10-09) — 사이드바 TAROT 메뉴를 빼면서 여기(타로 앱 옆)와 ABOUT 으로 옮겼다. -->
> 🔮 타로 앱(타로 운세·운세 타로핑)의 해석을 카드 78장 한 장씩 풀어 쓴 **[타로 카드 의미 사전](/ko/tarot/)**도 있습니다.
{: .prompt-info }

> 앱인토스에서는 2026년 10월 26일부터 비슷한 앱을 **파동권 허브** 하나로 묶어 냅니다. 토스의 미니앱 노출 방식이 바뀌고 계정당 등록할 수 있는 앱 수도 한도에 닿아, 기존 개별 앱 자리를 허브로 바꿨기 때문입니다. 그래서 앱인토스 칸에 '○○에서'라고 적힌 항목은 그 허브 안에서 그대로 이용할 수 있고, 예전 링크로 들어가도 허브가 열립니다. 자세한 이야기는 [허브 전환기](/ko/posts/toss-hub-conversion/)에 적었습니다.
{: .prompt-info }

| | 앱 | 출시 | Google Play | 앱인토스 |
| --- | --- | --- | --- | --- |
{% for a in site.data.apps_others -%}
| {% if a.icon_path != '' %}![{{ a.name }}]({{ a.icon_path }}){: width="40" height="40" .normal}{% else %}{{ a.emoji }}{% endif %} | {% if a.post_ko %}[**{{ a.name }}**]({{ a.post_ko }}){% else %}**{{ a.name }}**{% endif %} {% include app-badge.html id=a.id %}<br>{{ a.tagline }} | {{ a.released }} | {% if a.on_play and a.play_landing %}[설치]({{ a.play_landing }}){: data-direct="https://play.google.com/store/apps/details?id={{ a.play_package }}"}{% elsif a.on_play %}[설치](https://play.google.com/store/apps/details?id={{ a.play_package }}){% else %}준비 중{% endif %} | {% if a.on_toss and a.toss_landing %}[열기]({{ a.toss_landing }}){: data-direct="{{ a.toss_scheme }}"}{% elsif a.on_toss %}출시됨{% elsif a.toss_hub and a.toss_hub.landing %}[{{ a.toss_hub.name }}에서]({{ a.toss_hub.landing }}){: data-direct="{{ a.toss_hub.scheme }}"}{% elsif a.toss_hub %}{{ a.toss_hub.name }}에서{% else %}미출시{% endif %} |
{% endfor %}

**앱 이름을 누르면 그 앱의 소개 글로 갑니다**(소개 글이 아직 없는 앱은 링크가 없습니다). 게임은 [GAMES](/ko/games/)에, 브라우저에서 바로 해볼 수 있는 것은 [PLAY](/ko/play/)에 있습니다. 각 앱을 만들며 겪은 이야기는 [개발 기록](/ko/archives/)에 적어 두었습니다.

{% include apps-direct-links.html %}
