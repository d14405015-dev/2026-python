"""
UVA 100 - The 3n + 1 problem（-easy 版本）

這個版本目標是「更好記、好手打」：
- 函式少
- 邏輯直線
- 仍然正確通過題目常見測資

記憶口訣：
1. 奇數 -> 3n + 1
2. 偶數 -> n // 2
3. 算到 1 為止，統計長度
4. 每一列輸出 i j 最大長度
"""

from __future__ import annotations

import sys


def collatz_len(n: int, memo: dict[int, int]) -> int:
    """回傳 n 的 cycle length。

    這裡也放一點點快取（memo），
    讓重複出現的數字不用每次重算。
    """
    if n in memo:
        return memo[n]

    seq: list[int] = []
    x = n

    # 一直推進，直到碰到已知長度的數字。
    while x not in memo:
        seq.append(x)
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1

    # 從已知答案往回補。
    length = memo[x]
    for value in reversed(seq):
        length += 1
        memo[value] = length

    return memo[n]


def main() -> None:
    """逐行讀入 i, j，逐行輸出答案。"""
    memo = {1: 1}
    lines = sys.stdin.read().splitlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        i_str, j_str = line.split()
        i = int(i_str)
        j = int(j_str)

        left = min(i, j)
        right = max(i, j)

        best = 0
        for value in range(left, right + 1):
            length = collatz_len(value, memo)
            if length > best:
                best = length

        print(i, j, best)


if __name__ == "__main__":
    main()
