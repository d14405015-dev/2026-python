"""UVA 11461 - Square Numbers

標準版解法：
- 區間 [a, b] 的完全平方數個數
  = floor(sqrt(b)) - ceil(sqrt(a)) + 1（若結果為正）
- 使用整數平方根可避免浮點誤差。
"""

from __future__ import annotations

from math import isqrt


def count_squares(a: int, b: int) -> int:
    """計算閉區間 [a, b] 內完全平方數的個數。"""
    left = isqrt(a)
    if left * left < a:
        left += 1

    right = isqrt(b)

    return max(0, right - left + 1)


def solve(data: str) -> str:
    """處理多行 a b，遇到 0 0 結束。"""
    out = []

    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        out.append(str(count_squares(a, b)))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
