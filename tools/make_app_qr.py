# -*- coding: utf-8 -*-
"""앱별 QR 두 종을 만든다 — 토스 미니앱 실행용, Play 스토어 페이지용.

왜 필요한가 — `/toss/<id>/` 랜딩은 `intoss://` 딥링크를 여는 곳이라 **PC 에서는 열 수 없다.**
PC 로 들어온 사람이 휴대폰으로 옮겨 갈 방법이 없었다. QR 을 두면 카메라로 찍어 바로 넘어간다.
Play 쪽도 같은 이유로 스토어 페이지 QR 을 함께 둔다.

QR 이 담는 값
  토스: **랜딩 페이지 URL**(https://fadongkwon.com/toss/<id>/)
        `intoss://` 를 직접 담으면 휴대폰 기본 카메라가 커스텀 스킴을 못 여는 경우가 있어서,
        인스타 카드와 같은 방식으로 랜딩을 거쳐 딥링크를 태운다.
  Play: https://play.google.com/store/apps/details?id=<패키지>

중앙에 앱 아이콘을 얹고(app-icons/<id>.png) cv2 로 디코드해 값을 검증한다.

## 함정 두 개 (둘 다 실제로 밟았다, 2026-09-11)
1. **생성한 QR 을 임의 크기로 리사이즈하면 안 된다.** 원본 한 변이 목표 크기의 약수가
   아니면 NEAREST 로 늘려도 모듈 폭이 불균일해져 디코드가 깨진다. URL 길이에 따라 QR
   버전(=원본 크기)이 달라서 **일부 앱만** 깨지는 형태로 나타난다(420px 로 맞췄다가 4개 깨짐).
   크기는 box_size 로 정하고 표시 크기는 CSS 로 조절한다.
2. **cv2 5.0 의 QR 디텍터는 특정 패턴을 아예 못 찾는다.** 모듈 크기를 8~14 로 바꿔도,
   ECC 를 낮춰도 실패하던 QR 이 흰 여백을 24px 주면 읽혔고 48px 에서는 다시 실패했다.
   즉 디코드 실패가 곧 QR 불량이 아니다 → **여러 여백으로 재시도**해서 하나라도 값이
   맞으면 통과로 본다. (그래도 1번 같은 진짜 불량은 전부 걸러진다)

usage:
  python tools/make_app_qr.py            # 없거나 값이 다른 것만 다시 만든다
  python tools/make_app_qr.py --force    # 전부 다시 만든다
"""
import csv
import io
import os
import sys
import glob

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image
import cv2

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICON_DIR = os.path.join(ROOT, 'app-icons')
TOSS_DIR = os.path.join(ROOT, 'assets', 'img', 'toss-qr')
PLAY_DIR = os.path.join(ROOT, 'assets', 'img', 'play-qr')
BOX = 8             # 모듈 한 변(px)
ICON_RATIO = 0.21   # 아이콘 폭 비율. 0.25 넘으면 디코드가 깨지기 시작한다.
PROBE_PADS = (0, 16, 24, 32, 40)   # 검증용 여백 후보(함정 2번)


def apps():
    p = os.path.join(ROOT, 'apps.csv')
    return list(csv.DictReader(io.open(p, encoding='utf-8-sig')))


def landing_ids():
    return [os.path.basename(p)[:-5] for p in sorted(glob.glob(os.path.join(ROOT, 'toss', '*.html')))]


def make_qr(url, icon_path):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=BOX, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white').convert('RGB')
    if icon_path and os.path.exists(icon_path):
        side = int(img.width * ICON_RATIO)
        pad = max(4, side // 10)
        icon = Image.open(icon_path).convert('RGB').resize((side, side), Image.LANCZOS)
        plate = Image.new('RGB', (side + pad * 2, side + pad * 2), 'white')
        plate.paste(icon, (pad, pad))
        off = (img.width - plate.width) // 2
        img.paste(plate, (off, off))
    return img


def decodes_to(path, want):
    """여러 여백으로 재시도해 하나라도 값이 맞으면 True (함정 2번 참고)."""
    base = Image.open(path).convert('RGB')
    det = cv2.QRCodeDetector()
    tmp = os.path.join(ROOT, '.qr-probe.png')
    try:
        for pad in PROBE_PADS:
            if pad:
                canvas = Image.new('RGB', (base.width + pad * 2, base.height + pad * 2), 'white')
                canvas.paste(base, (pad, pad))
            else:
                canvas = base
            canvas.save(tmp)
            im = cv2.imread(tmp)
            ok, dec, _, _ = det.detectAndDecodeMulti(im)
            vals = [v for v in (dec if ok else []) if v]
            if not vals:
                v = det.detectAndDecode(im)[0]
                vals = [v] if v else []
            if want in vals:
                return True
        return False
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def build(jobs, force):
    made, kept, bad = [], [], []
    for out_dir, key, url, icon in jobs:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, key + '.png')
        if os.path.exists(dst) and not force and decodes_to(dst, url):
            kept.append(key)
            continue
        make_qr(url, icon).save(dst)
        if decodes_to(dst, url):
            made.append(key)
            continue
        # 아이콘이 가려 못 읽히는 경우가 있으니 아이콘 없이 한 번 더
        make_qr(url, None).save(dst)
        (made if decodes_to(dst, url) else bad).append(key)
    return made, kept, bad


def main():
    force = '--force' in sys.argv[1:]
    rows = apps()
    by_id = {r['id']: r for r in rows}
    landings = landing_ids()

    jobs = []
    for lid in landings:
        icon = os.path.join(ICON_DIR, lid + '.png')
        jobs.append((TOSS_DIR, lid, 'https://fadongkwon.com/toss/%s/' % lid,
                     icon if os.path.exists(icon) else None))
    for r in rows:
        pkg = (r.get('play_package') or '').strip()
        if not pkg or r.get('play', '').strip() != '1':
            continue
        icon = os.path.join(ICON_DIR, r['id'] + '.png')
        jobs.append((PLAY_DIR, r['id'],
                     'https://play.google.com/store/apps/details?id=' + pkg,
                     icon if os.path.exists(icon) else None))

    made, kept, bad = build(jobs, force)
    print('토스 랜딩 %d개 / Play 라이브 %d개' % (len(landings), sum(1 for r in rows if r.get('play') == '1')))
    print('새로 만듦 %d개, 유지 %d개' % (len(made), len(kept)))
    if bad:
        print('[실패] 값이 확인되지 않는 QR:', *bad, sep='\n  ')
        return 1
    print('전부 디코드 검증 통과')
    return 0


if __name__ == '__main__':
    sys.exit(main())
