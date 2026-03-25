# UVA 10055 - 簡單好記版（去掉 Fenwick Tree，改用直接計算）
#
# ====== 題目核心觀念 ======
# 有 N 個函數，一開始全是增函數。
# 操作有兩種：
#   v=1 i   → 把 f_i 的增減性反轉（增↔減）
#   v=2 L R → 查詢複合函數 f_L(f_L+1(...f_R(x)...)) 是增還是減
#
# 關鍵數學性質：
#   - 兩個增函數複合 → 增函數
#   - 一增一減複合   → 減函數
#   - 兩個減函數複合 → 增函數
#   規律：只要「減函數的個數」是偶數 → 整體增；奇數 → 整體減。
#
# 好記做法：
#   - 用 state[i] 記錄每個函數是增(0)還是減(1)
#   - v=1 就對 state[i] 做 XOR 1 反轉
#   - v=2 就對 state[l..r] 求和，判斷奇偶
#
# 時間複雜度：O(N) 每次查詢（若測資很大需改用 Fenwick Tree）

import sys

# 把所有輸入一次讀進來，轉成整數陣列方便存取。
nums = list(map(int, sys.stdin.read().split()))
if not nums:
    raise SystemExit

# 第一個數字 N = 函數總數，第二個數字 Q = 操作總數。
n = nums[0]
q = nums[1]
idx = 2

# state 陣列，索引 1~N 對應函數 f1~fN。
# 初始全為 0（增函數），1 代表減函數。
state = [0] * (n + 1)

ans = []

for _ in range(q):
    v = nums[idx]
    idx += 1

    if v == 1:
        # ── 操作 v=1：反轉 f_i 的增減性 ──
        # 讀取目標函數的編號 i。
        i = nums[idx]
        idx += 1

        # XOR 1 可以把 0 變 1、把 1 變 0，是最簡潔的反轉寫法。
        state[i] ^= 1

    else:
        # ── 操作 v=2：查詢區間 [l, r] 複合後的增減性 ──
        l = nums[idx]
        idx += 1
        r = nums[idx]
        idx += 1

        # 直接對 state[l..r] 求總和，計算「減函數個數」。
        # sum() 的切片寫法：state[l:r+1]
        # 偶數 → 增函數，輸出 0；奇數 → 減函數，輸出 1。
        dec_count = sum(state[l : r + 1])
        ans.append(str(dec_count % 2))

# 每組查詢答案各一行。
print("\n".join(ans))
