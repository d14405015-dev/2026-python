# U5. 優先佇列為何要加 index（1.5）

# 匯入 heapq（最小堆）來實作優先佇列
import heapq

# 佇列中要存放的資料物件
class Item:
    def __init__(self, name):
    # 紀錄項目名稱
        self.name = name

# 優先佇列容器（底層是 list）
pq = []
# 若只放 (priority, item)，同 priority 會比較 item，Item 不支援 < 會炸
# heapq.heappush(pq, (-1, Item('a')))
# heapq.heappush(pq, (-1, Item('b')))  # TypeError

# 正解：加 index 作為第二排序鍵，避免直接比較 item
# 同優先度時會比 index，確保可比較且順序穩定
idx = 0
heapq.heappush(pq, (-1, idx, Item('a'))); idx += 1
heapq.heappush(pq, (-1, idx, Item('b'))); idx += 1
