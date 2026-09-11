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
    # URL 규칙(2026-09-11): 영어 = /*, 한국어 = /ko/*  (근거: tools/urlscheme.py)
    # 비교 기준은 **한국어 원문 형태**(/ko/*)로 맞춘다.
    if u.startswith('/posts/'):
        return '/ko/posts/' + u[len('/posts/'):]
    if u == '/tarot/':
        return '/ko/tarot/'
    if u == '/about/':
        return '/ko/about/'
    if u == '/privacy/':
        return '/ko/privacy/'
    if u == '/play/':
        return '/ko/play/'
    if u == '/apps/':
        return '/ko/apps/'
    return u


def check_front_matter_yaml():
    """front matter 가 YAML 로 파싱되는지 확인한다.

    문법 오류가 나면 Jekyll 은 **빌드를 실패시키지 않고** 경고만 남기고 그 문서의
    data 를 비운다. 결과가 조용해서 알아채기 어렵다 — 제목·permalink 가 사라져
    기본 컬렉션 URL(/en_posts/....html)로 나가고, date 가 없으니 예약 글이
    즉시 공개된다. 2026-09-10 실제로 description 안의 ': '(콜론+공백) 때문에
    영문 글 한 편이 이렇게 나갔다.

    가장 흔한 원인은 인용부호 없는 값 안의 ': ' 이다. 그런 값은 큰따옴표로 감싼다.
    """
    try:
        import yaml
    except ImportError:
        return ['(PyYAML 이 없어 front matter YAML 검사를 건너뜀 — pip install pyyaml)']

    out = []
    for d in ('_posts', '_en_posts'):
        for p in sorted(glob.glob(os.path.join(ROOT, d, '*.md'))):
            s = io.open(p, encoding='utf-8').read()
            m = FM_RE.match(s)
            if not m:
                out.append('%s/%s: front matter 없음' % (d, os.path.basename(p)))
                continue
            try:
                yaml.safe_load(m.group(1))
            except Exception as e:
                out.append('%s/%s: front matter YAML 오류 — %s'
                           % (d, os.path.basename(p), str(e).replace('\n', ' ')[:150]))
    return out


def tag_slug(t):
    """Jekyll slugify(기본 모드)와 같게: 소문자 + 영숫자 아닌 구간을 하이픈으로."""
    return re.sub(r'[^a-z0-9]+', '-', t.strip().lower()).strip('-')


def check_front_matter_types():
    """tags/categories 항목과 app_name 이 **문자열로** 파싱되어야 한다.

    YAML 은 따옴표 없는 `2048` 을 정수로 읽는다. Jekyll 의 slugify 는 문자열만 받으므로
    그런 태그를 가진 글이 **공개되는 순간** 빌드가 통째로 죽는다
    (undefined method `gsub' for an instance of Integer).
    예약 글이면 공개 시각이 지난 뒤의 빌드부터 죽기 때문에, 올릴 때는 멀쩡하고
    며칠 뒤 새벽 cron 이 죽는 형태로 나타난다 — 사람이 잡을 수 없다.
    2026-09-11 실제로 이걸로 그날 예약분이 배포되지 못했다.

    처방: 숫자로만 된 값은 따옴표로 감쌀 것. tags: [..., '2048', ...]
    """
    try:
        import yaml
    except ImportError:
        return []

    out = []
    targets = []
    for d in ('_posts', '_en_posts', '_tabs'):
        targets += sorted(glob.glob(os.path.join(ROOT, d, '*.md')))
    for d in ('toss', 'play-store'):
        targets += sorted(glob.glob(os.path.join(ROOT, d, '*.html')))

    for p in targets:
        s = io.open(p, encoding='utf-8').read().replace(chr(13) + chr(10), chr(10))
        if not s.startswith('---' + chr(10)):
            continue
        try:
            fm, _ = split_fm(s)
            data = yaml.safe_load(fm) or {}
        except Exception:
            continue  # YAML 파싱 자체는 check_front_matter_yaml 이 본다
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        for key in ('tags', 'categories'):
            for v in (data.get(key) or []):
                if not isinstance(v, str):
                    out.append("%s: %s 의 %r 가 %s 로 파싱된다 — 따옴표로 감쌀 것"
                               % (rel, key, v, type(v).__name__))
        for key in ('app_name', 'title'):
            v = data.get(key)
            if v is not None and not isinstance(v, str):
                out.append("%s: %s 의 %r 가 %s 로 파싱된다 — 따옴표로 감쌀 것"
                           % (rel, key, v, type(v).__name__))
    return out


def check_page_layouts():
    """permalink 을 가진 페이지에 layout 선언이 있어야 한다.

    layout 을 아예 빼면 Jekyll 이 파일을 그대로 내보낸다 — head(CSS)도 사이드바도 없다.
    HTTP 200 이고 링크도 정상이라 htmlproofer 가 통과하므로 아무도 못 잡는다.
    2026-09-11 /apps/ · /ko/apps/ 가 그렇게 나가서 접근성용 숨김 텍스트가 본문에 보였다.

    `layout: none`(토스 랜딩)이나 `layout: null`(sitemap·리다이렉트 스텁)은 **명시한 선택**
    이므로 통과시킨다 — 문제는 키가 아예 없는 경우다.

    ⚠️ 컬렉션(_posts·_en_posts·_tabs)은 제외한다. _config.yml 의 defaults 가 layout 을
       주기 때문에 파일에서 생략하는 것이 정상이다(이걸 빼먹어 6건이 오탐으로 잡혔다).
       독립 페이지(루트·하위 디렉터리)만 검사한다.
    """
    out = []
    skip_dirs = {'.git', '_site', 'node_modules', 'assets',
                 '_posts', '_en_posts', '_tabs',
                 '.jekyll-cache', 'vendor', '.preview-tmp'}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in files:
            if os.path.splitext(fn)[1].lower() not in ('.md', '.html'):
                continue
            p = os.path.join(root, fn)
            try:
                s = io.open(p, encoding='utf-8').read().replace(chr(13) + chr(10), chr(10))
            except Exception:
                continue
            if not s.startswith('---' + chr(10)):
                continue
            try:
                fm, _ = split_fm(s)
            except ValueError:
                continue
            if not re.search(r'^permalink:', fm, re.M):
                continue
            if not re.search(r'^layout:', fm, re.M):
                rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
                out.append('%s: layout 선언 없음 (사이트 껍데기 없이 배포된다)' % rel)
    return out


def check_lang_declared():
    """영어판 페이지는 front matter 에 `lang: en` 을 반드시 선언해야 한다.

    URL 규칙(2026-09-11)상 영어가 루트(/*), 한국어가 /ko/* 다. 그래서 **주소만 보고는**
    영어판인지 알 수 없다 — 언어를 아는 방법은 lang 선언뿐이다.
    _plugins/external-links.rb 가 이 값으로 랜딩 링크에 ?lang= 을 실어 보내므로,
    선언이 빠지면 영어 페이지에서 누른 설치 링크가 한국어 랜딩으로 간다
    (사용자 제보 2026-09-11). 눈에 보이는 오류가 없어 htmlproofer 도 못 잡는다.

    판정: /ko/ 로 시작하지 않는 permalink 를 가졌고, 같은 이름의 한국어 짝이 있는 페이지.
    (짝이 없는 언어 중립 페이지 — 랜딩·sitemap·리다이렉트 스텁 — 는 대상이 아니다)
    """
    out = []
    pages = {}
    skip_dirs = {'.git', '_site', 'node_modules', 'assets', '_posts', '_en_posts',
                 '.jekyll-cache', 'vendor', '.preview-tmp', 'toss', 'play-store'}
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for fn in files:
            if os.path.splitext(fn)[1].lower() not in ('.md', '.html'):
                continue
            p = os.path.join(root, fn)
            try:
                s = io.open(p, encoding='utf-8').read().replace(chr(13) + chr(10), chr(10))
            except Exception:
                continue
            if not s.startswith('---' + chr(10)):
                continue
            try:
                fm, _ = split_fm(s)
            except ValueError:
                continue
            m = re.search(r'^permalink:[ 	]*(\S+)', fm, re.M)
            if not m:
                continue
            url = m.group(1).strip('\'"')
            pages[url] = (os.path.relpath(p, ROOT).replace(os.sep, '/'),
                          bool(re.search(r'^lang:[ 	]*en', fm, re.M)))

    for url, (rel, has_lang) in sorted(pages.items()):
        if url.startswith('/ko/') or has_lang:
            continue
        if ('/ko' + url) not in pages:
            continue  # 한국어 짝이 없다 = 언어 중립 페이지
        out.append('%s: lang: en 선언 없음 (영어 페이지가 한국어로 취급돼 '
                   '설치 링크가 한국어 랜딩으로 간다)' % rel)
    return out


def check_tab_titles():
    """_tabs/*.md 는 모두 명시 title 을 가져야 한다.

    없으면 Chirpy 가 **파일명에서 제목을 유도**한다. 파일명 규칙(2026-09-11)에 따라
    한국어 파일이 `ko-` 접두를 갖게 되면서 h1 이 "Ko About" 처럼 나갔다.
    HTTP 200 이고 링크도 정상이라 htmlproofer 는 통과한다 — 조용한 사고다.
    """
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, '_tabs', '*.md'))):
        s = io.open(p, encoding='utf-8').read()
        try:
            fm, _ = split_fm(s.replace(chr(13) + chr(10), chr(10)))
        except ValueError as e:
            out.append('%s: %s' % (os.path.basename(p), e))
            continue
        if not re.search(r'^title:[ \t]*\S', fm, re.M):
            out.append('%s: title 없음 (Chirpy 가 파일명에서 제목을 유도한다)'
                       % os.path.basename(p))
    return out


def check_en_tag_pages():
    """영문 포스트의 tags 마다 tags/<slug>/index.md 가 있어야 한다.

    URL 규칙(2026-09-11): 영어 = /*, 한국어 = /ko/*  (근거: tools/urlscheme.py)
    jekyll-archives 는 한국어 포스트(/ko/tags/:name/)만 만들고 영문 태그 페이지는
    수동 파일이다. 새 영문 태그를 쓰면서 페이지를 안 만들면 포스트가 없는 URL 로
    링크해 **htmlproofer(Test site) 가 죽는다** — 실제로 2026-09-09 이걸로 실패했다.
    """
    have = set(os.path.basename(os.path.dirname(p))
               for p in glob.glob(os.path.join(ROOT, 'tags', '*', 'index.md')))
    missing = {}
    for p in sorted(glob.glob(os.path.join(ROOT, '_en_posts', '*.md'))):
        s = io.open(p, encoding='utf-8').read()
        m = re.search(r'^tags:[ \t]*\[(.*?)\][ \t]*$', s[:4000], re.M | re.S)
        if not m:
            continue
        for t in m.group(1).split(','):
            t = t.strip()
            if t and tag_slug(t) not in have:
                missing.setdefault(tag_slug(t), (t, os.path.basename(p)))
    return ['영문 태그 페이지 없음: tags/%s/index.md (태그 "%s", %s)' % (k, v[0], v[1])
            for k, v in sorted(missing.items())]


def check_en_category_pages():
    """영문 포스트의 categories 마다 categories/<slug>/index.md 가 있어야 한다.

    태그(check_en_tag_pages)와 완전히 같은 함정인데 **카테고리는 검사하지 않고 있었다.**
    지금까지 안 터진 건 쓰는 카테고리가 적어서 우연히 다 있었기 때문이다.
    카테고리는 글마다 1~2개뿐이라 새 카테고리를 만드는 일이 드물고, 그래서 오히려
    한 번 빠뜨리면 그 글이 공개되는 날에야 htmlproofer 가 죽는다.
    """
    have = set(os.path.basename(os.path.dirname(p))
               for p in glob.glob(os.path.join(ROOT, 'categories', '*', 'index.md')))
    missing = {}
    for p in sorted(glob.glob(os.path.join(ROOT, '_en_posts', '*.md'))):
        s = io.open(p, encoding='utf-8').read()
        m = re.search(r'^categories:[ 	]*\[(.*?)\][ 	]*$', s[:4000], re.M | re.S)
        if not m:
            continue
        for c in m.group(1).split(','):
            c = c.strip().strip('\'"')
            if c and tag_slug(c) not in have:
                missing.setdefault(tag_slug(c), (c, os.path.basename(p)))
    return ['영문 카테고리 페이지 없음: categories/%s/index.md (카테고리 "%s", %s)'
            % (k, v[0], v[1]) for k, v in sorted(missing.items())]


def canon_liquid(t):
    """fixup 이 바꾼 영문 배너 include 를 한국어 원문 형태로 되돌린다."""
    # 파일명 규칙(2026-09-11): 영어 = 무표식, 한국어 = ko- 표식.
    # 비교 기준은 한국어 원문 형태(-ko)로 맞춘다.
    return t.replace('tarot-app-banner.html', 'tarot-app-banner-ko.html')


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
            # 본문은 텍스트 모드로 다시 읽는다 — 개행이 정규화된다.
            # raw_en(바이트)은 BOM 검사 전용이다. core.autocrlf=true 인 이 저장소는
            # git 이 만진 파일이 CRLF 로 바뀌는데, 바이트를 그대로 디코드하면
            # front matter 정규식이 안 맞아 멀쩡한 글이 "front matter 없음"으로 잡힌다.
            efm, eb = split_fm(io.open(enp, encoding='utf-8').read())
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

        # 예약 게시가 한쪽만 먼저 나가지 않도록 date 가 같아야 한다.
        # (미래 날짜 컬렉션 문서는 Jekyll 이 write 단계에서 걸러 파일을 내보내지 않고,
        #  site.en_posts 를 쓰는 목록은 각자 date <= site.time 으로 거른다)
        kd = re.search(r'^date:[ \t]*(.*)$', kfm, re.M)
        ed = re.search(r'^date:[ \t]*(.*)$', efm, re.M)
        if kd and ed and kd.group(1).strip() != ed.group(1).strip():
            problems.append('%s: date 불일치 ko=%s en=%s (예약 게시가 어긋난다)'
                            % (base, kd.group(1).strip(), ed.group(1).strip()))
        if re.search(r'[가-힣]', re.sub(r'^\s+alt:.*$', '', efm, flags=re.M)):
            problems.append('%s: front matter 에 한글 잔존' % base)

    problems.extend(check_front_matter_yaml())
    problems.extend(check_en_tag_pages())
    problems += check_tab_titles()
    problems += check_page_layouts()
    problems += check_front_matter_types()
    problems += check_lang_declared()
    problems += check_en_category_pages()

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
