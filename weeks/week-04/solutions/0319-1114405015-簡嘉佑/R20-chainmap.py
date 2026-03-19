# R20. ChainMap 合併映射（1.20）

# 匯入 ChainMap：可把多個 dict 視為單一映射來查找
from collections import ChainMap

# 第一層映射
a = {'x': 1, 'z': 3}
# 第二層映射
b = {'y': 2, 'z': 4}
# 建立 ChainMap，查找時會依序先看 a，再看 b
c = ChainMap(a, b)

# 直接取得 x（來自 a）
c['x']
# z 同時存在於 a 與 b，會先取到較前面的 a['z']
c['z']  # 取到 a 的 z
