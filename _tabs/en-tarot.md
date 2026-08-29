---
title: Tarot Dictionary
description: >-
  The meaning of all 78 tarot cards — upright and reversed, plus readings for love,
  career, money and health. Original artwork and interpretations from the Rider–Waite imagery.
icon: fas fa-star
order: 2
lang: en
locale: en_US
permalink: /en/tarot/
alt_url: /tarot/
---

A dictionary working through the meaning of all 78 tarot cards, one card at a time. Each entry covers the symbols in the picture, the upright and reversed meanings, and how the card reads in specific situations — love, career, money, health.

The artwork is all drawn in-house, and the interpretations are written from scratch based on the traditional Rider–Waite imagery. All 78 cards are published, so you can jump straight to any card in the list below.

> These readings are for entertainment and self-reflection. For important decisions about money, health, or legal matters, always consult a qualified professional.
{: .prompt-warning }

{%- comment -%}
  ⚠️ 컬렉션은 `_posts` 와 달리 미래 날짜 문서가 site.en_posts 에 그대로 남는다.
  (Jekyll 4.3: PostReader#read_publishable 은 읽을 때 걸러내지만,
   Collection#read_document 는 `published:` 만 보고 future 는 write? 단계에서만 본다)
  따라서 목록에서 날짜로 직접 걸러야 한다 — 안 그러면 아직 생성되지 않은 페이지를
  링크해 htmlproofer 가 빌드를 실패시킨다.
  영문 글의 date 는 한국어 원문과 동일하게 두므로 양쪽이 같은 날 함께 공개된다.
{%- endcomment -%}
{% assign live_en = site.en_posts | where_exp: 'p', 'p.date <= site.time' %}
{% assign all_tarot = live_en | where_exp: 'p', 'p.categories contains "Tarot"' %}
{% if all_tarot.size > 0 %}**All {{ all_tarot.size }} cards included**{% endif %}

{% assign groups = "Major Arcana|Wands|Cups|Swords|Pentacles" | split: "|" %}
{% assign labels = "Major Arcana (22 cards)|Wands · Fire (14 cards)|Cups · Water (14 cards)|Swords · Air (14 cards)|Pentacles · Earth (14 cards)" | split: "|" %}
{% assign notes = "The 22 cards that deal with the large movements and turning points of a life. Read as a single journey from The Fool (0) to The World (21).|Passion and will, action and expansion. The suit of starting things and pushing them forward.|Emotion and relationship, love and intuition. The suit of what happens inside the heart.|Thought and judgement, communication and conflict. The suit of problems you have to think through.|The material world — money, work, and the results you can hold in your hand." | split: "|" %}

{% for g in groups %}
{% assign gi = forloop.index0 %}
{% assign group_posts = live_en | where_exp: 'p', 'p.categories contains g' %}
{% if group_posts.size > 0 %}
{% assign items = group_posts | sort: 'date' %}
## {{ labels[gi] }}

{{ notes[gi] }}

{% for p in items %}
{% assign nm = p.card_name | default: p.title %}
{% assign sub = p.title | split: '— ' | last %}
- [{{ nm }}]({{ p.url }}){% if sub != p.title %} — {{ sub }}{% endif %}
{% endfor %}
{% endif %}
{% endfor %}

## New to tarot?

The 78 cards split into two groups. The **22 Major Arcana** deal with the big phases of a life; the **56 Minor Arcana** deal with concrete, everyday situations. The Minors divide again into four suits, and each suit owns a different territory: Wands is what you want to do, Cups is what you feel, Swords is what you think and judge, Pentacles is what you can actually touch.

Drawing Wands for a question is a different kind of answer than drawing Pentacles. Ask "should I change jobs?" and a Wands card is asking about your drive and appetite; a Pentacles card is asking about terms and stability. Rather than memorising 78 individual meanings, learn which territory each suit points at first — the cards get much easier to read.

Numbers matter too. Ace is the seed, 2 is balance and choice, 3 is growth, 4 is stability, 5 is conflict, 6 is recovery, 7 is testing, 8 is mastery, 9 is just before completion, 10 is completion or excess. Overlay the number on the suit's territory and you get a rough meaning: Five of Pentacles becomes "lack in the material world."

{% include tarot-app-banner-en.html %}
