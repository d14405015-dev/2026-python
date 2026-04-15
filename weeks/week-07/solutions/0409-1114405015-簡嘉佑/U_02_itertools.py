# Understand（理解）- itertools 工具函數
#
# 本檔案示範 itertools 常見工具：
# 1. islice：對迭代器做切片，避免一次產生全部資料。
# 2. dropwhile / takewhile：依條件「前綴」跳過或取用。
# 3. chain：串接多個可迭代物件。
# 4. permutations / combinations：排列與組合（順序是否重要）。
# 5. combinations_with_replacement：可重複取值的組合。

from itertools import islice, dropwhile, takewhile, chain, permutations, combinations

print("--- islice() 切片 ---")


def count(n):
    # 無限生成器：從 n 開始持續遞增
    # 常搭配 islice 等工具限制取值範圍
    i = n
    while True:
        yield i
        i += 1


c = count(0)
# islice(c, 5, 10) 代表取索引 5~9 的元素（右界不含 10）
# 由於 c 是迭代器，被消耗後位置會前進，不可自動回到起點
result = list(islice(c, 5, 10))
print(f"islice(c, 5, 10): {result}")

print("\n--- dropwhile() 條件跳過 ---")
nums = [1, 3, 5, 2, 4, 6]
# dropwhile 只會在「開頭連續符合條件」時跳過
# 一旦遇到第一個不符合條件的元素，後面全部原樣保留
result = list(dropwhile(lambda x: x < 5, nums))
print(f"dropwhile(x<5, {nums}): {result}")

print("\n--- takewhile() 條件取用 ---")
# takewhile 與 dropwhile 相反：
# 只取「開頭連續符合條件」的元素，遇到第一個不符合就停止
result = list(takewhile(lambda x: x < 5, nums))
print(f"takewhile(x<5, {nums}): {result}")

print("\n--- chain() 串聯 ---")
a = [1, 2]
b = [3, 4]
c = [5]
# chain(a, b, c) 可把多個序列視為單一長序列迭代
print(f"chain(a, b, c): {list(chain(a, b, c))}")

print("\n--- permutations() 排列 ---")
items = ["a", "b", "c"]
# permutations：順序重要，不可重複取同一位置元素
# 3 個元素全排列共有 3! = 6 種
print(f"permutations(items):")
for p in permutations(items):
    print(f"  {p}")

# 指定 r=2 時，表示從 3 個元素中取 2 個做有序排列
# 數量為 P(3,2)=3*2=6
print(f"permutations(items, 2):")
for p in permutations(items, 2):
    print(f"  {p}")

print("\n--- combinations() 組合 ---")
# combinations：順序不重要，不可重複
# 例如 ('a','b') 與 ('b','a') 視為同一組合
print(f"combinations(items, 2):")
for c in combinations(items, 2):
    print(f"  {c}")

print("\n--- 組合應用：密碼窮舉 ---")
chars = ["A", "B", "1"]
print("2位數密碼:")
# 使用 permutations(chars, 2) 產生兩位且不重複字元的排列
for p in permutations(chars, 2):
    print(f"  {''.join(p)}")

print("2位數密碼（可重複）:")
from itertools import combinations_with_replacement

# combinations_with_replacement：可重複取值，但順序不重要
# 若密碼情境需要順序也重要且可重複，通常應改用 product(chars, repeat=2)
for p in combinations_with_replacement(chars, 2):
    print(f"  {''.join(p)}")
