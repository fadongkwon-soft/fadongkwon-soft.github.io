# -*- coding: utf-8 -*-
"""Google Play 설치 중간 랜딩(/play-store/<id>/)을 apps.csv 로 생성한다.

왜 두는가 — 토스는 `intoss://` 딥링크라 중간 랜딩이 꼭 필요했고, 그 김에 PC 방문자용
QR 도 거기 뒀다. 그런데 **토스 랜딩에 Play QR 을 같이 놓으니 기대와 어긋났다** —
'앱인토스 열기'로 들어왔는데 Play QR 이 보이는 상황. 그래서 플랫폼마다 같은 모양의
랜딩을 두어 양쪽 경험을 맞춘다(사용자 결정, 2026-09-11).

토스 랜딩(toss/<id>.html)은 앱마다 딥링크 스킴이 달라 손으로 만들지만, Play 는
패키지명만 있으면 되므로 이 스크립트가 전량 생성한다. 라이브(play=1)인 앱만 만든다 —
미출시 앱에 링크하면 스토어에서 404 가 난다.

usage:
  python tools/gen_store_landings.py            # 없거나 내용이 다른 것만 쓴다
  python tools/gen_store_landings.py --check    # 무엇이 바뀔지만 출력
"""
import csv
import io
import os
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'play-store')

TPL = """---
# Google Play 설치 중간 랜딩. tools/gen_store_landings.py 가 apps.csv 로 생성한다 — 손으로 고치지 말 것.
# 토스 랜딩(/toss/<id>/)과 같은 모양을 주려고 둔다. PC 방문자는 QR 로 휴대폰에 넘어간다.
layout: none
permalink: /play-store/{id}/
store: play
app_name: '{name}'
---
{{% include app-redirect.html %}}
"""


def main():
    check = '--check' in sys.argv[1:]
    rows = list(csv.DictReader(io.open(os.path.join(ROOT, 'apps.csv'), encoding='utf-8-sig')))
    live = [r for r in rows
            if r.get('play', '').strip() == '1' and r.get('play_package', '').strip()]
    os.makedirs(OUT, exist_ok=True)

    want = {}
    for r in live:
        # ⚠️ app_name 은 반드시 따옴표로. 숫자만 있는 이름('2048')이 YAML 에서
        #    정수로 파싱되면 Jekyll 의 slugify 가 터져 빌드가 죽는다(2026-09-11 실제 사고).
        want[r['id']] = TPL.format(id=r['id'], name=r['name'].replace("'", "''"))

    wrote, same, removed = [], [], []
    for aid, body in want.items():
        p = os.path.join(OUT, aid + '.html')
        cur = io.open(p, encoding='utf-8').read().replace('\r\n', '\n') if os.path.exists(p) else None
        if cur == body:
            same.append(aid)
            continue
        wrote.append(aid)
        if not check:
            io.open(p, 'w', encoding='utf-8', newline='\n').write(body)

    # 라이브가 아닌데 남아 있는 랜딩은 지운다(스토어에서 404 가 난다)
    for p in sorted(glob.glob(os.path.join(OUT, '*.html'))):
        aid = os.path.basename(p)[:-5]
        if aid not in want:
            removed.append(aid)
            if not check:
                os.remove(p)

    print('Play 라이브 %d개 / 유지 %d · %s %d · 제거 %d'
          % (len(live), len(same), '갱신 예정' if check else '갱신', len(wrote), len(removed)))
    for label, items in (('갱신', wrote), ('제거', removed)):
        if items:
            print('  %s: %s' % (label, ', '.join(items)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
