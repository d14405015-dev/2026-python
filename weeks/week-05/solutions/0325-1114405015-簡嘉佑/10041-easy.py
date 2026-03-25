# UVA 10041 - 簡單版（好記版）
# 題目要找一個門牌位置，讓「到所有親戚家的距離總和」最小。
# 想法：把地址排序後，選中間那個地址（中位數）當作新家，
# 距離總和會最小。
#
# 為什麼是中位數？
# - 若住址往左移，左邊親戚更近、右邊親戚更遠；
# - 若住址往右移，右邊親戚更近、左邊親戚更遠；
# - 在中間位置時，兩邊拉扯最平衡，因此總距離最小。

import sys

# 讀取整份輸入：
# 例如輸入可能長這樣
# 2
# 2 2 4
# 3 2 4 6
#
# 用 split() 後會變成字串陣列，再 map(int, ...) 轉成整數陣列。
data = list(map(int, sys.stdin.read().split()))

# 若沒有輸入，直接結束。
if not data:
    raise SystemExit

t = data[0]  # 第一個數字是測試資料組數 T
idx = 1  # 指向目前讀到 data 的哪個位置
ans = []  # 收集每組答案（最後一次輸出）

for _ in range(t):
    # 每組格式：r s1 s2 ... sr
    # 先讀 r（親戚數量）
    r = data[idx]
    idx += 1

    # 讀出接下來的 r 個門牌號碼
    houses = data[idx : idx + r]
    idx += r

    # 排序後取中位數（r // 2）
    # r 為奇數：唯一中位數
    # r 為偶數：左右中位數都可達到最小總距離，這裡取右中位數
    houses.sort()
    mid = houses[r // 2]

    # 計算此組的最小總距離：sum(|si - mid|)
    total = 0
    for x in houses:
        total += abs(x - mid)

    # 轉成字串先存起來，最後用換行一次輸出
    ans.append(str(total))

# 題目要求每組答案各佔一行
print("\n".join(ans))
