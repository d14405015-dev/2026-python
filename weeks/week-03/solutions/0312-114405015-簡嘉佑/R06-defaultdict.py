# R6. 多值字典 defaultdict / setdefault（1.6）

# defaultdict 是 dict 的子類別。
# 當你存取不存在的 key 時，會自動建立預設值，
# 避免每次都先寫 if key not in d: ...
from collections import defaultdict


# 範例 1：每個 key 對應「多個值（list）」
# defaultdict(list) 代表新 key 的預設值是空 list []
d = defaultdict(list)

# 第一次存取 d['a'] 時，會自動建立 d['a'] = []
# 接著 append 進去，所以最後 d['a'] 會是 [1, 2]
d['a'].append(1); d['a'].append(2)


# 範例 2：每個 key 對應「不重複值（set）」
# defaultdict(set) 代表新 key 的預設值是空 set()
d = defaultdict(set)

# set 的特性是自動去重複，
# 所以適合收集不重複標籤、ID、關聯項目
d['a'].add(1); d['a'].add(2)


# 範例 3：不用 defaultdict，也可用一般 dict + setdefault
d = {}

# setdefault('a', []) 的意思：
# - 若 'a' 不存在，就先建立 d['a'] = []
# - 若 'a' 已存在，就回傳現有 d['a']
# 回傳值是一個 list，因此可以直接 append(1)
d.setdefault('a', []).append(1)
