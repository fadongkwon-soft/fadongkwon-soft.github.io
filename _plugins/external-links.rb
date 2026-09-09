#!/usr/bin/env ruby
#
# 본문에서 '사이트를 떠나는 링크'를 새 탭으로 열고, 그 사실을 눈과 화면 낭독기 양쪽에
# 알려 준다 (2026-09-09).
#
# 대상
#   - 외부 호스트 링크: play.google.com, instagram.com, toss.im, developers-... 등
#   - /toss/<id>/ 리다이렉트 페이지: 우리 주소지만 곧바로 앱인토스로 나가는 페이지다
#     (https://fadongkwon.com/toss/... 처럼 절대 주소로 쓴 것도 같게 본다)
#
# 대상이 아닌 것 (일부러 그대로 둔다)
#   - 사이트 내부 링크. 같은 사이트 안의 이동은 이탈이 아니라 추가 페이지뷰이고,
#     새 탭을 띄우면 탭이 쌓이고 뒤로가기 기대가 깨진다.
#   - mailto:·tel:·#앵커.
#   - 이미 target 이 붙어 있는 앵커(사이드바 등 테마가 처리한 것)는 속성을 건드리지 않는다.
#
# 붙이는 것
#   target="_blank" rel="noopener"
#   <span class="ext-mark" aria-hidden="true">↗</span>  — 눈으로 보는 표시. 낭독기는 건너뛴다.
#   <span class="ext-sr"> (새 창에서 열림)</span>       — 화면에서 숨고 낭독기만 읽는다.
#   새 창으로 열리는 것을 미리 알리지 않으면 WCAG 3.2.5 지적 대상이라 둘을 함께 넣는다.
#   문구는 문서 언어(lang)에 맞춘다. 스타일은 _includes/head.html 의 .ext-mark/.ext-sr.
#
# :post_convert 훅에서 doc.content(마크다운이 HTML 로 바뀐 본문)만 고치므로
# 사이드바·상단바·관련글 같은 테마 영역의 앵커는 영향을 받지 않는다.
# 이미 표시가 붙은 앵커는 건너뛰므로 두 번 적용돼도 중복되지 않는다.
#
# 전부 새 탭으로 바꾸고 싶으면 leaves_site? 가 항상 true 를 돌려주게 하면 된다.

module FadongExternalLinks
  SELF_HOSTS = ['fadongkwon.com', 'www.fadongkwon.com'].freeze

  A_ELEMENT = %r{<a\s([^>]*?)>(.*?)</a>}im
  HREF = /href\s*=\s*("|')(.*?)\1/i
  REL = /\brel\s*=\s*("|')(.*?)\1/i
  HAS_TARGET = /\btarget\s*=/i
  HAS_IMG = /<img\b/i
  ALREADY_MARKED = /\bext-sr\b/
  ABS_URL = %r{\A(?:https?:)?//([^/?\#]+)}i

  HINTS = { 'ko' => ' (새 창에서 열림)', 'en' => ' (opens in a new tab)' }.freeze
  MARK = '<span class="ext-mark" aria-hidden="true">↗</span>'.freeze

  # 이 링크를 누르면 우리 사이트를 벗어나는가?
  def self.leaves_site?(url)
    u = url.to_s.strip
    m = ABS_URL.match(u)
    unless m.nil?
      return true unless SELF_HOSTS.include?(m[1].downcase.split(':').first)

      # 자기 사이트를 절대 주소로 쓴 링크 — 경로만 떼어 내부 규칙을 그대로 적용한다.
      u = u[m.end(0)..-1].to_s
      u = '/' if u.empty?
    end

    u.start_with?('/toss/')
  end

  # 여는 태그의 속성에 target·rel 을 채운다. 이미 target 이 있으면 그대로 둔다.
  def self.with_new_tab(attrs)
    return attrs if attrs =~ HAS_TARGET

    rel = REL.match(attrs)
    if rel.nil?
      attrs = "#{attrs.rstrip} rel=\"noopener\""
    else
      vals = rel[2].split
      vals << 'noopener' unless vals.map(&:downcase).include?('noopener')
      attrs = attrs[0, rel.begin(0)].to_s + "rel=\"#{vals.join(' ')}\"" + attrs[rel.end(0)..-1].to_s
    end

    "#{attrs.rstrip} target=\"_blank\""
  end

  def self.apply(html, lang)
    hint = HINTS[lang] || HINTS['ko']

    html.gsub(A_ELEMENT) do |element|
      attrs = Regexp.last_match(1) # 아래에서 다른 정규식을 쓰기 전에 둘 다 먼저 확보한다
      inner = Regexp.last_match(2)
      href = HREF.match(attrs)

      if href.nil? || !leaves_site?(href[2]) || inner =~ ALREADY_MARKED
        element
      else
        mark = inner =~ HAS_IMG ? '' : MARK # 이미지 링크 뒤에는 화살표를 붙이지 않는다
        "<a #{with_new_tab(attrs)}>#{inner}#{mark}<span class=\"ext-sr\">#{hint}</span></a>"
      end
    end
  end
end

Jekyll::Hooks.register [:posts, :pages, :documents], :post_convert do |doc|
  next unless doc.respond_to?(:content)
  next unless doc.content.is_a?(String)
  next if doc.respond_to?(:output_ext) && doc.output_ext != '.html'

  english = doc.data['lang'].to_s.downcase.start_with?('en') ||
            doc.url.to_s.start_with?('/en/')
  doc.content = FadongExternalLinks.apply(doc.content, english ? 'en' : 'ko')
end
