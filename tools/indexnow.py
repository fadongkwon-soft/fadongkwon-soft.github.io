# -*- coding: utf-8 -*-
"""IndexNow 로 바뀐 페이지를 네이버·Bing(·Yandex 등 IndexNow 참여 엔진)에 한 번에 알린다(2026-10-28).

왜: 구글은 '색인 생성 요청'을 일괄로 보내는 공식 API 가 없다(Indexing API 는 채용 공고·라이브 영상 전용).
네이버와 Bing 은 IndexNow 를 지원해서 URL 수천 개를 요청 한 번에 알릴 수 있다. 배포 직후 자동으로 부른다.

동작: 공개 사이트맵(https://fadongkwon.com/sitemap.xml)을 읽어 lastmod 가 최근 N시간 안인 URL 만 보낸다.
배포 job 에는 빌드 결과(_site)가 없어서 git diff 대신 라이브 사이트맵을 기준으로 삼는다 —
push 배포와 예약 글 공개(정기 빌드) 둘 다 같은 방법으로 잡힌다.

키: 사이트 루트의 <KEY>.txt (내용 = 키). 공개가 전제인 값이라 비밀값이 아니다.

usage:
  python tools/indexnow.py                 최근 36시간 안에 바뀐 URL
  python tools/indexnow.py --hours 72
  python tools/indexnow.py --all           사이트맵 전체(처음 한 번, 또는 구조 개편 뒤)
  python tools/indexnow.py --dry-run       보내지 않고 목록만
"""
import argparse
import datetime as dt
import json
import re
import sys
import urllib.request

HOST = 'fadongkwon.com'
KEY = '2da61bf7e8e102da89e4c69d31a8bd72'
KEY_LOCATION = f'https://{HOST}/{KEY}.txt'
SITEMAP = f'https://{HOST}/sitemap.xml'
# api.indexnow.org 는 받은 URL 을 참여 엔진(Bing·Yandex·Seznam 등)에 공유한다. 네이버는 자체 엔드포인트도 함께 부른다.
ENDPOINTS = ['https://api.indexnow.org/indexnow', 'https://searchadvisor.naver.com/indexnow']
BATCH = 10000  # IndexNow 한 요청당 상한


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'fadongkwon-indexnow/1.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8')


def sitemap_urls():
    xml = fetch(SITEMAP)
    out = []
    for block in re.findall(r'<url>(.*?)</url>', xml, re.S):
        loc = re.search(r'<loc>([^<]+)</loc>', block)
        lm = re.search(r'<lastmod>([^<]+)</lastmod>', block)
        if not loc:
            continue
        when = None
        if lm:
            try:
                when = dt.datetime.fromisoformat(lm.group(1).strip())
            except ValueError:
                when = None
        out.append((loc.group(1).strip(), when))
    return out


def post(endpoint, urls):
    body = json.dumps({'host': HOST, 'key': KEY, 'keyLocation': KEY_LOCATION, 'urlList': urls}).encode('utf-8')
    req = urllib.request.Request(endpoint, data=body, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, ''
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')[:200]
    except Exception as e:  # noqa: BLE001 — 알림 실패가 배포를 막으면 안 된다
        return 0, str(e)[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--hours', type=float, default=36)
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()

    rows = sitemap_urls()
    if a.all:
        urls = [u for u, _ in rows]
    else:
        cut = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=a.hours)
        urls = [u for u, w in rows if w is not None and w.astimezone(dt.timezone.utc) >= cut]
    urls = [u for u in dict.fromkeys(urls) if u.startswith(f'https://{HOST}/')]
    print(f'사이트맵 {len(rows)}개 중 보낼 URL {len(urls)}개' + (' (전체)' if a.all else f' (최근 {a.hours:g}시간)'))
    for u in urls[:20]:
        print('  ', u)
    if len(urls) > 20:
        print(f'   … 외 {len(urls) - 20}개')
    if a.dry_run or not urls:
        return 0
    for ep in ENDPOINTS:
        for i in range(0, len(urls), BATCH):
            code, msg = post(ep, urls[i:i + BATCH])
            # 200 = 접수, 202 = 접수(키 확인 대기). 그 밖은 경고만 하고 배포는 그대로 둔다.
            ok = code in (200, 202)
            print(f'{ep} → HTTP {code}{"" if ok else " " + msg}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
