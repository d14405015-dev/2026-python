# R4. heapq 取 Top-N（1.4）

# `heapq` 是 Python 標準庫中的「最小堆（min-heap）」工具。
# 常見用途：
# - 快速找出前 N 大 / 前 N 小
# - 維護動態優先序資料
import heapq


# 一組數值資料
nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]

# 取出「最大的 3 個值」
# 回傳結果是 list，通常為由大到小，例如 [42, 37, 23]
heapq.nlargest(3, nums)

# 取出「最小的 3 個值」
# 通常結果例如 [-4, 1, 2]
heapq.nsmallest(3, nums)


# 也可以對「複雜物件」取 Top-N，只要提供 key 告訴它比較依據。
portfolio = [
    {'name': 'IBM', 'shares': 100, 'price': 91.1},
    {'name': 'AAPL', 'shares': 50, 'price': 543.22},
]

# 取出 price 最小的 1 筆（最便宜的一筆）
# key=lambda s: s['price'] 表示比較依據是每筆資料的 price 欄位
heapq.nsmallest(1, portfolio, key=lambda s: s['price'])


# 若你要反覆 pop 最小值，先把資料轉成 heap 會更有效率。
heap = list(nums)

# 原地把 list 轉成最小堆結構（不是完整排序）
# 重點：heap[0] 會是目前最小值
heapq.heapify(heap)

# 取出並移除最小值（min-heap 特性）
heapq.heappop(heap)
