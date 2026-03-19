# R01. 字串分割與匹配（2.1–2.3）
# re.split() 多分隔符 / startswith / endswith / fnmatch

# re：正規表示式模組，用於彈性字串切割與模式比對
import re
# fnmatch / fnmatchcase：提供類似 Shell 的萬用字元匹配
from fnmatch import fnmatch, fnmatchcase

# ── 2.1 多界定符分割 ──────────────────────────────────
# 原始字串同時混用空白、分號、逗號作為分隔符
line = "asdf fjdk; afed, fjek,asdf, foo"
# [;,\s] 代表「分號 / 逗號 / 任一空白字元」；\s* 允許分隔符後面有可有可無的空白
# 這種寫法適合處理格式不一致的輸入資料
print(re.split(r"[;,\s]\s*", line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# 非捕獲分組：分組但不保留分隔符
# (?:...) 可把多個替代條件包成一組，但不會像捕獲分組那樣把分隔符放回結果
# 若改成 (...)（捕獲分組），結果會夾雜分隔符本身，常讓初學者困惑
print(re.split(r"(?:,|;|\s)\s*", line))
# ['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# ── 2.2 開頭/結尾匹配 ────────────────────────────────
# 單一檔名範例：快速判斷副檔名與前綴
filename = "spam.txt"
print(filename.endswith(".txt"))  # True
print(filename.startswith("file:"))  # False

# 同時檢查多種後綴 → 傳入 tuple（不能傳 list）
# endswith / startswith 在多條件時要傳 tuple，這是常見考點
# 下面會留下所有以 .c 或 .h 結尾的檔名
filenames = ["Makefile", "foo.c", "bar.py", "spam.c", "spam.h"]
print([name for name in filenames if name.endswith((".c", ".h"))])
# ['foo.c', 'spam.c', 'spam.h']

# ── 2.3 Shell 通配符匹配 ─────────────────────────────
# *.txt：任意檔名前綴 + .txt 結尾
print(fnmatch("foo.txt", "*.txt"))  # True
# Dat[0-9]*：Dat + 一位數字 + 後續任意字元
print(fnmatch("Dat45.csv", "Dat[0-9]*"))  # True

# fnmatchcase 強制區分大小寫
# 在 Windows 上 fnmatch 可能受系統大小寫規則影響；fnmatchcase 行為較一致
print(fnmatchcase("foo.txt", "*.TXT"))  # False

# 地址範例：挑出結尾是空白 + ST 的項目（例如路名縮寫 Street）
addresses = ["5412 N CLARK ST", "1060 W ADDISON ST", "1039 W GRANVILLE AVE"]
print([a for a in addresses if fnmatchcase(a, "* ST")])
# ['5412 N CLARK ST', '1060 W ADDISON ST']
