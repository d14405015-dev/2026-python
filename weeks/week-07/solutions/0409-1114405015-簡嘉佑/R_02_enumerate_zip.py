# Remember（記憶）- enumerate() 和 zip()
#
# 本檔案重點：
# 1. enumerate(iterable, start=0)：同時取得「索引」與「元素」。
# 2. zip(iter1, iter2, ...)：把多個序列「平行配對」成 tuple。
# 3. zip() 預設以最短序列為準，較長序列的多餘資料會被忽略。
# 4. 若要保留最長序列，可用 itertools.zip_longest()。

colors = ["red", "green", "blue"]

print("--- enumerate() 基本用法 ---")
# enumerate(colors) 預設從 0 開始計數
# 每圈回傳 (索引, 值)，可直接解包成 i 與 color
for i, color in enumerate(colors):
    print(f"{i}: {color}")

print("\n--- enumerate(start=1) ---")
# 設定 start=1 讓索引從 1 開始，更符合人類習慣（第1個、第2個...）
for i, color in enumerate(colors, 1):
    print(f"第{i}個: {color}")

print("\n--- enumerate with 檔案 ---")
# 實務上常用於檔案逐行處理，搭配行號顯示錯誤位置
# 這裡用 list 模擬檔案每一行的內容
lines = ["line1", "line2", "line3"]
for lineno, line in enumerate(lines, 1):
    print(f"行 {lineno}: {line}")

print("\n--- zip() 基本用法 ---")
# zip(names, scores) 會把同位置元素配對：
# (names[0], scores[0]), (names[1], scores[1]), ...
names = ["Alice", "Bob", "Carol"]
scores = [90, 85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

print("\n--- zip() 多個序列 ---")
# zip() 不只兩個序列，三個以上也可以平行配對
a = [1, 2, 3]
b = [10, 20, 30]
c = [100, 200, 300]
for x, y, z in zip(a, b, c):
    print(f"{x} + {y} + {z} = {x + y + z}")

print("\n--- zip() 長度不同 ---")
# 預設 zip() 會在「最短序列結束」時停止
# 下面 x 長度是 2、y 長度是 3，結果只會有 2 組
x = [1, 2]
y = ["a", "b", "c"]
print(f"list(zip(x, y)): {list(zip(x, y))}")

from itertools import zip_longest

# zip_longest() 會以最長序列為準，不足的部分用 fillvalue 補齊
# 在資料清理或欄位對齊時很常用
print(f"zip_longest: {list(zip_longest(x, y, fillvalue=0))}")

print("\n--- 建立字典 ---")
# 常見技巧：用 zip(keys, values) 先配對，再交給 dict 建立字典
# 注意 keys 與 values 長度不一致時，仍以最短長度為準
keys = ["name", "age", "city"]
values = ["John", "30", "NYC"]
d = dict(zip(keys, values))
print(f"dict: {d}")
