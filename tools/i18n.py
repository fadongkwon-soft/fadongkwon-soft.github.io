# -*- coding: utf-8 -*-
"""한/영 이중 언어 구조 관리.

설계 요약
  - 한국어 원문은 `_posts/` 에 그대로 두고 URL(/posts/<slug>/)을 바꾸지 않는다.
  - 영문판은 컬렉션 `_en_posts/` 에 두고 /en/posts/<slug>/ 로 낸다.
  - 두 문서는 서로의 경로를 front matter `alt_url` 로 들고, metadata-hook 이
    그걸로 hreflang(ko/en/x-default)을 만든다. Liquid 로 짝을 탐색하면
    문서 수의 제곱만큼 반복이 생겨서 생성 시점에 박아 넣는다.
  - 영문 date 는 한국어와 동일하게 맞춘다. 그래야 예약 게시(미래 날짜 + 매일 cron)
    에서 두 언어가 같은 날 함께 공개되고 hreflang 짝이 항상 성립한다.

명령
  scaffold : 한국어 문서에 alt_url 주입 (idempotent)
  fixup    : _en_posts/*.md 의 기계적 항목을 한국어 원문 기준으로 강제 + 링크 재작성
  verify   : 내부 링크 / hreflang 짝 / front matter 검증
"""
import io
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KO_DIR = os.path.join(ROOT, '_posts')
EN_DIR = os.path.join(ROOT, '_en_posts')

FM_RE = re.compile(r'^---\n(.*?\n)---\n', re.S)

# 번역본에서 한국어판을 가리키는 링크는 영문판으로 돌린다.
# /toss/* 는 토스 딥링크 랜딩(언어 중립)이므로 건드리지 않는다.
LINK_MAP = [
    (re.compile(r'\(/posts/([a-z0-9-]+)/'), r'(/en/posts/\1/'),
    (re.compile(r'\(/tarot/'), r'(/en/tarot/'),
    (re.compile(r'\(/about/'), r'(/en/about/'),
]
INCLUDE_MAP = [('tarot-app-banner.html', 'tarot-app-banner-en.html')]

# 앵커 텍스트 통일. 78장이 같은 허브를 가리키는데 배치마다 표기가 갈렸다
# (`Tarot card meanings - all 78 cards` / 대문자형 / `78 tarot card meanings dictionary` 등).
# 같은 대상에 같은 앵커 텍스트를 쓰는 편이 검색엔진에도 독자에게도 낫다.
# href 재작성보다 먼저 돌려야 한다(아래 LINK_MAP 이 /tarot/ 를 /en/tarot/ 로 바꾸므로).
ANCHOR_MAP = [
    (re.compile(r'\[[^\]]*\]\(/tarot/\)'), '[Tarot Card Meanings — All 78 Cards](/tarot/)'),
]

REQUIRED_EN_KEYS = ('title', 'description', 'date', 'categories', 'permalink', 'alt_url')

# ─────────────────────────────────────────────────────────────────────────────
# 제목 정규화
#
# 한국어 타로 78장은 여러 세션에 걸쳐 쓰이면서 섹션 제목이 심하게 드리프트했다
# (같은 뜻의 섹션이 `상징 읽기` / `그림을 자세히 보면` / `그림 속 디테일` 등 80종 이상).
# 번역을 배치로 돌리면 배치마다 다른 영어 제목을 골라, 78장 사전 안에서 제목이 튄다.
# 실제로 `Reading the symbols` 가 `상징 읽기` 가 아닌 섹션에도 쓰여 예약어가 겹쳤다.
#
# structcheck 가 제목 개수·계층이 원문과 1:1 임을 보장하므로, **N번째 한국어 제목과
# N번째 영어 제목을 짝지어** 아래 표에 있는 것만 표준 영어로 강제한다.
# 표에 없는 카드별 고유 제목(예: `죽음 카드가 나쁜 카드가 아닌 이유`)은 손대지 않는다.
# 영어 부제(` — ` 뒤)는 그대로 살린다.
HEADING_MAP = {
    '카드 기본 정보': 'Card at a glance',
    '카드 한눈에 보기': 'Card at a glance',
    '한눈에 보기': 'Card at a glance',
    '왕의 기본 정보': 'Card at a glance',
    '시종의 기본 정보': 'Card at a glance',
    '상징 읽기': 'Reading the symbols',
    '그림을 자세히 보면': 'A closer look at the picture',
    '그림 속 디테일': 'A closer look at the picture',
    '그림 속 상징': 'A closer look at the picture',
    '상징과 숫자': 'Symbols and the number',
    '숫자와 상징으로 읽기': 'Symbols and the number',
    '수트와 숫자로 읽기': 'Reading it by suit and number',
    '왜 이런 의미가 되었나': 'Where the meaning comes from',
    '정방향 vs 역방향 한눈에': 'Upright vs reversed at a glance',
    '상황별 해석': 'Readings by situation',
    '오늘 이 카드를 뽑았다면': 'If you drew this card today',
    '함께 보면 좋은 카드': 'Cards to read alongside',
    '자주 묻는 질문': 'Frequently asked questions',
    '이 카드가 건네는 한 가지 조언': 'The one piece of advice this card offers',
    '함께 나오면 의미가 달라지는 조합': 'Combinations that change the reading',
    '함께 나온 카드로 더 정확히 읽기': 'Combinations that change the reading',
    '다른 카드와 겹칠 때 달라지는 뜻': 'Combinations that change the reading',
}

# 정/역 계열은 부제 유무로 문구가 갈린다.
#   부제 없음 -> `Upright meaning`  (단독 제목은 meaning 이 붙는 편이 읽기 좋다)
#   부제 있음 -> `Upright — <부제>` (meaning 을 끼우면 늘어진다)
UPRIGHT_KO = ('정방향', '정방향 의미', '정방향 설명', '정방향으로 나왔다면')
REVERSED_KO = ('역방향', '역방향 의미', '역방향 설명', '역방향으로 나왔다면')

# 상황별 해석의 소제목. 이모지는 원문 것을 그대로 두고 라벨만 통일한다.
SITUATION_MAP = {
    '연애': 'Love',
    '결혼': 'Marriage',
    '직장·커리어': 'Career',
    '직장·사업': 'Career & Business',
    '사업': 'Business',
    '금전': 'Money',
    '금전·투자': 'Money & Investing',
    '투자': 'Investing',
    '학업·시험': 'Study & Exams',
    '건강': 'Health',
    '건강·습관': 'Health & Habits',
    '대인관계': 'Relationships',
    '가족': 'Family',
    '부동산·주거': 'Property & Housing',
    '오늘의 운세': "Today's fortune",
}

# 표 1열 라벨. 한국어 원문도 같은 뜻을 `수트·숫자` / `수트 · 숫자` / `수트/숫자` /
# `수트·번호` 처럼 여러 표기로 쓴다. 제목과 같은 방식으로 원문 기준 위치 매핑한다.
# 표에 없는 카드별 고유 라벨(예: `등불의 쓰임`)은 손대지 않는다.
ROW_LABEL_MAP = {
    '구분': 'Field',
    '정방향': 'Upright',
    '역방향': 'Reversed',
    '정방향 키워드': 'Upright keywords',
    '역방향 키워드': 'Reversed keywords',
    '영문명': 'English name',
    '번호': 'Number',
    '숫자': 'Number',
    '수트': 'Suit',
    '수트·숫자': 'Suit & number',
    '수트 · 숫자': 'Suit & number',
    '수트/숫자': 'Suit & number',
    '수트·번호': 'Suit & number',
    '수트·코트': 'Suit & rank',
    '수트/코트': 'Suit & rank',
    '코트 위계': 'Court rank',
    '코트 위치': 'Court rank',
    '서열': 'Court rank',
    '원소': 'Element',
    '원소·영역': 'Element & domain',
    '수트 · 원소': 'Suit & element',
    '핵심': 'Core',
    '핵심 의미': 'Core meaning',
    '핵심 키워드': 'Core keywords',
    '핵심 조언': 'Key advice',
    '필요한 태도': 'What is needed',
    '조언': 'Advice',
    '태도': 'Attitude',
    '마음 상태': 'State of mind',
    '감정 상태': 'Emotional state',
    '상징하는 단계': 'Stage it stands for',
}

HEADING_RE = re.compile(r'^(#{2,4}) (.+)$', re.M)
EMOJI_PREFIX_RE = re.compile(r'^([^\w가-힣]+)\s*(.*)$')


def _split_subtitle(text):
    """제목을 (본체, 부제포함꼬리) 로 나눈다. 부제 구분자는 em dash."""
    if ' — ' in text:
        i = text.index(' — ')
        return text[:i], text[i:]
    return text, ''


def canonical_heading(ko_text, en_text):
    """한국어 제목을 근거로 영어 제목을 표준화. 바꿀 필요가 없으면 en_text 그대로."""
    ko_base, _ = _split_subtitle(ko_text.strip())
    en_base, en_tail = _split_subtitle(en_text.strip())

    # 이모지 접두어는 원문 것을 유지하고 라벨만 본다
    ko_m = EMOJI_PREFIX_RE.match(ko_base)
    ko_emoji, ko_label = (ko_m.group(1), ko_m.group(2)) if ko_m else ('', ko_base)
    en_m = EMOJI_PREFIX_RE.match(en_base)
    en_emoji = en_m.group(1) if en_m else ''

    if ko_label in SITUATION_MAP:
        emoji = en_emoji or ko_emoji
        prefix = (emoji.strip() + ' ') if emoji.strip() else ''
        return prefix + SITUATION_MAP[ko_label] + en_tail

    if ko_base in UPRIGHT_KO:
        return ('Upright' + en_tail) if en_tail else 'Upright meaning'
    if ko_base in REVERSED_KO:
        return ('Reversed' + en_tail) if en_tail else 'Reversed meaning'
    if ko_base in HEADING_MAP:
        return HEADING_MAP[ko_base] + en_tail
    return en_text.strip()


def normalize_headings(ko_body, en_body):
    """N번째 한국어 제목과 N번째 영어 제목을 짝지어 표준 문구를 강제한다.

    개수·계층이 다르면(structcheck 가 잡아야 하는 상황) 아무것도 하지 않는다.
    """
    ko_h = HEADING_RE.findall(ko_body)
    en_h = HEADING_RE.findall(en_body)
    if len(ko_h) != len(en_h):
        return en_body, 0
    if [h[0] for h in ko_h] != [h[0] for h in en_h]:
        return en_body, 0

    idx = [0]
    n = [0]

    def repl(m):
        i = idx[0]
        idx[0] += 1
        lvl, txt = m.group(1), m.group(2)
        new = canonical_heading(ko_h[i][1], txt)
        if new != txt.strip():
            n[0] += 1
        return lvl + ' ' + new

    return HEADING_RE.sub(repl, en_body), n[0]


def _is_table_row(line):
    return line.lstrip().startswith('|') and line.count('|') >= 2


def _is_separator(line):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return bool(cells) and all(c and set(c) <= set('-: ') for c in cells)


def normalize_row_labels(ko_body, en_body):
    """N번째 한국어 표 행과 N번째 영어 표 행을 짝지어 1열 라벨을 표준화한다.

    구분선 행은 양쪽에서 동일하게 제외한다. 행 수가 다르면(structcheck 가 잡아야 하는
    상황) 아무것도 하지 않는다 — 어긋난 상태로 매핑하면 라벨이 뒤섞인다.
    """
    ko_lines = ko_body.splitlines()
    en_lines = en_body.splitlines()
    ko_rows = [l for l in ko_lines if _is_table_row(l) and not _is_separator(l)]
    en_idx = [i for i, l in enumerate(en_lines)
              if _is_table_row(l) and not _is_separator(l)]
    if len(ko_rows) != len(en_idx):
        return en_body, 0

    n = 0
    for k, i in zip(ko_rows, en_idx):
        ko_label = k.strip().strip('|').split('|')[0].strip()
        want = ROW_LABEL_MAP.get(ko_label)
        if not want:
            continue
        line = en_lines[i]
        lead = line[:len(line) - len(line.lstrip())]
        cells = line.strip().strip('|').split('|')
        if cells[0].strip() == want:
            continue
        cells[0] = ' ' + want + ' '
        en_lines[i] = lead + '|' + '|'.join(cells) + '|'
        n += 1
    if not n:
        return en_body, 0
    tail = '\n' if en_body.endswith('\n') else ''
    return '\n'.join(en_lines) + tail, n


def split_fm(text):
    m = FM_RE.match(text)
    if not m:
        raise ValueError('front matter 없음')
    return m.group(1), text[m.end():]


def fm_get(fm, key):
    m = re.search(r'^' + re.escape(key) + r':[ \t]*(.*)$', fm, re.M)
    return m.group(1).strip() if m else None


def fm_set(fm, key, value):
    """최상위 키를 설정. 중첩 블록(image: 등)을 깨지 않도록 컬럼 0 만 본다."""
    line = key + ': ' + str(value)
    pat = re.compile(r'^' + re.escape(key) + r':[ \t]*.*$', re.M)
    if pat.search(fm):
        return pat.sub(lambda _m: line, fm, count=1)
    return fm.rstrip('\n') + '\n' + line + '\n'


def fm_block(fm, key):
    """`image:` 처럼 하위 들여쓰기를 갖는 블록을 통째로 뽑는다."""
    m = re.search(r'^(' + re.escape(key) + r':[ \t]*\n(?:[ \t]+.*\n)*)', fm, re.M)
    if m:
        return m.group(1)
    v = fm_get(fm, key)
    if v:
        return key + ': ' + v + '\n'
    return None


def ko_posts():
    out = []
    for p in sorted(glob.glob(os.path.join(KO_DIR, '*.md'))):
        base = os.path.basename(p)[:-3]
        out.append(dict(path=p, base=base, slug=base[11:]))
    return out


def en_files():
    return sorted(glob.glob(os.path.join(EN_DIR, '*.md')))


def card_name(ko_title):
    """한국어 타로 제목에서 영문 카드명 추출. 타로 카드 글이 아니면 None.

    '바보(The Fool) 카드 의미 - ...' -> 'The Fool'

    ⚠️ 괄호만 보고 뽑으면 안 된다. `Saju Lotto (사주로또)` 처럼 제목에 괄호가 있는
    일반 글에서 한글이 card_name 으로 들어갔다(2026-08-29 실제로 밟음).
    78장 카드 제목은 모두 `카드 의미` 를 포함하므로 그것을 게이트로 쓴다.
    """
    t = ko_title or ''
    if '카드 의미' not in t:
        return None
    m = re.search(r'\(([^)]+)\)', t)
    return m.group(1).strip() if m else None


def cmd_scaffold():
    posts = ko_posts()
    n = 0
    for r in posts:
        s = io.open(r['path'], encoding='utf-8').read()
        fm, body = split_fm(s)
        want = '/en/posts/' + r['slug'] + '/'
        if fm_get(fm, 'alt_url') == want:
            continue
        fm = fm_set(fm, 'alt_url', want)
        io.open(r['path'], 'w', encoding='utf-8', newline='\n').write('---\n' + fm + '---\n' + body)
        n += 1
    print('한국어 포스트 alt_url: %d개 변경 / 전체 %d개' % (n, len(posts)))

    for path, alt in [('index.html', '/en/'),
                      ('_tabs/tarot.md', '/en/tarot/'),
                      ('_tabs/about.md', '/en/about/')]:
        p = os.path.join(ROOT, path)
        s = io.open(p, encoding='utf-8').read()
        fm, body = split_fm(s)
        if fm_get(fm, 'alt_url') != alt:
            fm = fm_set(fm, 'alt_url', alt)
            io.open(p, 'w', encoding='utf-8', newline='\n').write('---\n' + fm + '---\n' + body)
            print('  alt_url 주입: %s -> %s' % (path, alt))


def cmd_fixup():
    ko = dict((r['slug'], r) for r in ko_posts())
    files = en_files()
    if not files:
        print('_en_posts 가 비어 있음')
        return []
    bad = []
    head_fixed = []
    row_fixed = []
    for p in files:
        base = os.path.basename(p)[:-3]
        slug = base[11:]
        if slug not in ko:
            bad.append(base + ': 대응하는 한국어 원문이 없음')
            continue
        kfm, kbody = split_fm(io.open(ko[slug]['path'], encoding='utf-8').read())
        try:
            fm, body = split_fm(io.open(p, encoding='utf-8').read())
        except ValueError as e:
            bad.append(base + ': ' + str(e))
            continue

        # 기계적 항목은 한국어 원문 기준으로 덮어쓴다 (번역 단계 실수를 차단)
        fm = fm_set(fm, 'date', fm_get(kfm, 'date'))
        fm = fm_set(fm, 'categories', fm_get(kfm, 'categories'))
        fm = fm_set(fm, 'permalink', '/en/posts/' + slug + '/')
        fm = fm_set(fm, 'alt_url', '/posts/' + slug + '/')
        # 태그는 영문 아카이브 페이지가 없어 링크가 404 나므로 넣지 않는다
        fm = re.sub(r'^tags:[ \t]*.*$\n?', '', fm, flags=re.M)
        # 대표 이미지가 없으면 한국어와 같은 파일을 쓴다
        if 'image:' not in fm:
            blk = fm_block(kfm, 'image')
            if blk:
                fm = fm.rstrip('\n') + '\n' + blk
        cn = card_name(fm_get(kfm, 'title'))
        if cn:
            fm = fm_set(fm, 'card_name', cn)
        else:
            # 타로 카드가 아니면 이전 실행이 잘못 넣었을 수 있는 값을 지운다
            fm = re.sub(r'^card_name:[ \t]*.*$\n?', '', fm, flags=re.M)

        for rx, rep in ANCHOR_MAP:
            body = rx.sub(lambda _m, r=rep: r, body)
        for rx, rep in LINK_MAP:
            body = rx.sub(rep, body)
        for a, b in INCLUDE_MAP:
            body = body.replace('include ' + a, 'include ' + b)

        # 제목·표라벨 표준화는 **타로 카드 글에만** 적용한다. 두 매핑은 타로 78장
        # 코퍼스에서 뽑은 것이라 다른 글에 쓰면 오역이 된다.
        # 실제로 밟음(2026-08-29): `구분` 을 타로 표에서는 `Field` 로 쓰지만,
        # 간호조무사 글에서는 교육 구분(Category)과 상·하반기(Session)를 뜻해서
        # 두 표의 헤더가 엉뚱하게 `Field` 로 바뀌었다.
        if cn:
            body, nh = normalize_headings(kbody, body)
            if nh:
                head_fixed.append('%s (%d개 제목)' % (base, nh))
            body, nr = normalize_row_labels(kbody, body)
            if nr:
                row_fixed.append('%s (%d개 라벨)' % (base, nr))

        io.open(p, 'w', encoding='utf-8', newline='\n').write('---\n' + fm + '---\n' + body)

    print('fixup: %d개 처리' % len(files))
    if head_fixed:
        print('  제목 표준화 %d개 파일:' % len(head_fixed))
        for h in head_fixed:
            print('    -', h)
    if row_fixed:
        print('  표 라벨 표준화 %d개 파일:' % len(row_fixed))
        for h in row_fixed:
            print('    -', h)
    for b in bad:
        print('  [경고]', b)
    return bad


def known_urls(ko, files):
    urls = set(['/', '/en/', '/tarot/', '/en/tarot/', '/about/', '/en/about/',
                '/privacy/', '/archives/', '/categories/', '/tags/'])
    for slug in ko:
        urls.add('/posts/' + slug + '/')
    for p in files:
        urls.add('/en/posts/' + os.path.basename(p)[:-3][11:] + '/')
    for p in glob.glob(os.path.join(ROOT, 'toss', '*.html')):
        urls.add('/toss/' + os.path.basename(p)[:-5] + '/')
    return urls


def cmd_verify():
    problems = []
    warnings = []
    ko = dict((r['slug'], r) for r in ko_posts())
    files = en_files()
    urls = known_urls(ko, files)

    def check_links(body, label):
        for m in re.finditer(r'\]\((/[^)\s]*)\)', body):
            u = m.group(1).split('#')[0]
            if u.startswith('/assets/'):
                continue
            if u and u not in urls:
                problems.append(label + ': 깨진 내부 링크 ' + u)

    for r in ko_posts():
        fm, body = split_fm(io.open(r['path'], encoding='utf-8').read())
        if fm_get(fm, 'alt_url') != '/en/posts/' + r['slug'] + '/':
            problems.append(r['base'] + ': alt_url 누락/불일치')
        check_links(body, r['base'])

    for p in files:
        base = os.path.basename(p)[:-3]
        slug = base[11:]
        fm, body = split_fm(io.open(p, encoding='utf-8').read())
        for k in REQUIRED_EN_KEYS:
            if not fm_get(fm, k):
                problems.append(base + '(en): ' + k + ' 누락')
        if fm_get(fm, 'alt_url') != '/posts/' + slug + '/':
            problems.append(base + '(en): alt_url 불일치')
        if slug in ko:
            kfm, _ = split_fm(io.open(ko[slug]['path'], encoding='utf-8').read())
            if fm_get(fm, 'date') != fm_get(kfm, 'date'):
                problems.append(base + '(en): date 가 한국어판과 다름 (예약 공개가 어긋난다)')
        stripped = re.sub(r'^card_name:.*$', '', fm, flags=re.M)
        if re.search(r'[가-힣]', stripped):
            problems.append(base + '(en): front matter 에 한글 잔존')
        # 본문 한글은 하드 실패로 두지 않는다. 한글 학습·자격시험·사주 글은 한국어
        # 낱말 자체가 소재라 정상적으로 등장한다(로마자 병기 형태). 타로 카드처럼
        # 한글이 나올 이유가 없는 글만 걸러내도록 개수만 보고한다.
        hangul = re.findall(r'[가-힣]+', body)
        if hangul:
            warnings.append('%s(en): 본문 한글 %d개 - %s'
                            % (base, len(hangul), ' '.join(hangul[:6])))
        if 'tarot-app-banner.html' in body:
            problems.append(base + '(en): 한국어 배너 include 가 남아 있음')
        check_links(body, base + '(en)')

    missing = sorted(set(ko) - set(os.path.basename(p)[:-3][11:] for p in files))
    print('한국어 %d개 / 영문 %d개' % (len(ko), len(files)))
    if missing:
        head = ', '.join(missing[:8]) + (' ...' if len(missing) > 8 else '')
        print('영문판 미작성 %d개: %s' % (len(missing), head))
    if warnings:
        print('')
        print('[참고] 확인 권장 %d건' % len(warnings))
        for x in warnings[:30]:
            print('  ~', x)
    if problems:
        print('')
        print('[실패] 문제 %d건' % len(problems))
        for x in problems[:60]:
            print('  -', x)
    else:
        print('')
        print('[통과] 검증 이상 없음')
    return problems


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
    os.makedirs(EN_DIR, exist_ok=True)
    {'scaffold': cmd_scaffold, 'fixup': cmd_fixup, 'verify': cmd_verify}[cmd]()
