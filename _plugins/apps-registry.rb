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

Jekyll::Hooks.register :site, :after_init do |site|
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
    # 아이콘은 CSV 가 절대 URL(앱이 실행 중에 받아가므로) — 사이트에서는 상대 경로로 쓴다.
    h['icon_path'] = h['icon'].to_s.sub(%r{\Ahttps?://[^/]+}, '')
    h
  end

  live = rows.select { |h| h['live'] }.sort_by { |h| h['sort'] }
  site.data['apps'] = live
  site.data['apps_all'] = rows
  site.data['apps_count'] = live.length

  Jekyll.logger.info 'apps-registry:', "apps.csv 에서 #{live.length}개(전체 #{rows.length}개) 적재"
end
