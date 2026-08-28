# -*- coding: utf-8 -*-
"""영문판이 한국어 원문의 구조를 그대로 지켰는지 대조한다 (읽기만 함).

번역 단계에서 가장 잘 깨지는 것들을 본다.
  - front matter 파싱 / BOM
  - 제목 계층(## / ###) 개수와 깊이 순서
  - 표 개수와 각 표의 행 수
  - 이미지 개수와 **경로 동일성** (경로는 절대 바뀌면 안 된다)
  - 링크 href 집합 동일성 (fixup 전이므로 원문과 같아야 한다)
  - kramdown 속성 블록(`{: ... }`) 개수
  - Liquid include / 태그 동일성
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FM_RE = re.compile(r'^---\n(.*?\n)---\n', re.S)


def split_fm(text):
    m = FM_RE.match(text)
    if not m:
        raise ValueError('front matter 없음')
    return m.group(1), text[m.end():]


def canon_link(u):
    """`i18n.py fixup` 이 재작성한 영문 링크를 한국어 원문 형태로 되돌려 비교한다.

    fixup 전(번역 직후)과 후(정규화 완료) 어느 상태에서도 같은 결과가 나와야
    이 검사를 파이프라인 양쪽에서 쓸 수 있다.
    """
    if u.startswith('/en/posts/'):
        return '/posts/' + u[len('/en/posts/'):]
    if u == '/en/tarot/':
        return '/tarot/'
    if u == '/en/about/':
        return '/about/'
    return u


def canon_liquid(t):
    """fixup 이 바꾼 영문 배너 include 를 한국어 원문 형태로 되돌린다."""
    return t.replace('tarot-app-banner-en.html', 'tarot-app-banner.html')


def profile(body):
    return dict(
        headings=re.findall(r'^(#{2,4})\s', body, re.M),
        tables=[len(t.strip().splitlines())
                for t in re.findall(r'((?:^\|.*\|\s*$\n)+)', body, re.M)],
        images=[canon_link(u) for u in re.findall(r'!\[[^\]]*\]\(([^)\s]+)', body)],
        links=sorted(canon_link(u)
                     for u in re.findall(r'(?<!!)\[[^\]]*\]\(([^)\s]+)', body)),
        kramdown=len(re.findall(r'\{:\s*[^}]*\}', body)),
        liquid=sorted(canon_liquid(t)
                      for t in re.findall(r'\{%\s*(.*?)\s*%\}', body)),
    )


def main():
    ko_dir = os.path.join(ROOT, '_posts')
    en_dir = os.path.join(ROOT, '_en_posts')
    problems = []
    checked = 0

    for enp in sorted(glob.glob(os.path.join(en_dir, '*.md'))):
        base = os.path.basename(enp)
        kop = os.path.join(ko_dir, base)
        if not os.path.exists(kop):
            problems.append('%s: 한국어 원문 없음' % base)
            continue

        raw_en = io.open(enp, 'rb').read()
        if raw_en.startswith(b'\xef\xbb\xbf'):
            problems.append('%s: BOM 있음 (front matter 가 죽는다)' % base)
        try:
            kfm, kb = split_fm(io.open(kop, encoding='utf-8').read())
            efm, eb = split_fm(raw_en.decode('utf-8'))
        except ValueError as e:
            problems.append('%s: %s' % (base, e))
            continue
        checked += 1

        k, e = profile(kb), profile(eb)

        if k['headings'] != e['headings']:
            problems.append('%s: 제목 구조 불일치 ko=%s개%s en=%s개%s'
                            % (base, len(k['headings']), k['headings'][:8],
                               len(e['headings']), e['headings'][:8]))
        if k['tables'] != e['tables']:
            problems.append('%s: 표 구조 불일치 ko=%s en=%s' % (base, k['tables'], e['tables']))
        if k['images'] != e['images']:
            only_ko = [x for x in k['images'] if x not in e['images']]
            only_en = [x for x in e['images'] if x not in k['images']]
            problems.append('%s: 이미지 경로 불일치 ko전용=%s en전용=%s' % (base, only_ko, only_en))
        if k['links'] != e['links']:
            only_ko = [x for x in k['links'] if x not in e['links']]
            only_en = [x for x in e['links'] if x not in k['links']]
            problems.append('%s: 링크 불일치 (fixup 전이라 같아야 함) ko전용=%s en전용=%s'
                            % (base, only_ko, only_en))
        if k['kramdown'] != e['kramdown']:
            problems.append('%s: kramdown 속성 블록 개수 ko=%d en=%d'
                            % (base, k['kramdown'], e['kramdown']))
        if k['liquid'] != e['liquid']:
            problems.append('%s: Liquid 태그 불일치 ko=%s en=%s' % (base, k['liquid'], e['liquid']))

        for key in ('title', 'description'):
            m = re.search(r'^' + key + r':[ \t]*(.*)$', efm, re.M)
            if not m or not m.group(1).strip():
                problems.append('%s: %s 누락' % (base, key))
        if re.search(r'[가-힣]', re.sub(r'^\s+alt:.*$', '', efm, flags=re.M)):
            problems.append('%s: front matter 에 한글 잔존' % base)

    print('대조 %d개' % checked)
    if problems:
        print('')
        print('[문제] %d건' % len(problems))
        for p in problems:
            print('  -', p)
        return 1
    print('')
    print('[통과] 구조 동일')
    return 0


if __name__ == '__main__':
    sys.exit(main())
