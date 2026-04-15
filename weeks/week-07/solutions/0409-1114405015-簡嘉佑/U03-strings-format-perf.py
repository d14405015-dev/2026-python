# U03. 字串格式化效能與陷阱（2.14–2.20）
# join vs + / format_map 缺失鍵 / bytes 索引差異
#
# 本檔案涵蓋三個常見重點：
# 1. 字串大量串接時，join 通常比 += 更有效率。
# 2. format_map 可搭配 __missing__ 優雅處理缺少欄位。
# 3. str 與 bytes 在索引與格式化行為上有本質差異。

import timeit

# ── join 效能優於 + （2.14）──────────────────────────
parts = [f"item{i}" for i in range(1000)]


def bad_concat():
    s = ""
    for p in parts:
        # Python 字串不可變，每次 += 都可能建立新字串並複製內容
        # 在大量迴圈中容易變成 O(n^2) 成本
        s += p  # 每次建立新字串，O(n²)
    return s


def good_join():
    # 先收集片段再一次 join，可降低重複配置與複製
    return "".join(parts)  # 一次分配，O(n)


# 以 timeit 做簡單基準比較（數值會因機器與版本而異）
t1 = timeit.timeit(bad_concat, number=500)
t2 = timeit.timeit(good_join, number=500)
print(f"+串接: {t1:.3f}s  join: {t2:.3f}s")


# ── format_map 處理缺失鍵（2.15）─────────────────────
class SafeSub(dict):
    # 當 format_map 找不到 key 時，會呼叫 __missing__
    # 這裡選擇保留原佔位符，避免 KeyError 中斷
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"  # 缺失時保留佔位符


name = "Guido"
s = "{name} has {n} messages."
# vars() 會回傳目前作用域變數字典（例如 name）
# n 不存在時，SafeSub 讓模板原樣保留 {n}
print(s.format_map(SafeSub(vars())))  # 'Guido has {n} messages.'（n 不存在也不報錯）

# ── bytes 索引回傳整數（2.20）────────────────────────
a = "Hello"
b = b"Hello"
# str 索引回傳「字元」；bytes 索引回傳「0~255 整數」
# 這是文字與位元組模型不同所導致的 API 差異
print(a[0])  # 'H'（字元）
print(b[0])  # 72（整數 = ord('H')）

# bytes 不能直接 format，需先格式化再 encode
# 正確流程：先在 str 上 format，再依需求 encode 成 bytes
print("{:10s} {:5d}".format("ACME", 100).encode("ascii"))
# b'ACME            100'
