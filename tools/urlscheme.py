# -*- coding: utf-8 -*-
"""URL 체계 전환: 영어 = `/*`, 한국어 = `/ko/*` (2026-09-11, 사용자 결정)

## 왜 바꾸는가

전환 전에는 **홈만 규칙이 반대**였다.

    홈        /        = 영어      /ko/            = 한국어
    나머지    /about/  = 한국어    /en/about/      = 영어
              /posts/x = 한국어    /en/posts/x     = 영어

홈은 영어가 루트인데 나머지는 한국어가 루트라 어느 쪽이 기본인지 알 수 없었다.
규칙을 하나로 통일한다 — **영어가 루트, 한국어는 항상 `/ko/` 접두.**

## 규칙 (이 파일이 유일한 근거다)

    영어                              한국어
    /                                 /ko/
    /page/N/                          /ko/page/N/
    /posts/<slug>/                    /ko/posts/<slug>/
    /about/ /tarot/ /play/            /ko/about/ /ko/tarot/ /ko/play/
    /archives/ /categories/ /tags/    /ko/archives/ /ko/categories/ /ko/tags/
    /privacy/                         /ko/privacy/
    /tags/<slug>/ /categories/<slug>/ /ko/tags/:name/ /ko/categories/:name/

**언어 중립(양쪽이 함께 링크하며 접두를 붙이지 않는다)**
    /play/<게임>/   게임 자체가 브라우저 언어를 따른다
    /toss/<앱>/     토스 딥링크 랜딩
    /kids/*         아동용 앱 안내
    /assets/*       정적 파일

## 파일명 규칙 (2026-09-11, URL 규칙과 같은 방향)

**영어 = 무표식(기본), 한국어 = `ko-` 표식.** URL 규칙이 영어를 루트로 뒀는데 파일명이
거꾸로면(`_tabs/en-privacy.md` 가 루트 `/privacy/` 를 서빙) 다음 세션이 반드시 헷갈린다.

    _tabs/about.md            -> /about/        (영어)
    _tabs/ko-about.md         -> /ko/about/     (한국어)
    _includes/tarot-app-banner.html      영문 글이 쓴다
    _includes/tarot-app-banner-ko.html   한국어 글이 쓴다
    _includes/privacy-body.md            영문 (/privacy/)
    _includes/privacy-body-ko.md         한국어 (/ko/privacy/)

**예외 — 이름을 테마·젬이 정하는 것들.** 규칙 위반이 아니라 프레임워크 제약이다.

    _layouts/tags.html         테마 오버라이드는 **이름이 테마와 같아야** 성립한다.
    _layouts/categories.html   한국어 탭이 테마 레이아웃(layout: tags)을 쓰므로
                               이 이름은 한국어가 가진다.
    _layouts/en-*.html         우리가 새로 만든 영문 전용 레이아웃(site.en_posts 를
                               읽는다). 테마에 대응물이 없어 접두어로 구분한다.
    assets/js/data/search.json 젬이 생성하는 한국어 인덱스. 영문은 search-en.json.

이 넷을 무표식/ko- 로 뒤집으려면 테마 레이아웃 3개(archives·tag·category)를 복사해
`ko-` 로 두고 jekyll-archives 설정까지 바꿔야 한다. 오버라이드가 3개 늘어 테마 업그레이드
때마다 재대조할 파일만 많아지고 기능 이득은 없다 — 그래서 하지 않았다.

## 스토어에 등록된 URL

`/privacy/` 는 Play·토스 콘솔에 개인정보처리방침으로 등록돼 있다. 이 전환에서도
그 주소는 그대로 살아 있고 **본문이 영문이라는 점도 전과 같다**(원래 영문이었다).
한국어 이용자는 `/ko/privacy/` 로 간다.

## 옛 주소는 어떻게 되는가

- 옛 한국어 주소 `/posts/x/` → **404 가 아니라 같은 글의 영문판**이 나온다.
  한국어 브라우저는 metadata-hook 의 로케일 판정이 `/ko/posts/x/` 로 보낸다.
- 옛 영문 주소 `/en/...` → 이 스크립트가 meta-refresh 리다이렉트 스텁을 만든다
  (`en/posts/<slug>/index.html` 등). 2026-08-29 에 생긴 주소들이라 수는 적다.

## 사용법

    python tools/urlscheme.py --check    변경 대상만 보고(쓰기 없음)
    python tools/urlscheme.py --apply    실제 적용 (idempotent — 두 번 돌려도 같다)
"""
import io
import os
import re
import sys
import glob
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KO_DIR = os.path.join(ROOT, '_posts')
EN_DIR = os.path.join(ROOT, '_en_posts')
TABS_DIR = os.path.join(ROOT, '_tabs')

# 한국어 본문에서 /ko 접두를 붙일 경로들. 뒤에 슬래시가 오는 형태만 잡는다.
KO_PREFIX_PATHS = ('posts', 'tarot', 'about', 'archives', 'categories', 'tags', 'privacy')

# /play/ 는 허브만 옮긴다 — /play/<게임>/ 은 언어 중립이라 건드리면 안 된다.
RE_KO_PLAY_HUB = re.compile(r'(?<![\w/])/play/(?=[)"\'\s\]])')

# 이미 /ko/ 나 /en/ 이 붙은 것, /toss /kids /assets 는 제외
RE_KO_ADD = re.compile(r'(?<![\w/])/(' + '|'.join(KO_PREFIX_PATHS) + r')/')

RE_EN_STRIP = re.compile(r'(?<![\w/])/en/(posts|tarot|about|play|archives|categories|tags|privacy)/')


def read(p):
    return io.open(p, encoding='utf-8').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='\n').write(s)


def split_fm(text):
    m = re.match(r'^---\n(.*?\n)---\n', text.replace('\r\n', '\n'), re.S)
    if not m:
        raise ValueError('front matter 없음')
    return m.group(1), text.replace('\r\n', '\n')[m.end():]


def fm_set(fm, key, value):
    """front matter 의 key 를 value 로 바꾼다(없으면 끝에 추가)."""
    rx = re.compile(r'^' + re.escape(key) + r':[ \t]*.*$', re.M)
    if rx.search(fm):
        return rx.sub(key + ': ' + value, fm, count=1)
    return fm.rstrip('\n') + '\n' + key + ': ' + value + '\n'


def fm_get(fm, key):
    m = re.search(r'^' + re.escape(key) + r':[ \t]*(.*)$', fm, re.M)
    return m.group(1).strip() if m else None


def ko_body(body):
    """한국어 본문: 사이트 내부 경로에 /ko 접두를 붙인다(중립 경로는 제외)."""
    out = RE_KO_ADD.sub(lambda m: '/ko/' + m.group(1) + '/', body)
    out = RE_KO_PLAY_HUB.sub('/ko/play/', out)
    return out


def en_body(body):
    """영문 본문: /en 접두를 떼어 루트로 만든다."""
    return RE_EN_STRIP.sub(lambda m: '/' + m.group(1) + '/', body)


def slug_of(path):
    return os.path.basename(path)[:-3][11:]


# ─────────────────────────────────────────────────────────────────────────────
def migrate_posts(apply):
    changed = []
    for p in sorted(glob.glob(os.path.join(KO_DIR, '*.md'))):
        s = read(p)
        fm, body = split_fm(s)
        slug = slug_of(p)
        new_fm = fm_set(fm, 'alt_url', '/posts/' + slug + '/')
        new_body = ko_body(body)
        new = '---\n' + new_fm + '---\n' + new_body
        if new != s.replace('\r\n', '\n'):
            changed.append(os.path.relpath(p, ROOT))
            if apply:
                write(p, new)
    return changed


def migrate_en_posts(apply):
    changed = []
    for p in sorted(glob.glob(os.path.join(EN_DIR, '*.md'))):
        s = read(p)
        fm, body = split_fm(s)
        slug = slug_of(p)
        new_fm = fm_set(fm, 'permalink', '/posts/' + slug + '/')
        new_fm = fm_set(new_fm, 'alt_url', '/ko/posts/' + slug + '/')
        new_body = en_body(body)
        new = '---\n' + new_fm + '---\n' + new_body
        if new != s.replace('\r\n', '\n'):
            changed.append(os.path.relpath(p, ROOT))
            if apply:
                write(p, new)
    return changed


# 탭: (파일명, 영문인가, URL 이름)
# 파일명 규칙(2026-09-11): **영어 = 무표식(기본), 한국어 = ko- 표식** — URL 규칙과 같은 방향.
TABS = [
    ('ko-about.md', False, 'about'), ('about.md', True, 'about'),
    ('ko-tarot.md', False, 'tarot'), ('tarot.md', True, 'tarot'),
    ('ko-archives.md', False, 'archives'), ('archives.md', True, 'archives'),
    ('ko-categories.md', False, 'categories'), ('categories.md', True, 'categories'),
    ('ko-tags.md', False, 'tags'), ('tags.md', True, 'tags'),
    ('ko-privacy.md', False, 'privacy'), ('privacy.md', True, 'privacy'),
]


def migrate_tabs(apply):
    changed = []
    for name, is_en, url in TABS:
        p = os.path.join(TABS_DIR, name)
        if not os.path.exists(p):
            continue
        s = read(p)
        fm, body = split_fm(s)
        if is_en:
            fm = fm_set(fm, 'permalink', '/' + url + '/')
            fm = fm_set(fm, 'alt_url', '/ko/' + url + '/')
            body = en_body(body)
        else:
            fm = fm_set(fm, 'permalink', '/ko/' + url + '/')
            fm = fm_set(fm, 'alt_url', '/' + url + '/')
            body = ko_body(body)
        new = '---\n' + fm + '---\n' + body
        if new != s.replace('\r\n', '\n'):
            changed.append(os.path.relpath(p, ROOT))
            if apply:
                write(p, new)
    return changed


# 디렉터리 이동: (출발, 도착) — 영문 트리를 루트로, 한국어 허브를 /ko/ 로
MOVES = [
    ('en/tags', 'tags'),
    ('en/categories', 'categories'),
    ('en/play/index.md', 'play/index.md'),        # 한국어 play 를 먼저 옮긴 뒤 실행
]


def migrate_dirs(apply):
    done = []
    ko_play_src = os.path.join(ROOT, 'play', 'index.md')
    ko_play_dst = os.path.join(ROOT, 'ko', 'play', 'index.md')
    en_play_src = os.path.join(ROOT, 'en', 'play', 'index.md')

    # 1) 한국어 PLAY 허브 -> /ko/play/  (영문이 /play/ 를 차지하기 전에)
    if os.path.exists(ko_play_src) and os.path.exists(en_play_src):
        done.append('play/index.md -> ko/play/index.md')
        if apply:
            os.makedirs(os.path.dirname(ko_play_dst), exist_ok=True)
            shutil.move(ko_play_src, ko_play_dst)

    # 2) 영문 트리를 루트로
    #    ⚠️ 전환 후 en/tags·en/categories 에는 **리다이렉트 스텁 index.html** 만 남는다.
    #    가드 없이 재실행하면 그 스텁을 tags/index.html 로 옮겨 목록 페이지를 덮어쓴다.
    #    전환 전 상태는 하위 디렉터리(en/tags/<slug>/)가 있다는 것으로 구분한다.
    for src, dst in [('en/tags', 'tags'), ('en/categories', 'categories'),
                     ('en/play/index.md', 'play/index.md')]:
        s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
        if not os.path.exists(s):
            continue
        if os.path.isdir(s) and not any(os.path.isdir(os.path.join(s, x)) for x in os.listdir(s)):
            continue
        done.append(src + ' -> ' + dst)
        if apply:
            os.makedirs(os.path.dirname(d) if os.path.isfile(s) else d, exist_ok=True)
            if os.path.isdir(s):
                for item in os.listdir(s):
                    tgt = os.path.join(d, item)
                    if os.path.exists(tgt):
                        shutil.rmtree(tgt) if os.path.isdir(tgt) else os.remove(tgt)
                    shutil.move(os.path.join(s, item), tgt)
                os.rmdir(s)
            else:
                shutil.move(s, d)
    if apply:
        pd = os.path.join(ROOT, 'en', 'play')
        if os.path.isdir(pd) and not os.listdir(pd):
            os.rmdir(pd)
    return done


def fix_moved_pages(apply):
    """옮긴 페이지들의 front matter permalink/alt_url 과 본문 링크를 새 규칙으로."""
    changed = []
    targets = [
        ('ko/play/index.md', '/ko/play/', '/play/', False),
        ('play/index.md', '/play/', '/ko/play/', True),
    ]
    for rel, permalink, alt, is_en in targets:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        s = read(p)
        fm, body = split_fm(s)
        fm = fm_set(fm, 'permalink', permalink)
        fm = fm_set(fm, 'alt_url', alt)
        body = en_body(body) if is_en else ko_body(body)
        new = '---\n' + fm + '---\n' + body
        if new != s.replace('\r\n', '\n'):
            changed.append(rel)
            if apply:
                write(p, new)

    # 태그·카테고리 스텁의 permalink 에서 /en 제거
    for kind in ('tags', 'categories'):
        for p in sorted(glob.glob(os.path.join(ROOT, kind, '*', 'index.md'))):
            s = read(p)
            fm, body = split_fm(s)
            slug = os.path.basename(os.path.dirname(p))
            fm = fm_set(fm, 'permalink', '/' + kind + '/' + slug + '/')
            new = '---\n' + fm + '---\n' + body
            if new != s.replace('\r\n', '\n'):
                changed.append(os.path.relpath(p, ROOT).replace(os.sep, '/'))
                if apply:
                    write(p, new)
    return changed


STUB = """---
layout: null
sitemap: false
permalink: {old}
redirect_to: {new}
---
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Redirecting…</title>
<link rel="canonical" href="{new}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={new}">
</head><body>
<!-- 2026-08-29~09-11 사이에만 존재했던 영문 주소(/en/*)를 새 주소로 보낸다.
     tools/urlscheme.py 가 생성한다. 몇 달 뒤 통째로 지워도 된다. -->
<p>Redirecting to <a href="{new}">{new}</a>…</p>
</body></html>
"""


def gen_en_redirect_stubs(apply):
    """옛 영문 주소(/en/*)가 404 가 되지 않게 meta-refresh 스텁을 만든다.

    본문이 있는 페이지만 만든다 — /en/tags/<slug>/ 같은 목록 페이지는 고유 내용이
    없어 색인 가치가 없으므로 제외한다(수도 127개로 많다).

    ⚠️ **예약 글(미래 날짜)은 스텁을 만들지 않는다.** 그 글은 /en/... 에도 공개된 적이
    없어서 보존할 옛 주소가 애초에 없고, 스텁이 링크하는 새 주소가 아직 생성되지 않아
    **htmlproofer 가 빌드를 죽인다**(2026-09-11 실제로 이걸로 실패, 예약 14편 x 링크 2개).
    """
    import datetime
    now = datetime.datetime.now()

    def is_future(path):
        fm, _ = split_fm(read(path))
        v = fm_get(fm, 'date') or ''
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?', v)
        if not m:
            return False
        return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                 int(m.group(4) or 0), int(m.group(5) or 0)) > now

    made = []
    pairs = []
    for p in sorted(glob.glob(os.path.join(EN_DIR, '*.md'))):
        if is_future(p):
            continue
        slug = slug_of(p)
        pairs.append(('/en/posts/' + slug + '/', '/posts/' + slug + '/'))
    for name in ('about', 'tarot', 'play', 'archives', 'categories', 'tags', 'privacy'):
        pairs.append(('/en/' + name + '/', '/' + name + '/'))

    for old, new in pairs:
        rel = old.strip('/').split('/')
        d = os.path.join(ROOT, *rel)
        f = os.path.join(d, 'index.html')
        content = STUB.format(old=old, new=new)
        if not os.path.exists(f) or read(f) != content:
            made.append(old)
            if apply:
                os.makedirs(d, exist_ok=True)
                write(f, content)
    return made


def main():
    apply = '--apply' in sys.argv[1:]
    if not apply and '--check' not in sys.argv[1:]:
        print(__doc__)
        return 1

    steps = [
        ('한국어 포스트(alt_url·본문 링크)', migrate_posts),
        ('영문 포스트(permalink·alt_url·본문 링크)', migrate_en_posts),
        ('탭 12개(permalink·alt_url)', migrate_tabs),
        ('디렉터리 이동', migrate_dirs),
        ('옮긴 페이지 permalink 정리', fix_moved_pages),
        ('/en/* 리다이렉트 스텁', gen_en_redirect_stubs),
    ]
    total = 0
    for label, fn in steps:
        items = fn(apply)
        total += len(items)
        print('[%s] %s: %d건' % ('적용' if apply else '대상', label, len(items)))
        for x in items[:6]:
            print('    ' + str(x))
        if len(items) > 6:
            print('    ... 그 외 %d건' % (len(items) - 6))
    print()
    print('합계 %d건 %s' % (total, '적용됨' if apply else '(--apply 로 실행)'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
