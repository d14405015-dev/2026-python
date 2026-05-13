"""
========================================================
題目：UVA 10908 — Largest Square
來源：ZeroJudge a901
========================================================

【題目大意】
  給定一個 M×N 的字元網格與 Q 個查詢。
  每筆查詢給定中心點 (r, c)，找出以該點為中心、
  所有字元相同的最大正方形邊長（邊長必須為奇數）。

【數學公式】
  邊長 = 2h + 1，其中 h 為「半徑」（從中心往外擴張的層數）。
  從 h=0 開始逐層往外嘗試，每次檢查半徑 (h+1) 的正方形：
    - 若仍在網格範圍內，且所有格子字元與中心相同 → h += 1
    - 否則停止，回傳當前 2h+1

【時間複雜度】
  每筆查詢最多擴張 min(M,N)/2 層，每層掃描 O((2h+1)²) 個格子。
  整體：O(Q × M × N)，在 M,N≤100、Q<21 的限制下足夠快。
"""

import sys


def solve_query(grid: list[str], r: int, c: int) -> int:
    """
    找出以 (r, c) 為中心的最大相同字元正方形邊長。

    參數：
        grid (list[str])：M×N 字元網格
        r    (int)      ：中心列（0-based）
        c    (int)      ：中心行（0-based）
    回傳：
        int：最大邊長（奇數，最小為 1）
    """
    m = len(grid)        # 網格總行數
    n = len(grid[0])     # 網格總列數
    ch = grid[r][c]      # 中心格的字元，用來比對

    h = 0  # 目前成立的半徑，初始為 0（邊長 1）
    while True:
        nh = h + 1  # 嘗試下一層半徑
        # ── 邊界檢查：新的正方形是否仍在網格內 ──────
        if r - nh < 0 or r + nh >= m or c - nh < 0 or c + nh >= n:
            break  # 超出邊界，停止擴張
        # ── 字元一致性檢查：掃描整個 (2nh+1)×(2nh+1) 正方形 ──
        ok = all(
            grid[r + dr][c + dc] == ch
            for dr in range(-nh, nh + 1)
            for dc in range(-nh, nh + 1)
        )
        if not ok:
            break  # 有不同字元，停止擴張
        h = nh  # 擴張成功，記錄新半徑

    return 2 * h + 1  # 邊長 = 2h+1


def main():
    data = sys.stdin.read().split("\n")
    idx = 0
    t = int(data[idx]); idx += 1  # 測試案例數 T

    for _ in range(t):
        m, n, q = map(int, data[idx].split()); idx += 1  # 行數、列數、查詢數
        grid = []
        for _ in range(m):
            grid.append(data[idx]); idx += 1   # 讀入每行字元
        # 輸出標頭行
        print(f"{m} {n} {q}")
        for _ in range(q):
            r, c = map(int, data[idx].split()); idx += 1  # 查詢中心
            print(solve_query(grid, r, c))


if __name__ == "__main__":
    main()
