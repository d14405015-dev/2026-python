"""UVA 11461 - Square Numbers（-easy 版本）

好記版本重點：
- 從 sqrt(a) 開始往上找，逐一檢查平方值是否 <= b。
- 實作非常直覺，易於初學者理解。
"""

from __future__ import annotations

from math import isqrt


def count_squares_easy(a: int, b: int) -> int:
    """以逐一列舉平方值的方式計數。"""
    start = isqrt(a)
    if start * start < a:
        start += 1

    cnt = 0
    x = start
    while x * x <= b:
        cnt += 1
        x += 1

    return cnt


def solve(data: str) -> str:
    out = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        out.append(str(count_squares_easy(a, b)))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
