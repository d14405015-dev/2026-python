"""UVA 11417 - GCD（-easy 版本）

好記版本重點：
- 完全照題目定義做兩層迴圈。
- 對每個 N，直接把所有 1 <= i < j <= N 的 gcd(i, j) 相加。
- 這版程式非常直覺，最適合初學時記憶邏輯。
"""

from __future__ import annotations

from math import gcd


def gcd_sum_direct(n: int) -> int:
    """依定義直接計算單一 N 的答案。"""
    total = 0
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total += gcd(i, j)
    return total


def solve(data: str) -> str:
    """逐行讀取 N，遇到 0 停止。"""
    out = []
    for line in data.splitlines():
        line = line.strip()
        if not line:
            continue

        n = int(line)
        if n == 0:
            break

        out.append(str(gcd_sum_direct(n)))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
