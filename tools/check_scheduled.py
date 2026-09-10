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

usage: python tools/check_scheduled.py
"""
import io
import os
import re
import sys
import glob
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME_PER_PAGE = 10


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


def collect():
    """[{slug, lang, path, date, url, alt, links[]}] 를 만든다."""
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
            ))
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
    n = len([d for d in docs if d['lang'] == 'ko' and not d['hidden'] and 'Tarot' not in d['cats']])
    import math
    pages = max(1, int(math.ceil(n / float(HOME_PER_PAGE))))
    for base, prefix in (('page', '/page/'), (os.path.join('ko', 'page'), '/ko/page/')):
        for i in range(2, pages + 1):
            f = os.path.join(ROOT, base, str(i), 'index.html')
            if not os.path.exists(f):
                problems.append('홈 스텁 없음: %s%d/ (예약분 공개일에 404 링크 -> 빌드 실패)' % (prefix, i))
    notes.append('홈 피드 비타로 글 %d개 -> %d쪽 (양 언어 스텁 확인)' % (n, pages))

    # 예약 현황
    sched = sorted([d for d in docs if d['date'] and d['date'] > now and d['lang'] == 'ko'],
                   key=lambda d: d['date'])
    notes.append('예약 대기 %d편 (한국어 기준, 영문은 같은 날짜)' % len(sched))

    print('=== 예약 게시 점검 ===')
    for x in notes:
        print('  ' + x)
    if sched:
        print()
        print('  공개 예정')
        for d in sched:
            print('    %s  %s' % (d['date'].strftime('%m-%d %H:%M'), d['slug']))
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
