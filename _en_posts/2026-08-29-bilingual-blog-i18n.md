---
title: 8 Traps I Hit Making This Blog Bilingual (Jekyll + Chirpy)
description: Turning a Korean-only Jekyll blog into English-first with automatic locale selection — scheduled-post pitfalls, theme override contracts, a zombie service worker, and running batch translation for 95 posts
date: 2026-08-29 16:30:00 +0900
categories: [Blogging, Episode]
permalink: /en/posts/bilingual-blog-i18n/
alt_url: /posts/bilingual-blog-i18n/
tags: [jekyll, chirpy, i18n, seo, github pages, solo developer]
---
## Info
> How I turned a Korean-only Jekyll (Chirpy) blog into a bilingual site — English by
> default, Korean auto-selected for Korean browsers — and the eight traps I hit along
> the way. You are reading the result right now.
{: .prompt-info }

This blog used to be Korean-only. As my apps went global, the blog needed to be
searchable in English too, so over two days I **translated 95 posts and rebuilt the
site as English-first, with Korean served only to Korean visitors.**

The punchline: the translation itself was the easy part. The hard part was the
**implicit assumptions baked into the static site generator and the theme.** Here is
the list of traps, in the order I stepped on them.

## 1. Mixing two languages in one post is terrible for SEO

My first idea was to put Korean and English side by side in each post. Clear ❌.
Search engines assume one language per URL. Mixed content muddies language detection,
halves your keyword density, and you only get one `<title>` and one `<html lang>` —
so you can never write a title tuned for English queries.

The right answer is **separate URLs per language plus reciprocal hreflang**. Korean
posts kept their original URLs (`/posts/…`), English versions went under
`/en/posts/…`, and each document points at its twin with
`<link rel="alternate" hreflang>`. Not breaking a single indexed Korean URL was the
non-negotiable constraint.

## 2. Auto-redirecting by Accept-Language starves crawlers

"Just read the browser language and redirect" is half a trap. Googlebot mostly crawls
from US IPs with English headers, so an unconditional redirect means **crawlers never
see one of your languages.**

The compromise: keep hreflang as the source of truth for indexing, and do language
selection in client-side JS — but ① skip crawler user agents, ② remember an explicit
switcher choice in localStorage and let it override the automatic pick, and ③ use
`location.replace` so the back button doesn't get polluted. Crawlers get hreflang;
humans get the script.

## 3. Jekyll collections only half-support scheduled publishing

This blog schedules posts with future dates plus a daily cron build. `_posts` filters
future posts at read time, but **collections keep future documents in
`site.en_posts`** — only the page output is skipped. So listings, the sitemap and the
search index all link to pages that don't exist yet, and htmlproofer kills the build.

Every place that iterates the collection needs a date filter:

```liquid
{% raw %}{% assign live = site.en_posts | where_exp: 'p', 'p.date <= site.time' %}{% endraw %}
```

Bonus lesson: if post bodies link to a post scheduled for later the same day, **don't
push during the publishing window** (09:00–10:40 KST here). The link target doesn't
exist yet and the build fails.

## 4. Themes branch on the layout *name*

The trap that cost me the most time. I rebuilt the home page as a language-neutral
layout and named it `lang-home`. Suddenly — only on home pages — grey gradients stuck
on top of images and the post cards got weird click targets.

The cause: Chirpy branches on the **string comparison** `page.layout == 'home'` in
four places (JS bundle selection, image wrapping, top bar, `<title>`). With a
different name, the home JS bundle never loaded (so image-loading placeholders never
cleared), and the content-image wrapper (a popup `<a>`) got nested inside the card's
`<a>`, which the HTML parser then split apart.

Lesson: **don't invent custom layout names — override the theme's layout under the
same name.** The name is the contract.

## 5. The HTML compressor kills scripts that use // comments

My auto-locale script simply didn't run after deploy. The console showed a single
`SyntaxError: Unexpected end of input`. Chirpy's HTML compression **removes every
newline**, so a `//` comment inside an inline script swallowed all the code that
followed it on the (now single) line. Inline `<script>` blocks may only use block
comments (`/* */`).

## 6. Turning off PWA creates a zombie service worker

Right after the relaunch, the site felt slow and looked broken — not because of the
new code, but because **the service worker installed before the relaunch kept serving
the old site from cache.** Worse: disabling PWA removed `sw.min.js`, so the old
worker lost its update path and got stuck forever.

The fix is a **kill-switch service worker at the same path**. Service worker script
requests bypass the service worker itself, so the next visit always fetches the new
version — which deletes all caches, unregisters itself, and reloads open tabs.

## 7. jekyll-archives doesn't know about collections

Per-category and per-tag pages are generated by jekyll-archives from `site.posts`
only — the English collection is invisible to it. I first hacked around it with one
long page of anchor sections, got a well-deserved "this looks weird", and ended up
making the **translation pipeline auto-generate stub pages per category and tag**
(currently 15 categories + 72 tags). New tags grow their own pages; removed tags get
cleaned up. Zero manual work.

## 8. Batch translation is protected by deterministic post-processing, not by specs

The 95 posts were translated by several sub-agents in parallel, which surfaced a fun
failure mode: give the spec both "preserve the structure 1:1" and "use section titles
from this table", and each batch judges differently when a source title isn't in the
table. However much you polish the spec, judgment calls will drift.

What actually worked wasn't a stricter spec but **mechanical verification and
post-processing**: a script that hard-gates heading count/hierarchy against the
source, and a fixup tool that overwrites every mechanical field — dates, paths, tags,
links — from the source of truth. Whether the translator is a human or an AI, let
them touch prose only.

## Wrap-up

After two days of rework, this blog now has:

- English as the default (root `/`), Korean at `/ko/` with all original post URLs intact
- Automatic language selection by browser locale, with manual choice remembered
- 95 posts × 2 languages, full hreflang, and scheduled posts that publish in both
  languages on the same day

Internationalizing a static site turned out to be less about translation and more
about **hunting down a system's implicit assumptions.** The eight items above are
that list.
