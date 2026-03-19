# R02. 正則表達式：搜尋、替換、旗標（2.4–2.8）
# re.compile / findall / sub / IGNORECASE / 非貪婪 / DOTALL

# re：Python 內建正則表達式模組
import re

# ── 2.4 匹配和搜尋 ────────────────────────────────────
# 測試字串：內含兩個日期格式
text = "Today is 11/27/2012. PyCon starts 3/13/2013."
# 先編譯樣式可重複使用；(\d+) 代表一段數字，三組分別對應月/日/年
datepat = re.compile(r"(\d+)/(\d+)/(\d+)")

# findall 會回傳所有匹配結果；因有分組，所以每筆是 tuple
print(datepat.findall(text))
# [('11', '27', '2012'), ('3', '13', '2013')]

# match 只從字串開頭比對（不是全文搜尋）
m = datepat.match("11/27/2012")
assert m is not None
# group(0) 是完整匹配；groups() 是各捕獲分組
print(m.group(0), m.groups())  # '11/27/2012' ('11', '27', '2012')

# finditer 逐筆回傳 Match 物件，適合邊走訪邊處理
for m in datepat.finditer(text):
    month, day, year = m.groups()
    # 重新排版為 year-month-day
    print(f"{year}-{month}-{day}")

# ── 2.5 搜尋和替換 ───────────────────────────────────
# re.sub：\1、\2、\3 可引用前面正則中的第 1/2/3 個分組
print(re.sub(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text))
# 'Today is 2012-11-27. PyCon starts 2013-3-13.'

# 命名群組
# 命名群組可提升可讀性：month/day/year 比單純數字索引更直觀
# 在替換字串中用 \g<name> 引用命名分組
print(
    re.sub(
        r"(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)",
        r"\g<year>-\g<month>-\g<day>",
        text,
    )
)

# re.subn 回傳替換次數
# subn 會回傳 (新字串, 替換次數)，方便做統計或驗證
newtext, n = re.subn(r"(\d+)/(\d+)/(\d+)", r"\3-\1-\2", text)
print(f"替換了 {n} 次")  # 替換了 2 次

# ── 2.6 忽略大小寫 ───────────────────────────────────
# 測試不同大小寫版本的 python
s = "UPPER PYTHON, lower python, Mixed Python"
# IGNORECASE 讓匹配不受大小寫影響
print(re.findall("python", s, flags=re.IGNORECASE))
# ['PYTHON', 'python', 'Python']

# ── 2.7 非貪婪（最短匹配）────────────────────────────
# 同一行有兩段引號內容，用來觀察貪婪與非貪婪差異
text2 = 'Computer says "no." Phone says "yes."'
# .* 是貪婪匹配：會盡可能吃到最後一個雙引號
print(re.compile(r'"(.*)"').findall(text2))  # 貪婪：['no." Phone says "yes.']
# .*? 是非貪婪匹配：每次只吃到最近的雙引號
print(re.compile(r'"(.*?)"').findall(text2))  # 非貪婪：['no.', 'yes.']

# ── 2.8 多行匹配（DOTALL）────────────────────────────
# 範例含換行的註解字串
code = "/* this is a\nmultiline comment */"
# DOTALL 讓 . 也能匹配換行，才能跨行抓到完整內容
print(re.compile(r"/\*(.*?)\*/", re.DOTALL).findall(code))
# [' this is a\nmultiline comment ']
