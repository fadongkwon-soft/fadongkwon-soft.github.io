# -*- coding: utf-8 -*-
"""Liquid 블록 태그 균형 검사 (로컬에 Ruby 가 없어 jekyll build 로 검증할 수 없다).

빌드를 실패시키는 가장 흔한 실수를 잡는다.
  - if/endif, unless/endunless, for/endfor, case/endcase,
    capture/endcapture, comment/endcomment, raw/endraw, tablerow/endtablerow
  - 짝이 안 맞는 `{%`, `{{`
  - front matter 구분자 누락
  - BOM (front matter 를 죽인다)

검사 대상: 이 저장소가 직접 소유한 Liquid 파일. 테마 gem 의 파일은 건드리지 않는다.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAIRS = {
    'if': 'endif',
    'unless': 'endunless',
    'for': 'endfor',
    'case': 'endcase',
    'capture': 'endcapture',
    'comment': 'endcomment',
    'raw': 'endraw',
    'tablerow': 'endtablerow',
    'form': 'endform',
    'highlight': 'endhighlight',
}
OPENERS = set(PAIRS)
CLOSERS = set(PAIRS.values())
# 블록을 열지 않는 중간/단독 태그
NEUTRAL = {'else', 'elsif', 'when', 'break', 'continue', 'assign', 'include',
           'include_cached', 'include_relative', 'cycle', 'increment',
           'decrement', 'echo', 'liquid', 'render', 'seo', 'link', 'post_url',
           'endcomment_'}

TAG_RE = re.compile(r'\{%-?\s*(\w+)')

TARGETS = [
    '_includes', '_layouts', '_tabs', 'toss', 'en',
    'assets/js/data',
]
ROOT_FILES = ['index.html', 'sitemap.xml', 'robots.txt']


def collect():
    files = []
    for d in TARGETS:
        full = os.path.join(ROOT, d)
        if not os.path.isdir(full):
            continue
        for dirpath, _dirs, names in os.walk(full):
            for n in names:
                if n.endswith(('.html', '.md', '.xml', '.json')):
                    files.append(os.path.join(dirpath, n))
    for n in ROOT_FILES:
        p = os.path.join(ROOT, n)
        if os.path.exists(p):
            files.append(p)
    return sorted(files)


def check(path):
    rel = os.path.relpath(path, ROOT).replace('\\', '/')
    out = []
    raw = io.open(path, 'rb').read()
    if raw.startswith(b'\xef\xbb\xbf'):
        out.append('%s: BOM 있음 (front matter 가 파싱되지 않는다)' % rel)
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as e:
        out.append('%s: UTF-8 아님 - %s' % (rel, e))
        return out

    if text.count('{%') != text.count('%}'):
        out.append('%s: {%% 와 %%} 개수 불일치 (%d / %d)'
                   % (rel, text.count('{%'), text.count('%}')))
    if text.count('{{') != text.count('}}'):
        out.append('%s: {{ 와 }} 개수 불일치 (%d / %d)'
                   % (rel, text.count('{{'), text.count('}}')))

    # front matter 가 있으면 닫혀 있어야 한다
    if text.startswith('---\n'):
        if not re.match(r'^---\n.*?\n---\n', text, re.S):
            out.append('%s: front matter 가 닫히지 않았다' % rel)

    # HTML 주석은 Liquid 를 가리지 못한다. `<!-- {% include x %} -->` 도 그대로 실행된다.
    # 2026-08-29: search-loader.html 주석에 "이렇게 불린다"는 설명으로 자기 자신을
    # include 하는 태그를 적었다가 무한 재귀로 jekyll build 가 죽었다.
    # 주석에 예시를 남기려면 중괄호를 빼거나 {% raw %} 로 감쌀 것.
    for m in re.finditer(r'<!--.*?-->', text, re.S):
        for t in TAG_RE.finditer(m.group(0)):
            line = text.count('\n', 0, m.start() + t.start()) + 1
            out.append('%s:%d: HTML 주석 안의 {%% %s %%} 는 그대로 실행된다 '
                       '(주석은 Liquid 를 가리지 못한다)' % (rel, line, t.group(1)))

    stack = []
    in_raw = False
    for m in TAG_RE.finditer(text):
        tag = m.group(1)
        line = text.count('\n', 0, m.start()) + 1
        if in_raw:
            if tag == 'endraw':
                in_raw = False
                if stack and stack[-1][0] == 'raw':
                    stack.pop()
                else:
                    out.append('%s:%d: endraw 짝이 없다' % (rel, line))
            continue
        if tag == 'raw':
            in_raw = True
            stack.append(('raw', line))
            continue
        if tag in OPENERS:
            stack.append((tag, line))
        elif tag in CLOSERS:
            want = None
            for o, c in PAIRS.items():
                if c == tag:
                    want = o
                    break
            if not stack:
                out.append('%s:%d: %s 가 열린 블록 없이 나왔다' % (rel, line, tag))
            elif stack[-1][0] != want:
                out.append('%s:%d: %s 가 나왔지만 열려 있는 것은 %s (%d번째 줄)'
                           % (rel, line, tag, stack[-1][0], stack[-1][1]))
                stack.pop()
            else:
                stack.pop()
        elif tag in NEUTRAL:
            pass
    for tag, line in stack:
        out.append('%s:%d: %s 블록이 닫히지 않았다' % (rel, line, tag))
    return out


def main():
    files = collect()
    problems = []
    for p in files:
        problems.extend(check(p))
    print('검사 %d개 파일' % len(files))
    if problems:
        print('')
        print('[문제] %d건' % len(problems))
        for x in problems:
            print('  -', x)
        return 1
    print('')
    print('[통과] Liquid 블록 균형 이상 없음')
    return 0


if __name__ == '__main__':
    sys.exit(main())
