# Understand（理解）- 生成器概念
#
# 本檔案重點：
# 1. 只要函式內出現 yield，就會變成「生成器函式」。
# 2. 呼叫生成器函式不會立刻執行本體，而是回傳一個 generator 物件。
# 3. 每次 next() 會從上次停住的位置繼續，直到下一個 yield。
# 4. 函式自然結束時，會自動拋出 StopIteration 表示資料耗盡。


def frange(start, stop, step):
    # 類似 range()，但支援浮點數步進
    # 注意浮點數累加可能有精度誤差，教學示範時通常可接受
    x = start
    while x < stop:
        # yield 回傳當前值，並暫停函式狀態（區域變數會被保留）
        yield x
        x += step


result = list(frange(0, 2, 0.5))
print(f"frange(0, 2, 0.5): {result}")


def countdown(n):
    # 這段 print 會在「第一次開始迭代」時才看到，不會在建立物件時執行
    print(f"Starting countdown from {n}")
    while n > 0:
        # 每次產生目前數字，下一次再繼續 n -= 1
        yield n
        n -= 1
    # 迭代結束前執行收尾邏輯
    print("Done!")


print("\n--- 建立生成器 ---")
c = countdown(3)
# 到這一行為止，countdown 函式本體尚未開始跑
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
# 手動呼叫 next()，觀察生成器逐步恢復執行的行為
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

try:
    # 資料耗盡後再 next()，會收到 StopIteration
    next(c)
except StopIteration:
    print("StopIteration!")


def fibonacci():
    # 無限生成器：持續產生費波那契數列
    # a 是目前值，b 是下一個值
    a, b = 0, 1
    while True:
        yield a
        # 同步更新到下一組狀態
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
# 因為是無限序列，通常搭配 range() 或條件限制取前 N 個
for i in range(10):
    print(next(fib), end=" ")
print()


def chain_iter(*iterables):
    # 把多個可迭代物件串接成單一序列
    for it in iterables:
        # yield from 會把控制權委派給子可迭代物件
        # 等同於：for x in it: yield x
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        # 建立樹節點間的父子關係
        self.children.append(node)

    def __iter__(self):
        # 讓 Node 物件可直接被 for 迭代其子節點
        return iter(self.children)

    def depth_first(self):
        # 深度優先（DFS）前序遍歷：先自己，再子樹
        yield self
        for child in self:
            # 遞迴委派：把子節點 depth_first() 的結果接續吐出
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

for node in root.depth_first():
    print(node.value, end=" ")
print()


def flatten(items):
    # 將巢狀序列遞迴攤平為一維序列
    for x in items:
        # 若元素本身可迭代且不是字串，則遞迴展開
        # 為何排除 str：字串也是 iterable，若不排除會被拆成單一字元
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
print(f"展開: {list(flatten(nested))}")
