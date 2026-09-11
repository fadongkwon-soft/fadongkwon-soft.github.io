# frozen_string_literal: true

# 루트 apps.csv 를 site.data['apps'] 로 읽어 들인다.
#
# 왜 플러그인인가 — apps.csv 는 **크로스 프로모션의 단일 소스**다. 모든 앱이 실행 중에
# https://fadongkwon.com/apps.csv 를 받아가므로 루트에 그대로 서빙되어야 하고, 그래서
# Jekyll 이 자동으로 읽어 주는 `_data/` 에 둘 수 없다. 사본을 만들면 둘이 갈라진다.
# 이 훅이 같은 파일을 빌드 시점에 읽어 Liquid 에서 쓸 수 있게 한다.
#
# 갱신 흐름: 게임 저장소에서 `pnpm publish:registry` 로 apps.csv 를 이 저장소에 복사·푸시
#   → 그 푸시가 빌드를 돌리고 → /apps/ · /ko/apps/ 목록이 자동으로 최신이 된다.
#   즉 **앱을 낼 때마다 글을 고칠 필요가 없다.**
#
# 컬럼: id,name,tagline,emoji,play_package,toss_scheme,play,toss,name_en,tagline_en,
#       icon,tagline_toss,tags,pos,kids
#   play / toss 는 '1' 이면 그 플랫폼에 라이브. 둘 다 0 이면 미출시라 목록에서 뺀다.
#   pos 는 유사도 1차원 좌표(가까운 값 = 비슷한 앱)라 정렬에 쓰면 같은 계열이 붙는다.
require 'csv'

# ⚠️ 훅은 반드시 :post_read 다. :after_init 에 넣으면 그 뒤 Jekyll 이 _data 를 읽으면서
#    site.data 를 **통째로 새 해시로 교체**해 여기서 넣은 키가 사라진다.
#    빌드는 성공하고 페이지도 200 이지만 목록이 빈 채로 나간다(2026-09-11 실제로 겪음).
Jekyll::Hooks.register :site, :post_read do |site|
  path = File.join(site.source, 'apps.csv')
  next unless File.exist?(path)

  rows = CSV.read(path, headers: true, encoding: 'bom|utf-8').map do |r|
    h = r.to_h
    h['live'] = h['play'].to_s.strip == '1' || h['toss'].to_s.strip == '1'
    h['on_play'] = h['play'].to_s.strip == '1'
    h['on_toss'] = h['toss'].to_s.strip == '1'
    h['kids_app'] = h['kids'].to_s.strip == '1'
    # 정렬 키. pos 가 비어 있으면 맨 뒤로 보낸다.
    h['sort'] = h['pos'].to_s.strip.empty? ? 999_999 : h['pos'].to_i
    h['tag_list'] = h['tags'].to_s.split(';').map(&:strip).reject(&:empty?)
    # 토스 딥링크 랜딩 페이지가 실제로 있는 앱만 그 링크를 낸다.
    # (없는 앱에 링크하면 htmlproofer 가 빌드를 죽인다 — saju-lotto 가 실제로 없다)
    landing = File.join(site.source, 'toss', "#{h['id']}.html")
    h['toss_landing'] = File.exist?(landing) ? "/toss/#{h['id']}/" : nil
    # Play 도 같은 모양의 중간 랜딩을 둔다(tools/gen_store_landings.py 가 생성).
    play_landing = File.join(site.source, 'play-store', "#{h['id']}.html")
    h['play_landing'] = File.exist?(play_landing) ? "/play-store/#{h['id']}/" : nil
    # 아이콘은 CSV 가 절대 URL(앱이 실행 중에 받아가므로) — 사이트에서는 상대 경로로 쓴다.
    h['icon_path'] = h['icon'].to_s.sub(%r{\Ahttps?://[^/]+}, '')
    # 게임/비게임은 tags 의 '게임' 유무로 갈린다(현재 게임 21 / 비게임 8).
    h['is_game'] = h['tag_list'].include?('게임')
    # 출시일. registry/apps.csv 의 released 컬럼이 근거다(비면 정렬 맨 뒤).
    h['released'] = h['released'].to_s.strip
    h['released_key'] = h['released'].empty? ? '0000-00-00' : h['released']
    h
  end

  # 출시 역순(최신 먼저). 같은 날 출시가 많아 2차 키로 pos(유사도 좌표)를 써서
  # 같은 계열이 붙어 나오게 한다.
  live = rows.select { |h| h['live'] }
             .sort_by { |h| [h['released_key'], -h['sort']] }
             .reverse
  site.data['apps'] = live
  site.data['apps_games'] = live.select { |h| h['is_game'] }
  site.data['apps_others'] = live.reject { |h| h['is_game'] }
  site.data['apps_all'] = rows
  site.data['apps_count'] = live.length
  # 플랫폼별 출시 현황도 그대로 넘긴다. 목록에서 걸러 내지 않고 **칸마다 상태를 보여준다** —
  # 한쪽만 라이브인 앱이 실제로 있다(2026-09-11: 신규 3종은 Play 라이브·토스 심사 대기).
  site.data['apps_play_count'] = rows.count { |h| h['on_play'] }
  site.data['apps_toss_count'] = rows.count { |h| h['on_toss'] }

  # 빈 목록이 조용히 배포되는 것을 막는다. apps.csv 가 있는데 한 개도 못 읽었다면
  # 컬럼 이름이나 훅 시점이 깨진 것이므로 빌드를 세운다(페이지는 200 이라 아무도 못 잡는다).
  raise "apps-registry: apps.csv 를 읽었는데 라이브 앱이 0개다 (컬럼·훅 시점 확인)" if live.empty?

  Jekyll.logger.info 'apps-registry:',
                     "apps.csv 적재: 라이브 #{live.length} / Play #{site.data['apps_play_count']} "                      "/ 토스 #{site.data['apps_toss_count']} (전체 #{rows.length})"
end
