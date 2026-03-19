# R03. 字串清理、對齊、拼接與格式化（2.11–2.16）
# strip / ljust / join / format / format_map / textwrap

# textwrap：用於長字串自動換行與縮排
import textwrap

# ── 2.11 清理字元 ─────────────────────────────────────
# 含有前後空白與換行字元的字串
s = "  hello world \n"
# strip()：移除左右兩端空白（空白、\n、\t 等）
print(repr(s.strip()))  # 'hello world'
# lstrip()：只移除左側空白，右側保留
print(repr(s.lstrip()))  # 'hello world \n'
# strip("-=") 不是移除整段 "-="，而是移除兩端所有屬於 '-' 或 '=' 的字元
print("-----hello=====".strip("-="))  # 'hello'

# ── 2.13 字串對齊 ─────────────────────────────────────
# 對齊示範字串
text = "Hello World"
# 左對齊，總寬度 20（右邊補空白）
print(text.ljust(20))  # 'Hello World         '
# 右對齊，總寬度 20（左邊補空白）
print(text.rjust(20))  # '         Hello World'
# 置中，並用 '*' 當填充字元
print(text.center(20, "*"))  # '****Hello World*****'
# format 也可做對齊：^ 代表置中，寬度 20
print(format(text, "^20"))  # '    Hello World     '
# 數值格式：> 右對齊、寬 10、.2f 保留 2 位小數
print(format(1.2345, ">10.2f"))  # '      1.23'

# ── 2.14 合併拼接 ─────────────────────────────────────
# join 會在元素間插入指定分隔符，不會在頭尾多加
parts = ["Is", "Chicago", "Not", "Chicago?"]
print(" ".join(parts))  # 'Is Chicago Not Chicago?'
print(",".join(parts))  # 'Is,Chicago,Not,Chicago?'

# join 只能拼接字串；非字串元素需先轉型
data = ["ACME", 50, 91.1]
print(",".join(str(d) for d in data))  # 'ACME,50,91.1'

# ── 2.15 插入變量 ─────────────────────────────────────
# 準備模板與變數
name, n = "Guido", 37
s = "{name} has {n} messages."
# format：以關鍵字參數帶入欄位
print(s.format(name=name, n=n))  # 'Guido has 37 messages.'
# format_map(vars())：直接使用目前作用域變數字典
print(s.format_map(vars()))  # 'Guido has 37 messages.'
# f-string：語法最簡潔，直觀嵌入變數
print(f"{name} has {n} messages.")  # f-string（最簡潔）

# ── 2.16 指定列寬 ─────────────────────────────────────
# 長字串示範：方便觀察自動換行效果
long_s = (
    "Look into my eyes, look into my eyes, the eyes, "
    "not around the eyes, look into my eyes, you're under."
)
# fill(..., 40)：每行最大寬度約 40 字元
print(textwrap.fill(long_s, 40))
# initial_indent：只在第一行前面加縮排
print(textwrap.fill(long_s, 40, initial_indent="    "))
