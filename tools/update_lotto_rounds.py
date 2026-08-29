#!/usr/bin/env python3
"""kr645_rounds.csv에 신규 회차를 append한다 (update-lotto-rounds 액션이 실행).

데이터 출처는 동행복권 데이터의 GitHub Pages 미러(smok95.github.io/lotto).
CSV 마지막 줄의 회차 다음부터 순서대로 조회해, 404가 나올 때까지 이어붙인다.
표준 라이브러리만 사용 — 러너와 로컬 어디서든 python3 하나로 돈다.
"""
import json
import sys
import urllib.error
import urllib.request

MIRROR = "https://smok95.github.io/lotto/results/{}.json"
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else "kr645_rounds.csv"


def fetch_round(no: int):
    try:
        with urllib.request.urlopen(MIRROR.format(no), timeout=15) as res:
            data = json.load(res)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    numbers = data.get("numbers")
    date = str(data.get("date", ""))
    if data.get("draw_no") != no or not isinstance(numbers, list) or len(numbers) != 6:
        return None
    if not isinstance(data.get("bonus_no"), int):
        return None
    day = date.split("T")[0]
    if len(day) != 10:
        return None
    return f"{no},{','.join(str(n) for n in numbers)},{data['bonus_no']},{day}"


def main() -> None:
    with open(CSV_PATH, encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    last = int(lines[-1].split(",")[0])

    added = 0
    no = last + 1
    while True:
        line = fetch_round(no)
        if line is None:
            break
        lines.append(line)
        print(f"appended round {no}: {line}")
        added += 1
        no += 1

    if added:
        with open(CSV_PATH, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    print(f"added={added}")
    # 액션의 후속 스텝(커밋 여부 분기)이 읽는 출력
    github_output = __import__("os").environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"added={added}\n")


if __name__ == "__main__":
    main()
