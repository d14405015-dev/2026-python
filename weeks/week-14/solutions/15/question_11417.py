"""UVA 11417 - GCD

標準版解法：
- 題目需要對多個 N 計算 G(N) = sum(gcd(i, j))，其中 1 <= i < j <= N。
- 因為 N 最大只有 500，可以先把 1..500 的答案全部預先算好，
  後續查表即可，速度快且實作直觀。
"""

from __future__ import annotations

from math import gcd

MAX_N = 500


def build_prefix_gcd_sums(limit: int = MAX_N) -> list[int]:
    """預先建立 G(0..limit) 的前綴答案表。

    prefix[n] 代表題目要求的 G(n)。
    計算方式：
    - 先求固定右端點 j = n 時，sum_{i=1..n-1} gcd(i, n)
    - 再加到 prefix[n - 1] 上得到 prefix[n]
    """
    prefix = [0] * (limit + 1)

    for n in range(2, limit + 1):
        pair_sum_for_n = 0
        for i in range(1, n):
            pair_sum_for_n += gcd(i, n)
        prefix[n] = prefix[n - 1] + pair_sum_for_n

    return prefix


def solve(data: str) -> str:
    """讀入多筆 N，輸出每筆對應的 G(N)。"""
    nums = [int(line.strip()) for line in data.splitlines() if line.strip()]
    prefix = build_prefix_gcd_sums(MAX_N)

    out = []
    for n in nums:
        if n == 0:
            break
        out.append(str(prefix[n]))

    return "\n".join(out)


if __name__ == "__main__":
    import sys

    print(solve(sys.stdin.read()))
