# U4. heap 為何能高效拿 Top-N（1.4）

# 匯入 heapq：Python 內建最小堆工具
import heapq

# 原始資料
nums = [5, 1, 9, 2]
# 複製一份資料，避免直接改動原清單
h = nums[:]
# 原地轉成最小堆結構
heapq.heapify(h)
# h[0] 永遠是最小值（這是 heap 的核心性質）
# 從堆中彈出目前最小值，並維持堆性質
m = heapq.heappop(h)  # 每次 pop 都拿到目前最小
