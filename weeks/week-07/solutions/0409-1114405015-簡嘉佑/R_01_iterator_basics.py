# Remember（記憶）- 迭代器基礎概念
#
# 本檔案示範 Python 的「可迭代物件（iterable）」與「迭代器（iterator）」：
# 1. iterable 只要能被 iter() 轉成 iterator 即可。
# 2. iterator 需要提供 __next__()，每次被 next() 呼叫時回傳下一個值。
# 3. 當資料耗盡，必須丟出 StopIteration，表示遍歷結束。
#
# 你可以把 iterator 想成「一次吐一個值的資料流」，而不是一次把所有值都拿出來。

# 1. 迭代器協議的核心方法
items = [1, 2, 3]

# iter() 會呼叫物件的 __iter__()，並回傳一個 iterator 物件
# 列表本身是 iterable，但不是 iterator，所以需要先用 iter() 包一層
it = iter(items)
print(f"迭代器: {it}")

# next() 會呼叫 iterator 的 __next__()，每次取出一個新值
# 這裡連續取三次，會依序得到 1、2、3
print(f"第一個: {next(it)}")  # 1
print(f"第二個: {next(it)}")  # 2
print(f"第三個: {next(it)}")  # 3

# 當沒有更多元素時，next() 會丟出 StopIteration
# 這是 Python 迭代器協議中「正常結束」的訊號，不是程式錯誤
try:
    next(it)
except StopIteration:
    print("迭代結束!")

# 2. 常見可迭代物件
print("\n--- 常見可迭代物件 ---")

# 列表：最常見的 iterable，可用 for 直接遍歷
print(f"列表 iter: {iter([1, 2, 3])}")

# 字串：會逐字元迭代
print(f"字串 iter: {iter('abc')}")

# 字典：預設會迭代 key（不是 value）
print(f"字典 iter: {iter({'a': 1, 'b': 2})}")

# 檔案物件：每次迭代通常讀一行，對處理大型檔案很實用
import io

f = io.StringIO("line1\nline2\nline3")
print(f"檔案 iter: {iter(f)}")


# 3. 自訂可迭代物件
class CountDown:
    # CountDown 是「可迭代物件」：實作 __iter__() 來回傳真正的 iterator
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        # 每次開始新的遍歷都建立一個新的迭代器，避免共享狀態互相影響
        return CountDownIterator(self.start)


class CountDownIterator:
    # CountDownIterator 是「迭代器」：負責保存當前狀態並提供 __next__()
    def __init__(self, start):
        self.current = start

    def __next__(self):
        # 當 current <= 0 代表倒數結束，依協議丟出 StopIteration
        if self.current <= 0:
            raise StopIteration
        # 先遞減再回傳，讓輸出從 start 到 1（例如 3, 2, 1）
        self.current -= 1
        return self.current + 1


print("\n--- 自訂迭代器 ---")
for i in CountDown(3):
    print(i, end=" ")  # 3 2 1

# 4. 迭代器 vs 可迭代物件
print("\n\n--- 迭代器 vs 可迭代物件 ---")

# 列表是 iterable（可被 iter() 轉換），但沒有 __next__()
my_list = [1, 2, 3]
print(f"列表: 可迭代物件 ✓, 迭代器 ✗")

# 對列表呼叫 iter() 後，得到的物件才是 iterator
my_iter = iter(my_list)
print(f"iter(列表): 可迭代物件 ✗, 迭代器 ✓")

# iterator 通常同時也是 iterable（其 __iter__() 會回傳自己）
print(f"迭代器: 可迭代物件 ✓ (有__iter__), 迭代器 ✓ (有__next__)")

# 5. StopIteration 例外
print("\n--- StopIteration 用法 ---")


# 手動遍歷（章節 4.1 風格）
# 模擬 for 迴圈底層行為：
# 1) 先呼叫 iter() 拿到 iterator
# 2) 重複呼叫 next() 取值
# 3) 捕捉 StopIteration 後結束迴圈
def manual_iter(items):
    it = iter(items)
    while True:
        try:
            item = next(it)
            print(f"取得: {item}")
        except StopIteration:
            break


manual_iter(["a", "b", "c"])


# 使用預設值的版本
# next(it, None) 可在耗盡時直接回傳預設值，不會丟出例外
# 這種寫法在某些情境下較簡潔，但要注意：
# 若資料本身可能包含 None，就不適合作為結束判斷值
def manual_iter_default(items):
    it = iter(items)
    while True:
        item = next(it, None)  # 預設值
        if item is None:
            break
        print(f"取得: {item}")


print("\n使用預設值:")
manual_iter_default(["a", "b", "c"])
