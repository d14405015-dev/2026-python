"""
UVA 100 - The 3n + 1 problem

這個版本是「標準版」：
- 可讀性高
- 速度也不錯（使用記憶化，避免重複計算）

題目要求：
輸入多組 i, j，對每一組輸出：
i j max_cycle_length
其中 max_cycle_length 是區間 [min(i, j), max(i, j)] 內所有數字的最大 cycle length。
"""

from __future__ import annotations

import sys


def build_cycle_length_cache() -> dict[int, int]:
    """建立並回傳 cycle length 快取。

    為了加速，我們先放入已知基底：
    - 1 的 cycle length 為 1
    """
    return {1: 1}


def cycle_length(n: int, cache: dict[int, int]) -> int:
    """計算單一整數 n 的 cycle length（含起點與終點 1）。

    作法說明：
    1. 一路沿著 Collatz 規則往下走，直到遇到「快取中已知」的值。
    2. 回推整條路徑，把每個中間值的長度補回快取。

    這樣可以避免重複計算，大幅提升效能。
    """
    if n in cache:
        return cache[n]

    original_n = n
    path: list[int] = []

    # 先往下走，直到走到已知答案的節點。
    while n not in cache:
        path.append(n)
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

    # n 已經在 cache 中，代表目前有一個已知長度可當起點。
    length = cache[n]

    # 反向回推路徑，把每一個節點的長度寫回 cache。
    # reversed(path) 的第一個元素是最接近已知節點的那個數。
    for value in reversed(path):
        length += 1
        cache[value] = length

    return cache[original_n]


def max_cycle_length(i: int, j: int, cache: dict[int, int]) -> int:
    """回傳區間 [min(i, j), max(i, j)] 的最大 cycle length。"""
    start = min(i, j)
    end = max(i, j)

    best = 0
    for value in range(start, end + 1):
        current = cycle_length(value, cache)
        if current > best:
            best = current
    return best


def solve(data: str) -> str:
    """解析整份輸入，回傳完整輸出字串。"""
    cache = build_cycle_length_cache()
    output_lines: list[str] = []

    for raw_line in data.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        i_str, j_str = line.split()
        i = int(i_str)
        j = int(j_str)

        answer = max_cycle_length(i, j, cache)
        output_lines.append(f"{i} {j} {answer}")

    return "\n".join(output_lines)


def main() -> None:
    """程式進入點：讀 stdin，計算後輸出。"""
    input_data = sys.stdin.read()
    result = solve(input_data)
    if result:
        print(result)


if __name__ == "__main__":
    main()
