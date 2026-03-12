# R5. 優先佇列 PriorityQueue（1.5）

# 這個範例用 heapq 實作「優先佇列」。
#
# 重要觀念：
# - heapq 是「最小堆」：數值越小，越先被 pop。
# - 但很多情境想要「priority 越大越先出」，
#   所以會把 priority 取負號（-priority）來反轉順序。
import heapq


class PriorityQueue:
    def __init__(self):
        # _queue: 真正存放堆資料的 list
        # 每筆元素格式為：(-priority, index, item)
        self._queue = []

        # _index: 遞增計數器，用來解決「同優先序」時的排序問題
        # 也能保持先進先出（FIFO）的穩定性
        self._index = 0

    def push(self, item, priority):
        # heappush 會依 tuple 逐欄位比較：
        # 1) 先比 -priority（數值越小，代表原 priority 越大）
        # 2) 若同優先序，再比 index（較早進來者先出）
        # 3) item 只作為攜帶資料，不參與主要優先排序
        heapq.heappush(self._queue, (-priority, self._index, item))

        # 每 push 一次就遞增，確保每筆資料 index 唯一
        self._index += 1

    def pop(self):
        # heappop 會取出「目前最小」tuple，
        # 也就是原始 priority 最大、且最早進入的那筆。
        # 回傳 tuple 的最後一欄 item（實際資料）給呼叫者。
        return heapq.heappop(self._queue)[-1]
