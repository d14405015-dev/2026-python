# U3. deque(maxlen=N) 為何能保留最後 N 筆（1.3）

# 匯入雙端佇列 deque
from collections import deque

# 設定最大長度為 3，超過時會自動丟棄最舊元素
q = deque(maxlen=3)
# 依序加入 1 到 5
for i in [1, 2, 3, 4, 5]:
    # 當容量已滿，再 append 新值時，左側舊值會被移除
    q.append(i)
# 結果只剩 [3, 4, 5]
