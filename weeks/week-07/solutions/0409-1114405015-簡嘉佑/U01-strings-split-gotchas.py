# U01. 字串分割與匹配的陷阱（2.1–2.11）
# 捕獲分組保留分隔符 / startswith 必須傳 tuple / strip 只處理頭尾
#
# 本檔案聚焦三個常見字串處理陷阱：
# 1. split 後若要重建原內容，需保留分隔符資訊。
# 2. startswith() 參數型別有限制，list 不能直接傳。
# 3. strip() 只清頭尾，無法直接整理中間多餘空白。

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
line = "asdf fjdk; afed, fjek,asdf, foo"
# 在 re.split 使用捕獲群組 ( ... )，可以把「分隔符」也保留下來
# 這在後續需要還原字串、分析原始格式時非常有用
fields = re.split(r"(;|,|\s)\s*", line)
# 分割結果通常呈現：值, 分隔符, 值, 分隔符, ...
# 因此偶數位是內容，奇數位是分隔符
values = fields[::2]  # 偶數索引 = 實際值
delimiters = fields[1::2] + [""]
# 重新把值與分隔符交錯組回去，驗證拆解流程是否完整
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'

# ── startswith 必須傳 tuple（2.2）────────────────────
url = "http://www.python.org"
choices = ["http:", "ftp:"]
try:
    # startswith 只接受「字串」或「字串 tuple」作為前綴集合
    # 傳 list 雖然語意接近，但型別不符，會丟 TypeError
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    print(f"TypeError: {e}")  # 不能傳 list！
# 實務上常見做法：動態清單先轉 tuple 再傳入
print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
s = "  hello     world  "
# strip() 僅處理字串前後空白，不影響中間連續空白
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）
# replace(" ", "") 會移除所有空白，可能破壞詞與詞之間應保留的間距
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）
# 正確需求若是「壓縮成單一空白」：先 strip，再用正規表示式合併連續空白
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
lines = ["  apple  \n", "  banana  \n"]
# 生成器表達式可逐項處理，面對大量資料時更省記憶體
for line in (l.strip() for l in lines):
    print(line)
