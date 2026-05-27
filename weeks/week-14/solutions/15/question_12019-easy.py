"""UVA 12019 - Doom's Day Algorithm（-easy 版本）

好記版本重點：
- 直接使用 Python 內建 datetime 幫我們算星期。
- 思路最短、最容易記憶。
"""

from __future__ import annotations

from datetime import date


def weekday_2012_easy(month: int, day: int) -> str:
    """利用 datetime.date 直接取得星期英文名。"""
    return date(2012, month, day).strftime("%A")


def solve(data: str) -> str:
    """依題目格式讀取測資並輸出答案。"""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    t = int(lines[0])
    out = []

    for i in range(1, t + 1):
        m, d = map(int, lines[i].split())
        out.append(weekday_2012_easy(m, d))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
