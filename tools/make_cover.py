# -*- coding: utf-8 -*-
"""블로그 커버(1200x630) 생성 — 기존 회고 글 커버와 같은 모양(어두운 배경, 코랄 키커, 흰 제목, 부제, 라벨 줄 4개, 푸터).

usage: python tools/make_cover.py <spec.json>
spec: {"out": "assets/img/<YYYYMMDD>_<slug>/cover.png", "kicker": "...", "title": "...", "sub": "...",
       "rows": [["라벨", "문장"], ...] (최대 4), "footer": "fadongkwon.com"}
여러 개면 spec 을 배열로.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

FB = r"C:\Windows\Fonts\malgunbd.ttf"
FR = r"C:\Windows\Fonts\malgun.ttf"
W, H = 1200, 630
BG = (23, 20, 21)
CORAL = (255, 110, 90)
WHITE = (245, 242, 240)
GREY = (170, 165, 165)
ROW_BG = (38, 32, 33)


def fit(path, text, size, max_w, min_size=18):
    while size > min_size and ImageFont.truetype(path, size).getlength(text) > max_w:
        size -= 2
    return ImageFont.truetype(path, size)


def make(spec):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    # 은은한 세로 그라데이션
    for y in range(H):
        t = y / H
        c = tuple(int(BG[i] + (10 - BG[i] * 0.05) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    x = 64
    d.text((x, 62), spec['kicker'], font=fit(FB, spec['kicker'], 30, W - 2 * x), fill=CORAL)
    tf = fit(FB, spec['title'], 66, W - 2 * x, 40)
    d.text((x, 108), spec['title'], font=tf, fill=WHITE)
    th = tf.getbbox(spec['title'])[3]
    sy = 108 + th + 22
    if spec.get('sub'):
        d.text((x, sy), spec['sub'], font=fit(FR, spec['sub'], 26, W - 2 * x), fill=GREY)
    rows = spec.get('rows', [])[:4]
    top = 280
    rh, gap = 58, 14
    lf = ImageFont.truetype(FB, 26)
    for i, (label, text) in enumerate(rows):
        y = top + i * (rh + gap)
        d.rounded_rectangle([x, y, W - x, y + rh], radius=8, fill=ROW_BG)
        d.rectangle([x, y, x + 5, y + rh], fill=CORAL)
        d.text((x + 34, y + 15), label, font=lf, fill=CORAL)
        lw = max(lf.getlength(label), 60)
        tx = x + 34 + lw + 36
        d.text((tx, y + 15), text, font=fit(FR, text, 26, W - x - tx - 16, 18), fill=WHITE)
    d.text((x, H - 44), spec.get('footer', 'fadongkwon.com'), font=ImageFont.truetype(FR, 22), fill=GREY)
    out = spec['out']
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, optimize=True)
    return out


if __name__ == '__main__':
    specs = json.load(open(sys.argv[1], encoding='utf-8'))
    if isinstance(specs, dict):
        specs = [specs]
    for s in specs:
        print('wrote', make(s))
