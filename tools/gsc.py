# -*- coding: utf-8 -*-
"""Search Console API — 색인 상태 일괄 조회·사이트맵 제출·실적 요약(2026-10-28).

왜: 콘솔 웹에서 URL 을 하나씩 검사하던 일을 한 번에 한다. 구글에는 '색인 생성 요청'을 일괄로 보내는
공식 API 가 없으므로(Indexing API 는 채용 공고·라이브 영상 전용) 그 버튼만 사람이 누른다.
이 스크립트는 그 버튼을 누를 후보(색인 안 된 핵심 글)를 골라 주는 쪽이다.

인증: 서비스 계정 키(GSC_SA_KEY 환경 변수, 기본 D:/Workspace/revenue-ledger/play_service_account.json).
      그 계정 이메일을 Search Console 속성(sc-domain:fadongkwon.com)의 사용자로 '전체' 권한으로 추가해야 한다
      (설정 → 사용자 및 권한 → 사용자 추가). 추가 전에는 403.
할당량: URL 검사 API 속성당 하루 2,000건·분당 600건 → 사이트맵 전체(약 500건)를 매일 돌려도 된다.

usage:
  python tools/gsc.py inspect [--only ko|en|all] [--limit N]   사이트맵 URL 색인 상태 → tools/out/gsc-inspect-<날짜>.csv
  python tools/gsc.py sitemap                                   sitemap.xml 다시 제출
  python tools/gsc.py perf [--days 7] [--ko]                    클릭·노출 요약(페이지별 상위)
"""
import argparse
import csv
import datetime as dt
import os
import re
import sys
import time
import urllib.request

SITE = 'sc-domain:fadongkwon.com'
SITEMAP = 'https://fadongkwon.com/sitemap.xml'
KEY = os.environ.get('GSC_SA_KEY', 'D:/Workspace/revenue-ledger/play_service_account.json')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')


def client():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_file(
        KEY, scopes=['https://www.googleapis.com/auth/webmasters'])
    return build('searchconsole', 'v1', credentials=creds, cache_discovery=False)


def sitemap_urls():
    with urllib.request.urlopen(SITEMAP, timeout=30) as r:
        xml = r.read().decode('utf-8')
    return re.findall(r'<loc>([^<]+)</loc>', xml)


def cmd_inspect(a):
    sc = client()
    urls = sitemap_urls()
    if a.only == 'ko':
        urls = [u for u in urls if '/ko/' in u]
    elif a.only == 'en':
        urls = [u for u in urls if '/ko/' not in u]
    if a.limit:
        urls = urls[:a.limit]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f'gsc-inspect-{dt.date.today().isoformat()}.csv')
    counts = {}
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['url', 'verdict', 'coverageState', 'lastCrawlTime', 'googleCanonical'])
        for i, u in enumerate(urls, 1):
            for attempt in range(3):
                try:
                    r = sc.urlInspection().index().inspect(body={'inspectionUrl': u, 'siteUrl': SITE}).execute()
                    break
                except Exception as e:  # noqa: BLE001
                    if attempt == 2:
                        r = {'inspectionResult': {'indexStatusResult': {'coverageState': f'ERROR {str(e)[:80]}'}}}
                    else:
                        time.sleep(3)
            s = r.get('inspectionResult', {}).get('indexStatusResult', {})
            state = s.get('coverageState', '')
            counts[state] = counts.get(state, 0) + 1
            w.writerow([u, s.get('verdict', ''), state, s.get('lastCrawlTime', ''), s.get('googleCanonical', '')])
            if i % 50 == 0:
                print(f'  {i}/{len(urls)}')
            time.sleep(0.12)  # 분당 600건 아래로
    print(f'{len(urls)}건 → {path}')
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f'  {v:4}  {k}')


def cmd_sitemap(a):
    sc = client()
    sc.sitemaps().submit(siteUrl=SITE, feedpath=SITEMAP).execute()
    info = sc.sitemaps().get(siteUrl=SITE, feedpath=SITEMAP).execute()
    print('제출 완료:', info.get('lastSubmitted'), '· 마지막 다운로드', info.get('lastDownloaded'),
          '· 경고', info.get('warnings'), '· 오류', info.get('errors'))


def cmd_perf(a):
    sc = client()
    end = dt.date.today() - dt.timedelta(days=2)  # 실적 데이터는 2~3일 늦다
    start = end - dt.timedelta(days=a.days - 1)
    body = {'startDate': start.isoformat(), 'endDate': end.isoformat(), 'dimensions': ['page'], 'rowLimit': 25}
    if a.ko:
        body['dimensionFilterGroups'] = [{'filters': [{'dimension': 'page', 'operator': 'contains', 'expression': '/ko/'}]}]
    r = sc.searchanalytics().query(siteUrl=SITE, body=body).execute()
    rows = r.get('rows', [])
    clicks = sum(x['clicks'] for x in rows)
    imps = sum(x['impressions'] for x in rows)
    print(f'{start} ~ {end}{" (/ko/)" if a.ko else ""}: 상위 {len(rows)}페이지 클릭 {clicks:g} · 노출 {imps:g}')
    for x in rows[:15]:
        print(f'  {x["clicks"]:3g} / {x["impressions"]:5g}  {x["keys"][0]}')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('inspect'); p.add_argument('--only', choices=['ko', 'en', 'all'], default='all'); p.add_argument('--limit', type=int)
    sub.add_parser('sitemap')
    p = sub.add_parser('perf'); p.add_argument('--days', type=int, default=7); p.add_argument('--ko', action='store_true')
    a = ap.parse_args()
    {'inspect': cmd_inspect, 'sitemap': cmd_sitemap, 'perf': cmd_perf}[a.cmd](a)


if __name__ == '__main__':
    sys.exit(main())
