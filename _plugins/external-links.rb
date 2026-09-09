#!/usr/bin/env ruby
#
# 본문에서 '사이트를 떠나는 링크'만 새 탭으로 연다 (2026-09-09).
#
# 대상
#   - 외부 호스트 링크: play.google.com, instagram.com, toss.im, developers-... 등
#   - /toss/<id>/ 리다이렉트 페이지: 우리 주소지만 곧바로 앱인토스로 나가는 페이지다
#
# 대상이 아닌 것 (일부러 그대로 둔다)
#   - 사이트 내부 링크. 같은 사이트 안의 이동은 이탈이 아니라 추가 페이지뷰이고,
#     새 탭을 띄우면 탭이 쌓이고 뒤로가기 기대가 깨진다.
#   - https://fadongkwon.com/... 처럼 절대 주소로 쓴 자기 사이트 링크도 내부로 본다.
#   - mailto:·tel:·#앵커.
#   - 이미 target 이 붙어 있는 앵커(사이드바 등 테마가 처리한 것)는 손대지 않는다.
#
# :post_convert 훅에서 doc.content(마크다운이 HTML 로 바뀐 본문)만 고치므로
# 사이드바·상단바·관련글 같은 테마 영역의 앵커는 영향을 받지 않는다.
#
# 전부 새 탭으로 바꾸고 싶으면 leaves_site? 가 항상 true 를 돌려주게 하면 된다.

module FadongExternalLinks
  SELF_HOSTS = ['fadongkwon.com', 'www.fadongkwon.com'].freeze

  A_TAG = /<a\s+([^>]*?)>/i
  HREF = /href\s*=\s*("|')(.*?)\1/i
  REL = /\brel\s*=\s*("|')(.*?)\1/i
  HAS_TARGET = /\btarget\s*=/i
  ABS_URL = %r{\A(?:https?:)?//([^/?\#]+)}i

  # 이 링크를 누르면 우리 사이트를 벗어나는가?
  def self.leaves_site?(url)
    u = url.to_s.strip
    m = ABS_URL.match(u)
    return !SELF_HOSTS.include?(m[1].downcase.split(':').first) unless m.nil?

    u.start_with?('/toss/')
  end

  def self.apply(html)
    html.gsub(A_TAG) do |tag|
      attrs = Regexp.last_match(1) # 아래에서 다른 정규식을 쓰기 전에 먼저 확보한다
      href = HREF.match(attrs)

      if attrs =~ HAS_TARGET || href.nil? || !leaves_site?(href[2])
        tag
      else
        rel = REL.match(attrs)
        if rel.nil?
          attrs = "#{attrs.rstrip} rel=\"noopener\""
        else
          vals = rel[2].split
          vals << 'noopener' unless vals.map(&:downcase).include?('noopener')
          attrs = attrs[0, rel.begin(0)].to_s + "rel=\"#{vals.join(' ')}\"" + attrs[rel.end(0)..-1].to_s
        end
        "<a #{attrs.rstrip} target=\"_blank\">"
      end
    end
  end
end

Jekyll::Hooks.register [:posts, :pages, :documents], :post_convert do |doc|
  next unless doc.respond_to?(:content)
  next unless doc.content.is_a?(String)
  next if doc.respond_to?(:output_ext) && doc.output_ext != '.html'

  doc.content = FadongExternalLinks.apply(doc.content)
end
