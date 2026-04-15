# U01. 字串分割與匹配的陷阱（2.1–2.11）
# 捕獲分組保留分隔符 / startswith 必須傳 tuple / strip 只處理頭尾
#
# 本檔案要解決三個常見誤區：
# 1. split 後想重組原字串，卻把分隔符弄丟。
# 2. startswith() 傳 list 導致 TypeError。
# 3. 認為 strip() 能清除中間空白，結果資料清理失敗。

import re

# ── 捕獲分組保留分隔符（2.1）─────────────────────────
line = "asdf fjdk; afed, fjek,asdf, foo"
# re.split 若使用「捕獲群組 ( ... )」，會把匹配到的分隔符一起放進結果
# 這在需要「保留原分隔符資訊」時很有用，例如還原、分析、標註來源格式
fields = re.split(r"(;|,|\s)\s*", line)
# re.split 的結果會是：值, 分隔符, 值, 分隔符, ...
# 偶數索引通常是實際值，奇數索引通常是分隔符
values = fields[::2]  # 偶數索引 = 實際值
delimiters = fields[1::2] + [""]
# 用 zip 把值與分隔符重新交錯串回去，驗證分割資訊是否完整
rebuilt = "".join(v + d for v, d in zip(values, delimiters))
print(rebuilt)  # 'asdf fjdk;afed,fjek,asdf,foo'

# ── startswith 必須傳 tuple（2.2）────────────────────
url = "http://www.python.org"
choices = ["http:", "ftp:"]
try:
    # startswith() 的第一個參數只能是「字串」或「字串 tuple」
    # list 雖然也是容器，但 API 規格不接受，因此會拋 TypeError
    url.startswith(choices)  # type: ignore[arg-type]
except TypeError as e:
    print(f"TypeError: {e}")  # 不能傳 list！
# 實務上如果前綴集合是動態建立，記得先 tuple(...) 再傳入
print(url.startswith(tuple(choices)))  # True（轉成 tuple 才行）

# ── strip 只處理頭尾，不處理中間（2.11）──────────────
s = "  hello     world  "
# strip() 只會移除字串前後空白，不會動到中間
print(repr(s.strip()))  # 'hello     world'（中間多餘空白還在）
# replace(" ", "") 會刪掉所有空白，可能把原本應保留的詞間空格也破壞
print(repr(s.replace(" ", "")))  # 'helloworld'（過頭，連詞間空白也消）
# 若需求是「把多個空白壓成一個空白」，可用正規表示式 \s+
# 先 strip 再壓縮，可避免頭尾多留空格
print(repr(re.sub(r"\s+", " ", s.strip())))  # 'hello world'（正確）

# 生成器逐行清理（高效，不預載入記憶體）
lines = ["  apple  \n", "  banana  \n"]
# 這種寫法適合大量文字處理：逐行處理、逐行輸出，記憶體使用較穩定
for line in (l.strip() for l in lines):
    print(line)
