# U6. defaultdict 為何比手動初始化乾淨（1.6）

# 匯入 defaultdict：當 key 不存在時可自動建立預設值
from collections import defaultdict

# (鍵, 值) 範例資料，目標是把相同鍵的值收集成 list
pairs = [('a', 1), ('a', 2), ('b', 3)]

# 手動版：一直判斷 key 是否存在
d = {}
for k, v in pairs:
    # 首次看到 key 時要先建立空 list
    if k not in d:
        d[k] = []
    # 再把值加到對應 list
    d[k].append(v)

# defaultdict：省掉初始化分支
# 傳入 list 工廠函式，缺少 key 時會自動建立 []
d2 = defaultdict(list)
for k, v in pairs:
    # 可直接 append，程式更精簡
    d2[k].append(v)
