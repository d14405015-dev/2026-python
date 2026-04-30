# U01. 計時裝飾器實作與資料格式速度比較（6.1 / 6.2 / 6.3）
# 從「重複的計時程式碼」出發，引入裝飾器，再做格式實驗
#
# 這支程式的目標：
#   1) 展示「沒有裝飾器」時每個函式都要手動計時的缺點
#   2) 實作 timeit 裝飾器，把計時邏輯封裝起來
#   3) 用 functools.wraps 保留原函式的 metadata（__name__ / __doc__）
#   4) 對 CSV / JSON / XML 三種格式進行速度比較實驗

import csv          # 讀寫 CSV 格式
import json         # 讀寫 JSON 格式
import time         # 高精度計時 perf_counter
import io           # io.StringIO：把字串當成檔案物件
import xml.etree.ElementTree as ET  # 解析 XML 格式
import functools    # functools.wraps：保留被包裝函式的 metadata

# ═══════════════════════════════════════════════════════════
# Part 1｜問題：每個函式都要手動計時 → 大量重複
# ═══════════════════════════════════════════════════════════
# 以下三個函式分別用三種格式解析相同的資料，
# 如果要對每個函式計時，傳統做法是在呼叫前後各加一行，
# 造成大量重複且容易漏改。

def read_csv_raw(data: str) -> list:
    """將 CSV 格式字串解析成 list of dict。

    流程說明：
    1. io.StringIO(data)  → 把純字串包成「類檔案物件」，
       讓 DictReader 以為自己在讀一個真實檔案
    2. csv.DictReader(...)→ 以第一列（標題列）為 key，
       後續每列自動解析成 {欄位名: 值} 的 dict
    3. list(...)          → DictReader 是惰性迭代器，
       加上 list() 強制一次讀完全部資料（方便計時）
    """
    return list(csv.DictReader(io.StringIO(data)))

def read_json_raw(data: str) -> list:
    """將 JSON 格式字串反序列化成 list of dict。

    json.loads（load string）：
    - 底層以 C 擴充模組實作，速度通常是三者最快
    - 回傳型別取決於 JSON 根節點：
        JSON array   → Python list
        JSON object  → Python dict
    此處 JSON 資料是陣列，所以回傳 list of dict。
    """
    return json.loads(data)

def read_xml_raw(data: str) -> list:
    """將 XML 格式字串解析成 list of dict。

    流程說明：
    1. ET.fromstring(data)      → 把 XML 字串解析成元素樹，
       root 是根節點 <data>
    2. root.findall("row")     → 在根節點的直接子元素中，
       找出所有 tag 為 "row" 的元素，回傳 list
    3. r.attrib                → 取出每個 <row> 元素的屬性字典，
       例如 <row id="0" name="Student0000" score="60"/>
       → {"id": "0", "name": "Student0000", "score": "60"}
       注意：XML 屬性值一律是字串，與 JSON 不同（JSON 有數值型別）
    """
    root = ET.fromstring(data)
    return [r.attrib for r in root.findall("row")]

# 沒有裝飾器時的傳統計時方式（已註解掉，僅供對比說明）：
# start = time.perf_counter()
# result = read_csv_raw(data)
# print(f"read_csv_raw 耗時 {time.perf_counter() - start:.6f}s")
#
# start = time.perf_counter()
# result = read_json_raw(data)
# print(f"read_json_raw 耗時 {time.perf_counter() - start:.6f}s")
#
# 問題：每加一個函式就多寫三行，且容易忘記移除

# ═══════════════════════════════════════════════════════════
# Part 2｜解法：裝飾器把計時邏輯包起來，一次定義，到處復用
# ═══════════════════════════════════════════════════════════
# 裝飾器（Decorator）是一種高階函式：
#   - 接受一個函式作為參數
#   - 回傳一個「增強版」的新函式
#   - 原函式的邏輯完全不需要修改

def timeit(func):
    """基礎版裝飾器：在呼叫前後計時，印出耗時。

    缺點：wrapper 會蓋掉原函式的 __name__、__doc__ 等屬性，
    導致 help()、debug 工具看到的名稱是 'wrapper' 而非原函式名。
    """
    def wrapper(*args, **kwargs):
        # *args, **kwargs：轉發所有位置與關鍵字引數，
        # 讓 wrapper 可以包裝任何簽名的函式
        start = time.perf_counter()   # 記錄開始時間
        # time.perf_counter()：系統最高精度的單調時鐘，
        # 不受系統時間調整影響，專為效能量測設計（單位：秒）
        result = func(*args, **kwargs)   # 執行原函式，傳遞所有引數
        elapsed = time.perf_counter() - start  # 兩次相減 = 實際耗時
        # f-string 格式說明：
        #   {func.__name__:<20s} → 函式名稱，靠左對齊，共 20 字元寬（排版整齊）
        #   {elapsed:.6f}s       → 耗時，保留小數點後 6 位（微秒級精度）
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result  # 必須把原函式的回傳值原封傳出，
                       # 否則對呼叫端來說結果就消失了
    return wrapper

# ── 展示 metadata 遺失的問題 ────────────────────────────────
# Python 的裝飾器本質上是「函式替換」：
#   wrapped = timeit(demo)  等同於  @timeit 語法糖
# 但基礎版 timeit 回傳的是 wrapper，
# wrapper.__name__ 是 'wrapper' 而非 'demo'。
# 這在日誌紀錄、錯誤追蹤（traceback）、help() 時會造成混淆。
def demo():
    """這是 demo 的說明文字"""
    pass

wrapped = timeit(demo)
# 預期輸出 'demo'，但實際是 'wrapper'，說明 metadata 已被覆蓋
print("未加 wraps 前：", wrapped.__name__)   # 輸出 'wrapper'（錯誤！）

# ═══════════════════════════════════════════════════════════
# Part 3｜functools.wraps：保留原函式的 metadata
# ═══════════════════════════════════════════════════════════
# @functools.wraps(func) 會把 func 的以下屬性複製到 wrapper：
#   __name__、__qualname__、__doc__、__dict__、__module__、__wrapped__
# 如此 help()、logging、traceback 都能看到正確的函式名稱

def timeit(func):
    """改良版裝飾器：加上 functools.wraps 保留 metadata。

    @functools.wraps(func) 的作用：
    把 func 的以下屬性全部複製到 wrapper：
      __name__     → 函式名稱（最常用）
      __qualname__ → 完整限定名稱（含類別/巢狀層次）
      __doc__      → docstring
      __dict__     → 函式自訂屬性
      __module__   → 所屬模組名稱
      __wrapped__  → 指向原始函式，方便反向取用
    """
    @functools.wraps(func)   # 把 func 的所有 metadata 複製到 wrapper
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__:<20s} {elapsed:.6f}s")
        return result
    return wrapper

wrapped = timeit(demo)
# 現在 wrapped.__name__ 正確顯示為 'demo'
print("加 wraps 後：  ", wrapped.__name__)   # 輸出 'demo'（正確）
print()

# ═══════════════════════════════════════════════════════════
# Part 4｜實驗：相同資料，CSV vs JSON vs XML 速度比較
# ═══════════════════════════════════════════════════════════

# ── 產生測試資料（1000 筆學生記錄）────────────────────────
# 用程式產生而非讀取外部檔案，確保三種格式的資料完全等量等值
N = 1000

# 產生 CSV 格式字串
# io.StringIO() 模擬一個「記憶體中的文字檔」，
# 避免真的寫到磁碟，速度更快且不產生暫存檔案。
csv_buf = io.StringIO()
# DictWriter：以 dict 為單位寫入，fieldnames 定義欄位順序
writer = csv.DictWriter(csv_buf, fieldnames=["id", "name", "score"])
writer.writeheader()  # 寫入標題列 → 輸出：id,name,score
for i in range(N):
    # f"Student{i:04d}"：i 格式化為 4 位數補零，例如 Student0007
    # 60 + i % 40：分數在 60~99 之間循環，確保每筆資料不完全相同
    writer.writerow({"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40})
CSV_DATA = csv_buf.getvalue()  # getvalue() 取出 StringIO 中的全部字串內容

# 產生 JSON 格式字串
# 使用串列推導式（list comprehension）一次產生 N 個 dict，
# 再由 json.dumps 序列化成 JSON 字串。
# JSON 的數值欄位（id、score）保留 int 型別，
# 解析時也會還原為 int（這是 CSV/XML 做不到的）。
JSON_DATA = json.dumps([
    {"id": i, "name": f"Student{i:04d}", "score": 60 + i % 40}
    for i in range(N)
])

# 產生 XML 格式字串
# 使用生成器運算式（generator expression）+ str.join 串接，
# 比迴圈 += 更有效率（只建立一次字串，不浪費中間記憶體）。
# 每筆資料形如：<row id="0" name="Student0000" score="60"/>
# 注意：XML 屬性值必須加引號，所有欄位都以字串形式儲存。
xml_rows = "".join(
    f'<row id="{i}" name="Student{i:04d}" score="{60 + i % 40}"/>'
    for i in range(N)
)
# XML 文件必須有唯一根元素，這裡以 <data> 包住所有 <row>
XML_DATA = f"<data>{xml_rows}</data>"

# ── 帶回傳耗時的靜默計時包裝 ────────────────────────────
# 與 timeit 不同：不印出結果，而是把耗時一起回傳，
# 方便後續累加計算平均值。
def timeit_silent(func):
    """靜默版計時裝飾器：回傳 (原函式結果, 耗時秒數) 元組。

    與 timeit 的差別：
    - timeit        → 直接 print 耗時，適合互動式展示
    - timeit_silent → 把耗時當成回傳值，適合程式化收集資料

    使用方式（解包賦值）：
        result, elapsed = _csv(CSV_DATA)
        # 若只需要耗時，可用 _ 捨棄結果：
        _, t = _csv(CSV_DATA)
    """
    @functools.wraps(func)   # 同樣保留 metadata
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        # 以 tuple 一次回傳兩個值：原始結果 + 耗時秒數
        return result, time.perf_counter() - start
    return wrapper

# 用 timeit_silent 包裝三個原始讀取函式，產生計時版本
_csv  = timeit_silent(read_csv_raw)
_json = timeit_silent(read_json_raw)
_xml  = timeit_silent(read_xml_raw)

# ── 執行比較（重複 5 次取平均，排除冷啟動影響）────────────
# 第一次執行可能因 CPU 暖機、記憶體初始化而偏慢，
# 重複多次取平均可得到更穩定的基準值。
RUNS = 5
times = {"CSV": 0.0, "JSON": 0.0, "XML": 0.0}  # 累加各格式總耗時

for _ in range(RUNS):
    _, t = _csv(CSV_DATA)    ; times["CSV"]  += t  # 每次加上本次耗時
    _, t = _json(JSON_DATA)  ; times["JSON"] += t
    _, t = _xml(XML_DATA)    ; times["XML"]  += t

# 印出結果表格
# 格式字串說明：
#   {'格式':<6}    → 欄位名「格式」，靠左對齊，共 6 字元寬
#   {'平均耗時':>12} → 欄位名「平均耗時」，靠右對齊，12 字元寬
print(f"=== 讀取 {N} 筆資料，重複 {RUNS} 次平均 ===\n")
print(f"{'格式':<6} {'平均耗時':>12}  {'相對 JSON':>10}")

# 以 JSON 的平均耗時作為基準（base = 1.0x），
# 其他格式的 avg/base 就代表「比 JSON 慢幾倍」
base = times["JSON"] / RUNS
for fmt, total in times.items():
    avg = total / RUNS   # 總耗時 ÷ 執行次數 = 每次平均耗時
    # {fmt:<6}         → 格式名稱，靠左對齊 6 字元
    # {avg:.6f}s       → 平均秒數，6 位小數
    # {avg/base:>8.2f}x → 相對倍數，靠右 8 字元、2 位小數
    print(f"  {fmt:<6} {avg:.6f}s   {avg/base:>8.2f}x")

# ═══════════════════════════════════════════════════════════
# 觀察重點
# ═══════════════════════════════════════════════════════════
# 1. JSON 通常最快：Python 的 json 模組底層是 C 實作，解析效率高
# 2. XML  通常最慢：需要建立元素樹、解析屬性字串，開銷最大
# 3. CSV  介於中間：格式簡單，但每欄值都是字串，需要自行轉型
#
# 裝飾器帶來的好處：
# - 計時邏輯只寫一次，不汙染原函式本體
# - 要移除計時只需拿掉包裝呼叫，函式本身不需修改
# - functools.wraps 確保 debug / help() 時看到正確函式名稱
# - 可輕易組合：例如同時加上計時與日誌兩個裝飾器
