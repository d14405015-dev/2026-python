# Understand（理解）- 生成器概念


# 以浮點數步進產生區間數值（不包含 stop）
def frange(start, stop, step):
    x = start
    while x < stop:
        # 每次回傳目前 x，並暫停函式狀態
        yield x
        x += step


result = list(frange(0, 2, 0.5))
# 轉成 list 以便一次查看所有產生結果
print(f"frange(0, 2, 0.5): {result}")


# 倒數生成器：每次產生一個數字直到 1
def countdown(n):
    print(f"Starting countdown from {n}")
    while n > 0:
        yield n
        n -= 1
    print("Done!")


print("\n--- 建立生成器 ---")
# 呼叫函式只會建立生成器，不會立刻執行到 yield
c = countdown(3)
print(f"生成器物件: {c}")

print("\n--- 逐步迭代 ---")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")
print(f"next(c): {next(c)}")

# 生成器資料耗盡後會拋出 StopIteration
try:
    next(c)
except StopIteration:
    print("StopIteration!")


# 無限 Fibonacci 生成器
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


print("\n--- Fibonacci 生成器 ---")
fib = fibonacci()
# 只取前 10 個值，避免無限生成器跑不完
for i in range(10):
    print(next(fib), end=" ")
print()


# 串接多個可迭代物件
def chain_iter(*iterables):
    for it in iterables:
        # 將子迭代器的值直接往外轉送
        yield from it


print("\n--- yield from 用法 ---")
result = list(chain_iter([1, 2], [3, 4], [5, 6]))
print(f"chain_iter: {result}")


class Node:
    # 每個節點保存自己的值與子節點清單
    def __init__(self, value):
        self.value = value
        self.children = []

    # 新增一個子節點
    def add_child(self, node):
        self.children.append(node)

    # 讓 Node 物件可直接被 for 迴圈走訪其 children
    def __iter__(self):
        return iter(self.children)

    # 深度優先走訪（先自己，再走訪所有子節點）
    def depth_first(self):
        yield self
        for child in self:
            yield from child.depth_first()


print("\n--- 樹的深度優先遍歷 ---")
# 建立一棵簡單的樹做遍歷示範
root = Node(0)
root.add_child(Node(1))
root.add_child(Node(2))
root.children[0].add_child(Node(3))
root.children[0].add_child(Node(4))

for node in root.depth_first():
    print(node.value, end=" ")
print()


# 遞迴攤平巢狀可迭代資料（字串除外）
def flatten(items):
    for x in items:
        # 可迭代且不是字串時，繼續往下展開
        if hasattr(x, "__iter__") and not isinstance(x, str):
            yield from flatten(x)
        else:
            yield x


print("\n--- 巢狀序列攤平 ---")
nested = [1, [2, [3, 4]], 5]
# flatten 會把任意層巢狀結構展開成一維序列
print(f"展開: {list(flatten(nested))}")
