#!/usr/bin/env ruby
#
# 컬렉션 문서에도 "미래 날짜는 아직 공개하지 않는다"를 적용한다 (2026-09-10).
#
# 왜 필요한가
#   Jekyll 의 future 제외는 _posts 에만 걸린다. 컬렉션(_en_posts)은 date 가
#   미래여도 그대로 빌드돼 즉시 공개된다. 그래서 한/영 쌍을 미래 날짜로 예약하면
#   한국어판은 대기하는데 영문판만 먼저 나갔다.
#
#   게다가 영문판의 언어 스위처(_includes/topbar.html)는 page.alt_url 로 아직
#   빌드되지 않은 한국어 주소를 가리키게 되고, 그 깨진 내부 링크 때문에
#   htmlproofer(Test site) 가 exit 1 로 죽는다. 2026-09-10 실제로 이것 때문에
#   예약 게시 4편 커밋의 빌드가 실패했다.
#
# 무엇을 하는가
#   읽기가 끝난 직후(:post_read) posts 를 제외한 모든 컬렉션에서 date 가 미래인
#   문서를 뺀다. 제너레이터(jekyll-archives)와 렌더링은 그 뒤에 돌기 때문에
#   목록·태그·아카이브 페이지에서도 함께 사라진다.
#   date 가 없는 문서(_tabs 등)는 건드리지 않는다.
#   _config.yml 에 future: true 를 두면 이 훅은 아무것도 하지 않는다(로컬 미리보기용).

Jekyll::Hooks.register :site, :post_read do |site|
  next if site.config['future']

  now = Time.now
  removed = 0

  site.collections.each do |label, collection|
    next if label == 'posts' # posts 는 Jekyll 이 이미 처리한다

    collection.docs.reject! do |doc|
      d = doc.data['date']
      if d.is_a?(Time) && d > now
        removed += 1
        true
      else
        false
      end
    end
  end

  Jekyll.logger.info 'Scheduled:', "#{removed} future collection document(s) held back" if removed > 0
end
