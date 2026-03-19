# U7. OrderedDict 的取捨：保序但更吃記憶體（1.7）

# 匯入 OrderedDict：會依「插入順序」保存鍵的排列
from collections import OrderedDict

# 建立有序字典
d = OrderedDict()
# 先插入 foo
d['foo'] = 1
# 再插入 bar（迭代時會維持 foo -> bar 的順序）
d['bar'] = 2
# 你能解釋：為了維持插入順序，它需要額外結構（因此更耗記憶體）
# 你能解釋：為了維持插入順序，它需要額外結構（因此更耗記憶體）
