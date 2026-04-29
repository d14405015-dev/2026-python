"""
UVA 10268（依目前題目敘述）- Easy 版本

題意簡化：
- 有 k 顆相同水球、n 層樓。
- 想知道最糟情況下，至少要丟幾次，才能保證找出「最早會破的樓層」。
- 如果答案超過 63，輸出固定句子：More than 63 trials needed.

這題最容易背的做法不是直接想「第幾層丟」，
而是改想：

dp[m][e] = 在最多丟 m 次、手上有 e 顆球時，最多能測出幾層樓。

轉移公式：
dp[m][e] = dp[m - 1][e - 1] + dp[m - 1][e] + 1

原因：
- 這次從某一層丟下去。
- 如果破了，下面還能測 dp[m - 1][e - 1] 層。
- 如果沒破，上面還能測 dp[m - 1][e] 層。
- 再加上現在測的這一層，所以 +1。

只要找到最小的 m，使 dp[m][k] >= n 就是答案。
"""

from __future__ import annotations

import sys


LIMIT = 63


def min_trials(eggs: int, floors: int) -> str:
    """回傳單筆測資的答案字串。"""
    if floors == 0:
        return "0"

    # dp[e] 代表目前這個丟球次數下，e 顆球最多能測幾層。
    dp = [0] * (eggs + 1)

    for moves in range(1, LIMIT + 1):
        # 要從大到小更新，避免本輪資料蓋掉上一輪還要用的值。
        for egg in range(eggs, 0, -1):
            dp[egg] = dp[egg] + dp[egg - 1] + 1

        if dp[eggs] >= floors:
            return str(moves)

    return "More than 63 trials needed."


def solve(data: str) -> str:
    """讀到 k=0 為止，逐筆輸出答案。"""
    tokens = list(map(int, data.split()))
    out_lines = []

    index = 0
    while index + 1 < len(tokens):
        eggs = tokens[index]
        floors = tokens[index + 1]
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