"""
UVA 10268（依目前題目敘述）- Optimized 版本

優化重點：
1. 仍使用經典 dp[e] = 最多可測樓層數 的做法。
2. 每輪只更新到 min(eggs, moves)，因為球數超過丟球次數時沒有額外意義。
3. 每次更新時把值上限截到 floors，避免整數不必要變大。
"""

from __future__ import annotations

import sys


LIMIT = 63


def min_trials(eggs: int, floors: int) -> str:
    if floors == 0:
        return "0"

    usable_eggs = min(eggs, LIMIT)
    dp = [0] * (usable_eggs + 1)

    for moves in range(1, LIMIT + 1):
        upper_egg = min(usable_eggs, moves)
        for egg in range(upper_egg, 0, -1):
            dp[egg] = min(floors, dp[egg] + dp[egg - 1] + 1)
        if dp[upper_egg] >= floors:
            return str(moves)

    return "More than 63 trials needed."


def solve(data: str) -> str:
    values = list(map(int, data.split()))
    out_lines = []

    index = 0
    while index + 1 < len(values):
        eggs = values[index]
        floors = values[index + 1]
        index += 2

        if eggs == 0:
            break

        out_lines.append(min_trials(eggs, floors))

    return "\n".join(out_lines)


def main() -> None:
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()