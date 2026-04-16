import sys


def solve(data):
    """炮兵部署問題 — bitmask DP（容易記憶版）

    記憶口訣：「地形過濾 → 預建合法列 → 兩列狀態壓縮 DP」

    步驟一：把每列地形轉成位元遮罩（bit = 1 代表平原）。
    步驟二：列出所有「橫向不衝突」的位元排列，再用地形過濾掉山地位置。
    步驟三：逐列做 DP，記錄「前兩列的排列組合」能達到的最大炮兵數。
    步驟四：答案就是所有最終狀態中的最大值。

    為什麼只需要記前兩列？
    因為炮兵的縱向攻擊範圍是上下各兩格，
    所以第 i 列的炮兵只可能和第 i-1 列、第 i-2 列的炮兵互相攻擊。
    更早的列已經不會影響當前列的合法性。
    """
    lines = data.strip().split("\n")
    n, m = map(int, lines[0].split())
    grid = [lines[i + 1].strip() for i in range(n)]

    # ---------- 步驟一：把地形轉成位元遮罩 ----------
    # terrain[i] 的第 j 個 bit 為 1，代表第 i 列第 j 欄是平原（可以放炮兵）。
    terrain = []
    for row in grid:
        t = 0
        for j, ch in enumerate(row):
            if ch == "P":
                t |= (1 << j)
        terrain.append(t)

    # ---------- 步驟二：預建合法排列 ----------
    # 「橫向合法」的定義：同一列中任意兩個炮兵欄位距離必須 > 2。
    # 位元技巧：mask & (mask >> 1) 有交集 → 存在距離 1 的炮兵對。
    #           mask & (mask >> 2) 有交集 → 存在距離 2 的炮兵對。
    def ok_row(mask):
        return not (mask & (mask >> 1)) and not (mask & (mask >> 2))

    base_masks = [m_val for m_val in range(1 << m) if ok_row(m_val)]

    # 每一列合法排列 = 橫向合法 且 不踏到山地。
    valid = [
        [mask for mask in base_masks if (mask & terrain[r]) == mask]
        for r in range(n)
    ]

    # ---------- 步驟三：逐列 DP ----------
    # dp 是一個字典：key = (上上列排列, 上列排列)，value = 目前最多炮兵數。
    # 初始：第 0 列處理，虛構一個「不存在的」上上列（值為 0）。
    dp = {(0, mask): bin(mask).count("1") for mask in valid[0]}

    for r in range(1, n):
        next_dp = {}
        for curr in valid[r]:
            soldiers = bin(curr).count("1")
            for (prev2, prev1), count in dp.items():
                # 縱向衝突：curr 和上一列（距離 1）有共同欄位 → 攻擊到 → 跳過。
                if curr & prev1:
                    continue
                # 縱向衝突：curr 和上上列（距離 2）有共同欄位 → 攻擊到 → 跳過。
                if curr & prev2:
                    continue
                key = (prev1, curr)
                new_count = count + soldiers
                if next_dp.get(key, -1) < new_count:
                    next_dp[key] = new_count
        dp = next_dp

    # ---------- 步驟四：取最大值 ----------
    return str(max(dp.values())) + "\n" if dp else "0\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
