import sys


def no_horizontal_conflict(mask, m):
    """判斷同一列的炮兵排列是否符合橫向攻擊規則。

    炮兵的攻擊範圍向左右各延伸兩格，
    因此同一列中任意兩個炮兵的欄位距離必須大於 2。
    換成位元運算：mask 和 (mask >> 1) 有交集代表距離為 1，
    mask 和 (mask >> 2) 有交集代表距離為 2，兩者都不能有交集。
    """
    return not (mask & (mask >> 1)) and not (mask & (mask >> 2))


def fits_terrain(mask, terrain_mask):
    """確認炮兵排列只落在平原格（P）上。

    terrain_mask 的第 j 位為 1 表示第 j 欄是平原，
    炮兵排列 mask 所有設定位元都必須對應到平原。
    """
    return (mask & terrain_mask) == mask


def popcount(x):
    """計算整數 x 中 1 的個數，代表本列部署的炮兵數量。"""
    return bin(x).count("1")


def solve(data):
    """讀取輸入並回傳最大炮兵部署數量。

    演算法概念：
    由於 M ≤ 10，可以用 bitmask 表示每一列的炮兵排列方式。
    炮兵縱向攻擊範圍為上下各兩列，
    所以推進到第 i 列時，只需追蹤第 i-1 列（prev1）和第 i-2 列（prev2）的狀態。

    DP 定義：
    dp[(prev2_mask, prev1_mask)] = 從第 0 列到目前為止的最大炮兵數量，
    其中 prev1_mask 是上一列的排列，prev2_mask 是上上一列的排列。

    轉移條件：
    當前列的 curr_mask 必須滿足：
    1. 不和 prev1 在同欄位（縱向距離 1，互相攻擊）
    2. 不和 prev2 在同欄位（縱向距離 2，互相攻擊）
    """
    lines = data.strip().split("\n")
    n, m = map(int, lines[0].split())
    grid = [lines[i + 1].strip() for i in range(n)]

    # 把每列地形轉成 bitmask：bit j = 1 代表第 j 欄是平原。
    terrain = []
    for row in grid:
        mask = 0
        for j, ch in enumerate(row):
            if ch == "P":
                mask |= (1 << j)
        terrain.append(mask)

    # 預先產生所有「橫向不衝突」的 bitmask。
    all_valid_masks = [
        mask for mask in range(1 << m)
        if no_horizontal_conflict(mask, m)
    ]

    # 針對每一列過濾出合乎地形的 bitmask。
    row_valid_masks = [
        [mask for mask in all_valid_masks if fits_terrain(mask, terrain[row_idx])]
        for row_idx in range(n)
    ]

    # DP 初始化：第 0 列，prev2 = 0（不存在的列用 0 代替），prev1 = 本列排列。
    dp = {}
    for mask in row_valid_masks[0]:
        key = (0, mask)
        dp[key] = popcount(mask)

    # 逐列推進 DP。
    for row_idx in range(1, n):
        new_dp = {}
        for curr in row_valid_masks[row_idx]:
            curr_soldiers = popcount(curr)
            for (prev2, prev1), total_so_far in dp.items():
                # 縱向衝突檢查：curr 和 prev1 有同欄代表距離 1，互相攻擊。
                if curr & prev1:
                    continue
                # 縱向衝突檢查：curr 和 prev2 有同欄代表距離 2，互相攻擊。
                if curr & prev2:
                    continue
                new_total = total_so_far + curr_soldiers
                new_key = (prev1, curr)
                if new_dp.get(new_key, -1) < new_total:
                    new_dp[new_key] = new_total
        dp = new_dp

    return str(max(dp.values())) + "\n" if dp else "0\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
