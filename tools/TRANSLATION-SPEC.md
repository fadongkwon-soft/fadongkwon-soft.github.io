# 영문판 작성 규격 (fadongkwon.com)

한국어 `_posts/<date>-<slug>.md` 에 대응하는 영문판을 `_en_posts/<같은 파일명>.md` 로 만든다.
목적은 **글로벌 검색 유입**이다. 직역이 아니라 "원래 영어로 쓴 글"로 읽혀야 한다.

## 절대 규칙

1. **파일명은 한국어 원문과 완전히 동일**하게 `_en_posts/` 에 둔다. 날짜 접두어 포함.
2. **링크(`href`)와 이미지 경로는 한국어 원문 그대로 둔다.** `/posts/...` → `/en/posts/...`
   재작성은 `tools/i18n.py fixup` 이 기계적으로 처리한다. 손으로 고치지 말 것.
3. **`{% include tarot-app-banner.html %}` 도 그대로 둔다.** 스크립트가 영문판으로 바꾼다.
4. **kramdown 속성 블록을 절대 지우지 말 것**: `{: w="300" }`, `{: .prompt-warning }`,
   `{: .prompt-tip }`, `{: .normal}`, `{: width="350" .normal}` 등.
5. 이미지 바로 아래의 `_기울임 캡션_` 줄은 Chirpy 가 figcaption 으로 렌더한다. 형태를 유지하고 내용만 번역.
6. **섹션을 추가하거나 빼지 말 것.** 제목 계층(`##`, `###`)과 순서, 표 구조, 목록 구조를 그대로 유지.
7. 섹션 제목의 이모지는 유지한다 (`### 💕 연애` → `### 💕 Love`).
8. `{% include embed/youtube.html id='...' %}` 는 그대로 둔다.

## front matter

작성할 키는 **`title`, `description`, 그리고 원문에 `image:` 블록이 있으면 `image:`** 뿐이다.
`date`, `categories`, `permalink`, `alt_url`, `card_name` 은 스크립트가 한국어 원문 기준으로
채우므로 쓰지 않는다. `tags` 는 영문 아카이브 페이지가 없어 링크가 깨지므로 쓰지 않는다.

```yaml
---
title: The Fool Tarot Card Meaning — Upright, Reversed, Love, Career & Money
description: What the Fool card means upright and reversed, the symbols in the picture, and how it reads for love, career, money and study.
image:
  path: /assets/img/tarot/feature_major_00_fool.jpg
  alt: The Fool tarot card
---
```

- `image.path` 는 **한국어 원문과 똑같은 파일 경로**. `alt` 만 영어로.
- `title`: 영문 검색어를 겨냥한다. 50~65자 권장. 한국어처럼 em dash(`—`)로 부제를 붙여도 좋다.
  키워드를 앞에 둔다 (`The Fool Tarot Card Meaning — ...`).
- `description`: 한 문장, 110~155자. 검색결과 스니펫에 그대로 나온다고 생각하고 쓴다.
- 콜론(`:`)이 들어가면 YAML 이 깨지므로 값에 `:` 를 쓰지 말거나 따옴표로 감싼다.

## 문체

- 1인칭, 담백하고 단정한 문장. 한국어 원문의 목소리를 그대로 옮긴다.
- 과장된 마케팅 어투 금지. "amazing", "revolutionary", "game-changing" 같은 말 쓰지 않는다.
- 문장을 통째로 재구성해도 좋다. 어색한 직역보다 자연스러운 영어가 우선이다.
- 정보(숫자, 날짜, 카드 키워드, 제도 이름)는 절대 바꾸지 않는다.
- 영국식/미국식은 미국식으로 통일.

## 용어집 (반드시 이대로)

| 한국어 | English |
| --- | --- |
| 타로 운세 (앱) | Tarot Fortune |
| 운세 타로핑 (앱) | Tarot Ping |
| 한글 몬스터 | Hangul Monsters |
| 수학 몬스터 | Math Monsters |
| 간호조무사 모의고사 | Nursing Assistant Mock Exam |
| 반응속도 챌린지 | Reaction Challenge |
| 기억력 카드 | Memory Cards |
| 병 돌리기 | Spin the Bottle |
| 주스 스피너 | Juice Spinner |
| 사주로또 | Saju Lotto |
| 앱인토스 / 토스 미니앱 | Apps in Toss / Toss mini app |
| 파동권소프트 | Fadongkwon Soft |
| 정방향 / 역방향 | upright / reversed |
| 메이저 아르카나 / 마이너 아르카나 | Major Arcana / Minor Arcana |
| 완드 / 컵 / 소드 / 펜타클 | Wands / Cups / Swords / Pentacles |
| 에이스 / 시종 / 기사 / 여왕 / 왕 | Ace / Page / Knight / Queen / King |
| 상황별 해석 | Readings by situation |
| 연애 / 직장·커리어 / 금전 / 학업·시험 | Love / Career / Money / Study & Exams |
| 상징 읽기 | Reading the symbols |
| 오늘 이 카드를 뽑았다면 | If you drew this card today |
| 함께 보면 좋은 카드 | Cards to read alongside |
| 카드 기본 정보 | Card at a glance |

- 한국 고유 제도·기관명은 영문 설명 + 필요하면 한글 병기 (`the Korean History Proficiency Test (한국사능력검정시험)`).
- 타로 카드 글에는 한글이 나올 이유가 없다. 카드명은 영문명만 쓴다.

## 검증

작성 후 저장소 루트에서:

```bash
python tools/i18n.py fixup && python tools/i18n.py verify
```

`fixup` 이 링크·front matter 를 정규화하고, `verify` 가 깨진 내부 링크와 누락 키를 잡는다.
