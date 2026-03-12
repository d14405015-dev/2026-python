# R3. deque 保留最後 N 筆（1.3）

# deque（double-ended queue）是「雙端佇列」：
# - 可以從左邊或右邊快速加入/移除元素
# - 很適合做固定長度緩衝區、滑動視窗、最近 N 筆資料
from collections import deque


# 範例 1：設定 maxlen=3，表示最多只保留 3 筆
q = deque(maxlen=3)

# 依序加入 1, 2, 3，內容變成：deque([1, 2, 3], maxlen=3)
q.append(1); q.append(2); q.append(3)

# 再加入 4 時，因為容量已滿，會「自動淘汰最舊」的元素 1
# 最終內容：deque([2, 3, 4], maxlen=3)
q.append(4)  # 自動丟掉最舊的 1


# 範例 2：不設定 maxlen，deque 長度可持續成長
q = deque()

# append(1)：從右邊加入 1 -> deque([1])
# appendleft(2)：從左邊加入 2 -> deque([2, 1])
q.append(1); q.appendleft(2)

# pop()：從右邊移除並回傳元素（這裡會拿到 1）
# popleft()：從左邊移除並回傳元素（這裡會拿到 2）
# 兩次操作後佇列會變空
q.pop(); q.popleft()
