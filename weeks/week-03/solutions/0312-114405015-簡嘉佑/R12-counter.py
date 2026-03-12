# R12. Counter 統計 + most_common（1.12）

# Counter 是 collections 提供的「計數字典」：
# - key 是元素
# - value 是該元素出現次數
#
# 很適合做：字詞統計、事件次數統計、Top-N 頻率分析
from collections import Counter


# 一組單字資料（有重複）
words = ['look', 'into', 'my', 'eyes', 'look']

# 建立 Counter 後，會自動統計每個單字次數
# 例如：{'look': 2, 'into': 1, 'my': 1, 'eyes': 1}
word_counts = Counter(words)

# most_common(3) 取出「出現次數最多」的前 3 項
# 回傳格式是 list[tuple]，每個 tuple 為 (元素, 次數)
# 例如：[('look', 2), ('into', 1), ('my', 1)]
word_counts.most_common(3)


# update(...) 會把新資料再累加進現有計數
# 這裡再加入 ['eyes', 'eyes'] 之後，eyes 次數會 +2
# 原本 eyes=1，更新後會變 eyes=3
word_counts.update(['eyes', 'eyes'])
