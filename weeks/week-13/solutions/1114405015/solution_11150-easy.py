"""UVA 11150 - 過橋最少踩石子數（easy 版本）

設計目標：
1. 寫法直觀、步驟固定，方便記憶。
2. 支援線上評測輸入格式，也提供可測試的函式介面。

核心觀念（容易記）：
1. 青蛙每步可跳 S~T。
2. 位置太大（L 可到 1e9）不能直接做完整 DP。
3. 先把「石子位置與位置差」做壓縮，保留會影響結果的區段。
4. 在壓縮後的小範圍上做最短路/DP，求最少踩石子。

為什麼能壓縮：
- 每一步最多只會跳 T（T <= 10）。
- 當兩顆石子之間距離很大時，中間的很多空位置對答案沒有額外資訊，
  只需要保留足夠長度讓跳躍關係成立即可。
- 常見做法把間隔截斷在固定上限（這裡用 100），可安全且高效。
"""

from __future__ import annotations

import sys
from typing import List, Sequence


INF = 10**9
COMPRESS_GAP_CAP = 100


def compress_positions(L: int, stones: Sequence[int], cap: int = COMPRESS_GAP_CAP) -> tuple[int, List[int]]:
    """將原始座標壓縮成較小座標。

    回傳：
    - Lc: 壓縮後的終點座標
    - compressed_stones: 壓縮後石子座標（遞增）

    方法說明：
    - 依序看相鄰關鍵點（前一點 -> 下一顆石子 -> 最後到 L）。
    - 若距離很大，只保留 cap 的有效長度，其餘區段可視為重複狀態。
    """
    sorted_stones = sorted(stones)

    compressed_stones: List[int] = []
    prev_original = 0
    current_compressed = 0

    for pos in sorted_stones:
        gap = pos - prev_original
        current_compressed += min(gap, cap)
        compressed_stones.append(current_compressed)
        prev_original = pos

    # 把最後一顆石子到終點 L 的區間也納入壓縮。
    current_compressed += min(L - prev_original, cap)
    Lc = current_compressed

    return Lc, compressed_stones


def min_stones(L: int, S: int, T: int, stones: Sequence[int]) -> int:
    """計算青蛙過河最少踩到幾顆石子。"""
    if L <= 0:
        return 0

    # 特例：S == T 時，跳法固定，直接看會落在哪些點即可。
    if S == T:
        step = S
        stone_set = set(stones)
        pos = step
        count = 0
        while pos < L:
            if pos in stone_set:
                count += 1
            pos += step
        return count

    Lc, compressed_stones = compress_positions(L, stones)
    stone_set = set(compressed_stones)

    # dp[i] = 到達壓縮座標 i 的最少踩石子數
    # 狀態範圍開到 Lc + T，因為跳到或超過終點就算成功。
    max_pos = Lc + T
    dp = [INF] * (max_pos + 1)
    dp[0] = 0

    for i in range(max_pos + 1):
        if dp[i] == INF:
            continue
        if i >= Lc:
            # 已經到或超過終點，不需要再延伸。
            continue

        for step in range(S, T + 1):
            nxt = i + step
            if nxt > max_pos:
                continue

            # 只有在橋上區間（<= Lc）且剛好落在石子位置才加 1。
            add = 1 if (nxt <= Lc and nxt in stone_set) else 0
            candidate = dp[i] + add
            if candidate < dp[nxt]:
                dp[nxt] = candidate

    return min(dp[Lc : Lc + T + 1])


def solve(input_text: str) -> str:
    """處理單筆輸入並輸出答案字串。"""
    tokens = list(map(int, input_text.split()))
    if not tokens:
        return ""

    idx = 0
    L = tokens[idx]
    idx += 1

    S = tokens[idx]
    T = tokens[idx + 1]
    M = tokens[idx + 2]
    idx += 3

    stones = tokens[idx : idx + M]

    ans = min_stones(L, S, T, stones)
    return str(ans)


def main() -> None:
    """線上評測入口。"""
    data = sys.stdin.read()
    output = solve(data)
    if output:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
