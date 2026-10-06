# -*- coding: utf-8 -*-
"""예약 게시분이 공개될 때 빌드가 죽지 않는지 미리 점검한다.

## 왜 필요한가

htmlproofer(`Test site` 단계)는 **아직 생성되지 않은 페이지로의 내부 링크**를 실패로
본다. 예약 글은 공개 시각이 지나기 전에는 파일이 생성되지 않으므로, 이미 공개된 글이
예약 글의 URL 을 링크하고 있으면 **그 예약 글이 공개되는 날 cron 빌드가 죽는다.**
`i18n.py verify` 는 "URL 이 존재하는 글을 가리키는가"만 보므로 이 조합을 못 잡는다.

점검 항목
  1. ko/en 짝의 date 가 같은가 (다르면 한쪽만 먼저 공개돼 hreflang 짝이 깨진다)
  2. 공개된 글이 미래 글의 URL 을 링크하는가 (공개일에 htmlproofer 실패)
  3. 예약 글끼리의 링크는 공개 순서가 맞는가 (먼저 나오는 글이 나중 글을 링크하면 실패)
  4. permalink/alt_url 이 URL 규칙(영어 = /*, 한국어 = /ko/*)을 지키는가
  5. 홈 페이지네이션 스텁이 예약분 공개 후 쪽수까지 준비돼 있는가
  6. 본문·커버 이미지가 실재하는가 (예약 글은 htmlproofer 가 공개일까지 못 본다)
  7. [경고만] 앱 소개 글(categories 첫 값 Products)이 /apps/ 와 이어지는가 — 아래 check_app_posts

usage: python tools/check_scheduled.py
"""
import io
import os
import re
import csv
import sys
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_PER_PAGE = 10


def hub_only_categories():
    """_config.yml 의 `hub_only_categories: [A, B]` 한 줄 — tools/i18n.py 의 같은 함수와 맞출 것."""
    m = re.search(r'^hub_only_categories:\s*\[([^\]]*)\]', read(os.path.join(ROOT, '_config.yml')), re.M)
    if not m:
        raise SystemExit('_config.yml 에 hub_only_categories: [..] 한 줄이 없다')
    return [c.strip().strip('\'"') for c in m.group(1).split(',') if c.strip()]


def top_category(cats):
    """front matter 원문 `[Products, Game]` → 'Products'."""
    return cats.strip().strip('[]').split(',')[0].strip().strip('\'"')


def read(p):
    return io.open(p, encoding='utf-8').read().replace('\r\n', '\n')


def split_fm(text):
    m = re.match(r'^---\n(.*?\n)---\n', text, re.S)
    if not m:
        raise ValueError('front matter 없음')
    return m.group(1), text[m.end():]


def fm_get(fm, key):
    m = re.search(r'^' + re.escape(key) + r':[ \t]*(.*)$', fm, re.M)
    return m.group(1).strip() if m else None


def parse_date(v):
    if not v:
        return None
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2}))?', v)
    if not m:
        return None
    y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    hh = int(m.group(4) or 0)
    mm = int(m.group(5) or 0)
    return datetime.datetime(y, mo, d, hh, mm)


def collect_images(fm, body):
    """본문의 ![](/...) 와 front matter 의 커버(image: path:)를 모은다."""
    out = [m.group(1) for m in re.finditer(r'!\[[^\]]*\]\((/[^)\s]+)', body)]
    m = re.search(r'^image:\s*\n\s*path:\s*(\S+)', fm, re.M)
    if m:
        out.append(m.group(1).strip('\'"'))
    return out


def collect():
    """[{slug, lang, path, date, url, alt, links[], images[]}] 를 만든다."""
    out = []
    for lang, d in (('ko', '_posts'), ('en', '_en_posts')):
        for p in sorted(glob.glob(os.path.join(ROOT, d, '*.md'))):
            fm, body = split_fm(read(p))
            slug = os.path.basename(p)[:-3][11:]
            url = ('/ko/posts/' + slug + '/') if lang == 'ko' else ('/posts/' + slug + '/')
            out.append(dict(
                slug=slug, lang=lang, base=os.path.basename(p),
                date=parse_date(fm_get(fm, 'date')),
                url=url,
                permalink=fm_get(fm, 'permalink'),
                alt=fm_get(fm, 'alt_url'),
                hidden=(fm_get(fm, 'hidden') or '').strip() == 'true',
                cats=fm_get(fm, 'categories') or '',
                links=[m.group(1).split('#')[0]
                       for m in re.finditer(r'\]\((/[^)\s]*)\)', body)],
                images=collect_images(fm, body),
            ))
    return out


def check_app_posts(docs, now):
    """앱 소개 글(categories 첫 값 Products)이 /apps/ 와 이어지는지 본다(2026-10-06). 경고 목록을 돌려준다.

    Products 는 hub_only_categories 라 홈·아카이브·RSS 에서 빠지고 /apps/ 링크로만 들어간다.
    /apps/ 는 _plugins/apps-registry.rb 가 **슬러그 = apps.csv 의 앱 id**(다르면 APP_POST_SLUG)인 글만 잇는다.
    그래서 슬러그가 어긋나면 그 글은 어디서도 링크되지 않는다 — 실사례 hangul-monsters-toss(본편의 토스판 소식).
    빌드는 멀쩡하므로 실패가 아니라 경고로 둔다. ko/en 의 최상위 카테고리가 다르면 한쪽 홈에만 섞이므로 같이 본다."""
    rows = list(csv.DictReader(io.open(os.path.join(ROOT, 'apps.csv'), encoding='utf-8-sig')))
    live = dict((r['id'], r.get('play', '').strip() == '1' or r.get('toss', '').strip() == '1') for r in rows)
    reg = read(os.path.join(ROOT, '_plugins', 'apps-registry.rb'))
    block = re.search(r'APP_POST_SLUG\s*=\s*\{(.*?)\}', reg, re.S)
    alias = dict(re.findall(r"'([\w-]+)'\s*=>\s*'([\w-]+)'", block.group(1))) if block else {}
    slug_to_id = dict((s, i) for i, s in alias.items())
    en_top = dict((d['slug'], top_category(d['cats'])) for d in docs if d['lang'] == 'en')
    warns = []
    for d in docs:
        if d['lang'] != 'ko' or d['hidden'] or top_category(d['cats']) != 'Products':
            continue
        app = slug_to_id.get(d['slug'], d['slug'])
        if app not in live:
            warns.append('%s: 앱 소개 글인데 apps.csv 에 id "%s" 가 없다 -> /apps/ 에서 안 이어져 어디서도 링크되지 않는다'
                         ' (파일 슬러그를 앱 id 로 맞추거나 apps-registry.rb APP_POST_SLUG 에 추가, 아니면 본편에 합치기)'
                         % (d['base'], app))
        elif not live[app] and d['date'] and d['date'] <= now:
            warns.append('%s: 공개됐지만 앱 "%s" 가 아직 어느 스토어에도 라이브가 아니라 /apps/ 에 안 뜬다 (출시되면 자동으로 이어진다)'
                         % (d['base'], app))
        if d['slug'] in en_top and en_top[d['slug']] != 'Products':
            warns.append('%s: 영문판 최상위 카테고리가 %s 다 (Products 여야 영문 홈에서도 빠진다)' % (d['base'], en_top[d['slug']]))
    return warns


def check_images(docs, now):
    """본문과 커버(front matter image.path)가 가리키는 파일이 실제로 있는지 본다.

    htmlproofer 는 **빌드된 사이트**만 본다. 예약 글은 공개 시각 전에는 생성되지
    않으므로, 커버 이미지 경로를 잘못 적어도 올리는 날에는 아무 신호가 없고
    공개되는 날 cron 빌드가 죽는다 — `check_front_matter_types` 가 잡은 2048 태그와
    정확히 같은 모양의 함정이다(올릴 땐 멀쩡, 며칠 뒤 새벽에 실패).

    이미 공개된 글은 지금 빌드가 통과하고 있다는 것이 곧 증거라 참고로만 알린다.
    """
    out = []
    for d in docs:
        for u in d['images']:
            f = os.path.join(ROOT, u.split('?')[0].lstrip('/').replace('/', os.sep))
            if os.path.exists(f):
                continue
            future = d['date'] and d['date'] > now
            msg = '%s(%s): 이미지 없음 %s' % (d['base'], d['lang'], u)
            out.append(msg + (' — %s 공개일에 빌드가 죽는다' % d['date'].strftime('%m-%d %H:%M')
                              if future else ' (이미 공개된 글)'))
    return out


def main():
    now = datetime.datetime.now()
    docs = collect()
    by_url = dict((d['url'], d) for d in docs)
    problems, notes = [], []

    # 1) ko/en date 일치
    ko = dict((d['slug'], d) for d in docs if d['lang'] == 'ko')
    en = dict((d['slug'], d) for d in docs if d['lang'] == 'en')
    for slug, k in sorted(ko.items()):
        e = en.get(slug)
        if not e:
            problems.append('%s: 영문판 없음' % slug)
        elif k['date'] != e['date']:
            problems.append('%s: date 불일치 ko=%s en=%s (한쪽만 먼저 공개된다)'
                            % (slug, k['date'], e['date']))

    # 4) URL 규칙
    for d in docs:
        if d['lang'] == 'en':
            want_p, want_a = '/posts/' + d['slug'] + '/', '/ko/posts/' + d['slug'] + '/'
            if d['permalink'] != want_p:
                problems.append('%s(en): permalink %s (기대 %s)' % (d['base'], d['permalink'], want_p))
            if d['alt'] != want_a:
                problems.append('%s(en): alt_url %s (기대 %s)' % (d['base'], d['alt'], want_a))
        else:
            want_a = '/posts/' + d['slug'] + '/'
            if d['alt'] != want_a:
                problems.append('%s(ko): alt_url %s (기대 %s)' % (d['base'], d['alt'], want_a))

    # 2·3) 링크 시점 검사 — 링크하는 쪽이 먼저 공개되면 그날 htmlproofer 가 죽는다
    for d in docs:
        for u in d['links']:
            t = by_url.get(u)
            if not t:
                continue
            # 위험은 **대상이 아직 미공개**일 때만 생긴다. 둘 다 과거면 페이지가 이미
            # 둘 다 있으므로 순서는 무의미하다(처음엔 이걸 빠뜨려 40건을 오탐했다).
            if not (t['date'] and d['date']) or t['date'] <= now:
                continue
            if d['date'] <= t['date']:
                when = '이미 공개됨' if d['date'] <= now else d['date'].strftime('%m-%d %H:%M') + ' 공개'
                problems.append(
                    '%s(%s, %s) -> %s : 대상이 %s 에 공개된다 — 링크한 글이 먼저/같이 나오면 빌드 실패'
                    % (d['base'], d['lang'], when, u, t['date'].strftime('%m-%d %H:%M')))

    # 5) 홈 페이지네이션 쪽수 (예약분 포함해서 세어야 한다)
    hubs = hub_only_categories()
    n = len([d for d in docs if d['lang'] == 'ko' and not d['hidden'] and top_category(d['cats']) not in hubs])
    import math
    pages = max(1, int(math.ceil(n / float(HOME_PER_PAGE))))
    for base, prefix in (('page', '/page/'), (os.path.join('ko', 'page'), '/ko/page/')):
        for i in range(2, pages + 1):
            f = os.path.join(ROOT, base, str(i), 'index.html')
            if not os.path.exists(f):
                problems.append('홈 스텁 없음: %s%d/ (예약분 공개일에 404 링크 -> 빌드 실패)' % (prefix, i))
    notes.append('홈 피드 글(허브 전용 %s 제외) %d개 -> %d쪽 (양 언어 스텁 확인)' % ('·'.join(hubs), n, pages))

    # 6) 이미지 실재 — 예약 글은 htmlproofer 가 공개일 전까지 못 본다
    problems += check_images(docs, now)

    # 예약 현황
    sched = sorted([d for d in docs if d['date'] and d['date'] > now and d['lang'] == 'ko'],
                   key=lambda d: d['date'])
    notes.append('예약 대기 %d편 (한국어 기준, 영문은 같은 날짜)' % len(sched))

    # 7) 앱 소개 글 ↔ /apps/ 연결 (경고만 — 종료 코드에 영향 없음)
    warns = check_app_posts(docs, now)

    print('=== 예약 게시 점검 ===')
    for x in notes:
        print('  ' + x)
    if sched:
        print()
        print('  공개 예정')
        for d in sched:
            print('    %s  %s' % (d['date'].strftime('%m-%d %H:%M'), d['slug']))
    print()
    if warns:
        print('[경고] 앱 소개 글 연결 %d건 (빌드는 통과 — 고치면 없어진다)' % len(warns))
        for x in warns:
            print('  - ' + x)
        print()
    if problems:
        print('[실패] 문제 %d건' % len(problems))
        for x in problems[:40]:
            print('  - ' + x)
        return 1
    print('[통과] 예약 게시분 이상 없음')
    return 0


if __name__ == '__main__':
    sys.exit(main())
