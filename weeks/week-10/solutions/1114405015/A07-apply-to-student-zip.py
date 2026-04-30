# A07. 綜合應用：把 I/O 技巧套到真實學生資料
# Bloom: Apply — 複習並組合 R01~A06 的 API
#
# 這支程式的目標：
# 1) 從 zip 壓縮檔直接讀 109~114 的 CSV（不解壓）
# 2) 做跨屆統計（總人數、各系所、各入學方式）
# 3) 在暫存資料夾產出 Markdown 報告與 pickle 快照
# 4) 離開程式後不留下中間檔案（由 TemporaryDirectory 自動清理）
#
# 資料來源：assets/npu-stu-109-114-anon.zip（6 屆新生資料庫，學號已匿名）
# 用到的小節對照：
#   5.11 pathlib 組路徑
#   5.12 exists 檢查
#   5.7  zipfile 讀壓縮檔（不解壓）
#   5.1  encoding='utf-8-sig' 處理 Excel 存的 BOM
#   5.6  io.StringIO 把 bytes 轉成 csv 可讀的 file-like
#   5.19 TemporaryDirectory 沙箱輸出
#   5.5  open(..., 'x') 只寫一次的報告檔
#   5.21 pickle 保存跨屆統計快照
#   5.2  print(file=) 寫 Markdown 週報

import csv
import io
import pickle
import tempfile
import zipfile
from collections import Counter
from pathlib import Path


# ── 5.11 / 5.12 找到資料檔 ─────────────────────────────
# 以「目前程式所在資料夾」作為起點，避免使用硬編碼絕對路徑。
HERE = Path(__file__).resolve().parent


def _find_zip_path(start: Path) -> Path:
    """向上搜尋 assets zip，讓程式搬到別層資料夾也能正常執行。

    搜尋方式：
    - 先檢查目前目錄
    - 再一路往父層資料夾檢查
    - 只要找到 assets/npu-stu-109-114-anon.zip 就回傳
    """
    for parent in [start] + list(start.parents):
        candidate = parent / "assets" / "npu-stu-109-114-anon.zip"
        if candidate.exists():
            return candidate

    # 全部父層都找不到時，丟出明確錯誤讓使用者知道缺資料檔。
    raise FileNotFoundError("找不到 assets/npu-stu-109-114-anon.zip")


ZIP_PATH = _find_zip_path(HERE)
print("資料來源:", ZIP_PATH.name)


# ── 5.7 + 5.6 + 5.1 不解壓讀 zip 裡的 CSV ──────────────
def iter_year_csv(zip_path: Path):
    """逐年產出 (學年, header, rows)。

    為什麼設計成 generator：
    - 介面更清楚，主流程只要 for year, header, rows in ...
    - 可把「讀檔細節」與「統計邏輯」拆開，維護性更好

    回傳內容：
    - year: 例如 '109'、'110'
    - header: CSV 標題列（欄位名稱）
    - rows: 資料列（不含標題）
    """
    with zipfile.ZipFile(zip_path) as z:
        # zip 內可能有多個檔案，逐一檢查。
        for info in z.infolist():
            name = info.filename
            if not name.endswith(".csv"):
                # 不是 CSV（例如說明文字）就跳過。
                continue

            # 依題目資料命名規則，檔名前三碼就是學年（109~114）。
            year = name[:3]

            # 讀出的內容是 bytes，先用 utf-8-sig 去掉可能的 BOM。
            raw = z.read(info)
            text = raw.decode("utf-8-sig")

            # 用 StringIO 把字串包成「類檔案物件」再交給 csv.reader。
            reader = csv.reader(io.StringIO(text))
            rows = list(reader)
            if not rows:
                # 保險處理：空檔案直接跳過，避免 rows[0] 失敗。
                continue

            # rows[0] 是表頭，rows[1:] 才是資料。
            yield year, rows[0], rows[1:]


# ── 跨屆統計 ───────────────────────────────────────────
# summary: 每一年一包統計結果
#   total: 該年總人數
#   by_dept: 各系所人數 Counter
#   by_entry: 各入學方式人數 Counter
summary = {}

# all_depts: 跨六屆累加後的系所人數，方便找全體熱門系所。
all_depts = Counter()

for year, header, rows in iter_year_csv(ZIP_PATH):
    # 找到關鍵欄位的索引位置，後續就能用 r[idx] 快速取值。
    dept_idx = header.index("系所名稱")
    entry_idx = header.index("入學方式")

    # len(r) > idx：防止資料列欄位不足時 IndexError。
    by_dept = Counter(r[dept_idx] for r in rows if len(r) > dept_idx)
    by_entry = Counter(r[entry_idx] for r in rows if len(r) > entry_idx)

    summary[year] = {
        "total": len(rows),
        "by_dept": by_dept,
        "by_entry": by_entry,
    }

    # 跨屆統計累加。
    all_depts.update(by_dept)


# ── 終端輸出：總覽 ─────────────────────────────────────
# 1) 六屆總人數
print("\n=== 6 屆新生人數 ===")
for year in sorted(summary):
    print(f"  {year} 學年：{summary[year]['total']:>4} 人")

# 2) 六屆合計最熱門 5 個系所
print("\n=== 全體最熱門 5 個系所（累計 6 屆） ===")
for dept, n in all_depts.most_common(5):
    print(f"  {n:>4} 人  {dept}")

# 3) 114 學年入學方式分布
print("\n=== 114 學年入學方式分布 ===")
if "114" in summary:
    for kind, n in summary["114"]["by_entry"].most_common():
        print(f"  {n:>4} 人  {kind}")


# ── 5.19 + 5.5 + 5.2 沙箱產生報告、5.21 存快照 ─────────
with tempfile.TemporaryDirectory() as tmp:
    # tmp 是字串路徑，先轉 Path 方便後續 / 運算子組路徑。
    tmp = Path(tmp)

    # A. 5.21 用 pickle 保存整個 summary（可快速回復 Python 物件）。
    snap = tmp / "summary.pkl"
    with open(snap, "wb") as f:
        pickle.dump(summary, f)
    print(f"\n快照寫入 {snap.name}：{snap.stat().st_size} bytes")

    # B. 5.5 用 x 模式建立 Markdown 報告，避免不小心覆蓋既有檔案。
    report = tmp / "report.md"
    with open(report, "x", encoding="utf-8") as f:
        # 5.2 使用 print(file=...) 直接把文字輸出到檔案。
        print("# 6 屆新生概況報告\n", file=f)
        print("| 學年 | 人數 | 第一大系所 |", file=f)
        print("|------|------|------------|", file=f)
        for year in sorted(summary):
            top_dept, top_n = summary[year]["by_dept"].most_common(1)[0]
            print(
                f"| {year} | {summary[year]['total']} | "
                f"{top_dept} ({top_n}) |",
                file=f,
            )

    # C. 把報告讀回終端，確認內容正確。
    print("\n=== Markdown 報告預覽 ===")
    print(report.read_text(encoding="utf-8"))

    # D. 驗證 pickle 可讀回，確認序列化成功。
    with open(snap, "rb") as f:
        loaded = pickle.load(f)
    print("pickle 讀回 key:", sorted(loaded.keys()))

# 離開 with 後，tmp 目錄會被自動刪除，不會污染專案資料夾。
print("\n(沙箱已自動清理)")


# ── 課堂延伸挑戰 ───────────────────────────────────────
# 1) 把報告改寫到 HERE / report.md（改用 w 會覆蓋，x 會報錯）。
# 2) 加一欄女性比例：找出性別欄位後用 Counter 統計。
# 3) 把 summary 壓縮存成 summary.pkl.gz（gzip.open('wb') + pickle.dump）。
# 4) 跨屆找出人數逐年下降最明顯的系所（把 by_dept 按年排成折線）。
