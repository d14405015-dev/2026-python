# R9. 兩字典相同點：keys/items 集合運算（1.9）

# 兩個範例字典
a = {'x': 1, 'y': 2, 'z': 3}
b = {'w': 10, 'x': 11, 'y': 2}

# a.keys() 與 b.keys() 都是「可做集合運算」的視圖（dict_keys）
# 交集 &：找出兩邊都存在的 key
# 這裡結果是 {'x', 'y'}
a.keys() & b.keys()

# 差集 -：找出只在 a 出現、但不在 b 的 key
# 這裡結果是 {'z'}
a.keys() - b.keys()

# items() 也能做集合運算，但比較的是「(key, value) 整組」
# 只有 key 和 value 都相同才算同一項
# 這裡結果是 {('y', 2)}，因為 x 的值不同（1 vs 11）
a.items() & b.items()


# 字典推導式（dict comprehension）範例：
# 從 a 中建立新字典 c，但排除 key 'z' 和 'w'
#
# 先算 a.keys() - {'z', 'w'}：
# - 'z' 在 a 裡會被排除
# - 'w' 不在 a 裡，差集自然忽略它
# 最後只剩 {'x', 'y'}，所以 c 會是 {'x': 1, 'y': 2}
c = {k: a[k] for k in a.keys() - {'z', 'w'}}
