#!/usr/bin/env ruby
#
# 본문에서 '사이트를 떠나는 링크'를 새 탭으로 열고, 그 사실을 눈과 화면 낭독기 양쪽에
# 알려 준다 (2026-09-09).
#
# 대상
#   - 외부 호스트 링크: play.google.com, instagram.com, toss.im, developers-... 등
#   - /toss/<id>/, /play-store/<id>/ 설치 랜딩: 우리 주소지만 곧바로 스토어/앱으로
#     나가는 페이지다 (https://fadongkwon.com/toss/... 처럼 절대 주소로 쓴 것도 같게 본다)
#     ⚠️ Play 랜딩을 나중에 만들면서 여기 등록을 빠뜨려, 앱인토스는 새 탭인데 Play 만
#        같은 탭으로 전환됐다(사용자 제보 2026-09-11). 랜딩을 새로 만들면 여기도 추가할 것.
#
# 랜딩 링크에는 문서 언어를 ?lang= 으로 실어 보낸다.
#   랜딩(/toss/, /play-store/)은 언어 중립 주소다 — 인스타 QR·스토어에 박혀 있어서
#   /ko/ 를 붙이거나 영문판 주소를 따로 만들 수 없다. 그래서 한 페이지가 양쪽 언어를
#   모두 담고 파라미터로 고른다(_includes/app-redirect.html).
#   영어 글에서 눌렀는데 한국어 랜딩이 뜨던 문제를 여기서 막는다(사용자 제보 2026-09-11).
#   한국어 글에도 ?lang=ko 를 명시한다 — 한 번 영어로 바꾼 적이 있으면 localStorage 에
#   'en' 이 남아 한국어 글에서 눌러도 영문 랜딩이 뜬다.
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
  LANDING_PREFIXES = ['/toss/', '/play-store/'].freeze

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

    landing?(u)
  end

  # 랜딩 주소면 문서 언어를 ?lang= 으로 붙여 돌려준다. 아니면 그대로.
  def self.with_lang(url, lang)
    u = url.to_s.strip
    path = u
    m = ABS_URL.match(u)
    unless m.nil?
      return u unless SELF_HOSTS.include?(m[1].downcase.split(':').first)

      path = u[m.end(0)..-1].to_s
    end
    return u unless landing?(path)
    return u if u =~ /[?&]lang=/

    # #앵커가 있으면 그 **앞에** 넣는다. 뒤에 붙이면 브라우저가 쿼리로 읽지 않는다.
    head, sep, frag = u.partition('#')
    "#{head}#{head.include?('?') ? '&' : '?'}lang=#{lang}#{sep}#{frag}"
  end

  def self.landing?(path)
    LANDING_PREFIXES.any? { |prefix| path.to_s.start_with?(prefix) }
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

  # 여는 태그의 href 를 언어 파라미터가 붙은 주소로 갈아끼운다.
  def self.with_lang_href(attrs, href_match, lang)
    fixed = with_lang(href_match[2], lang)
    return attrs if fixed == href_match[2]

    q = href_match[1]
    attrs[0, href_match.begin(0)].to_s + "href=#{q}#{fixed}#{q}" + attrs[href_match.end(0)..-1].to_s
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
        attrs = with_lang_href(attrs, href, lang)
        "<a #{with_new_tab(attrs)}>#{inner}#{mark}<span class=\"ext-sr\">#{hint}</span></a>"
      end
    end
  end
end

Jekyll::Hooks.register [:posts, :pages, :documents], :post_convert do |doc|
  next unless doc.respond_to?(:content)
  next unless doc.content.is_a?(String)
  next if doc.respond_to?(:output_ext) && doc.output_ext != '.html'

  # 랜딩 페이지 자신은 건드리지 않는다. 여기 링크는 손으로 다 통제하고 있고,
  # 토스↔Play 상호 링크는 사이트 안 이동이라 새 탭으로 띄울 이유가 없다.
  next if FadongExternalLinks.landing?(doc.url.to_s)

  # 언어 판별은 front matter 의 lang 하나만 본다. 영어판은 전부 lang: en 을 선언한다
  # (_en_posts 는 _config.yml defaults 가, 탭·페이지는 각 파일이).
  # 예전엔 URL 이 /en/ 으로 시작하는지도 같이 봤는데, 2026-09-11 URL 전환으로
  # 영어가 루트(/*)로 옮겨가면서 그 조건은 죽은 코드가 됐다 — 지우고 lang 만 믿는다.
  # i18n_structcheck.py 의 check_lang_declared 가 선언 누락을 막는다.
  english = doc.data['lang'].to_s.downcase.start_with?('en')
  doc.content = FadongExternalLinks.apply(doc.content, english ? 'en' : 'ko')
end
