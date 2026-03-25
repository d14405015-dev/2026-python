# UVA 10050 - Hartals（簡單好記版）
#
# 題目要我們計算：在 N 天內，因為政黨罷會而損失了幾個「工作天」。
# 注意兩個重點：
# 1) 同一天若有多個政黨罷會，只能算 1 天。
# 2) 星期五與星期六是假日，不算工作天損失。
#
# 好記做法：
# - 準備一個集合 lost_days，專門記錄「真的損失的工作天」。
# - 對每個政黨週期 h，從第 h 天開始，每隔 h 天走一次。
# - 若該天不是週五/週六，就放進集合。
# - 最後集合大小就是答案。

import sys


# 一次讀入全部資料，依空白切割成整數。
nums = list(map(int, sys.stdin.read().split()))

# 沒有輸入就直接結束。
if not nums:
    raise SystemExit

# 第一個數字是測資筆數 T。
t = nums[0]
idx = 1  # 讀取指標，指出目前讀到 nums 的位置
answers = []

for _ in range(t):
    # 每組測資先讀 N（總天數）。
    n = nums[idx]
    idx += 1

    # 再讀 P（政黨數）。
    p = nums[idx]
    idx += 1

    # 接著讀 P 個 hartal 參數 h。
    hs = nums[idx : idx + p]
    idx += p

    # 用集合避免同一天被重複計算。
    lost_days = set()

    for h in hs:
        # 第一次罷會在第 h 天，之後每隔 h 天再罷會。
        day = h
        while day <= n:
            # 題目設定第 1 天是星期日，所以：
            # day % 7 == 6 -> 星期五（假日）
            # day % 7 == 0 -> 星期六（假日）
            # 假日不算損失工作天。
            if day % 7 not in (6, 0):
                lost_days.add(day)
            day += h

    # 這組答案就是集合大小。
    answers.append(str(len(lost_days)))

# 每組答案輸出一行。
print("\n".join(answers))
