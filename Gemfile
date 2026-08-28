# frozen_string_literal: true

source "https://rubygems.org"

# ⚠️ 버전을 고정한다. _includes/_layouts 오버라이드 5개가 이 버전의 원본을
# 복사·수정한 것이라, 떠 있으면 상류 릴리즈만으로 사이트가 깨진다.
# 실제 사고(2026-08-29): `~> 7.2` 가 7.6.0 을 받아왔는데 7.6.0 에서
# post-description.html / no-linenos.html 이 제거돼 빌드가 실패했다.
# 올릴 때는 tools/theme-includes.txt 를 갱신하고 오버라이드를 재대조할 것.
gem "jekyll-theme-chirpy", "= 7.6.0"

gem "html-proofer", "~> 5.0", group: :test

platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

gem "wdm", "~> 0.2.0", :platforms => [:mingw, :x64_mingw, :mswin]
