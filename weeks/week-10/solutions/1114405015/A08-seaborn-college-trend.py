# A08. 用 seaborn 畫 109~114 學年各學院生源分析圖
# Bloom: Apply — 把 A07 的統計成果交給視覺化套件
#
# 這支程式的目標：
#   1) 從 zip 壓縮檔讀出 109~114 六屆的 CSV 資料（不解壓）
#   2) 將每筆學生資料依「系所」對應到「學院」，整理成 long-form DataFrame
#   3) 用 seaborn 繪製兩張圖：折線趨勢圖 + 堆疊長條圖
#   4) 輸出圖檔（若已存在則跳過，不覆蓋）
#
# 需要：pip install seaborn matplotlib pandas
#
# 用到的 I/O 技巧延續 A07：
#   5.7  zipfile 不解壓讀 CSV
#   5.1  utf-8-sig 去 BOM
#   5.6  io.StringIO → csv
#   5.11 pathlib
#   5.5  open('x') 不覆蓋輸出檔

# ── 標準函式庫 ────────────────────────────────────────
import csv         # 讀 CSV 格式資料
import io          # io.StringIO：把字串當成檔案物件使用
import platform    # 偵測作業系統，用來選對應的中文字型
import zipfile     # 讀取 zip 壓縮檔（不需要先解壓縮）
from pathlib import Path  # 跨平台路徑操作

# ── 第三方套件 ────────────────────────────────────────
import matplotlib.pyplot as plt  # 底層繪圖框架，控制圖形大小、存檔等
import pandas as pd              # 資料整理與樞紐分析
import seaborn as sns            # 高階統計視覺化套件，基於 matplotlib

# ── 中文字型：依平台挑一個有的 ─────────────────────────
# matplotlib 預設不支援中文，需手動指定系統內建的 CJK 字型。
# 不同作業系統的中文字型名稱不同，這裡依 platform.system() 自動選擇：
#   Darwin  → macOS（Heiti TC / Arial Unicode MS）
#   Windows → Windows（微軟正黑體 / 微軟雅黑）
#   Linux   → Linux（Noto Sans CJK TC）
_CJK_FONTS = {
    "Darwin": ["Heiti TC", "Arial Unicode MS", "PingFang TC"],
    "Windows": ["Microsoft JhengHei", "Microsoft YaHei"],
    "Linux": ["Noto Sans CJK TC", "WenQuanYi Zen Hei"],
}.get(platform.system(), ["sans-serif"])  # 找不到對應平台時退回 sans-serif


def _apply_cjk_font():
    """將 CJK 字型套用到 matplotlib 全域設定。

    為什麼要獨立成函式：
    sns.set_theme() 執行後會重設 rcParams，若不重套一次，
    之後的圖表中文字仍會變成方塊（□□□）。
    因此需要在 sns.set_theme() 之後再呼叫一次此函式。
    """
    # 把 CJK 字型插在清單最前面，確保優先被 matplotlib 選取
    plt.rcParams["font.sans-serif"] = _CJK_FONTS + plt.rcParams["font.sans-serif"]
    plt.rcParams["font.family"] = "sans-serif"
    # 避免負號「-」被畫成方塊（某些字型不含 Unicode 負號）
    plt.rcParams["axes.unicode_minus"] = False


# 程式一開始就先套用一次，確保後續所有圖表都能顯示中文
_apply_cjk_font()

# ── 系所 → 學院 對照表（NPU 三大學院） ─────────────────
# CSV 欄位只有「系所名稱」，沒有「學院」欄位。
# 這裡手動建立一張對照表，讓後續可以把每筆學生資料歸到正確的學院。
# 若系所名稱不在此表中，load_long_frame 會歸類為「其他」。
DEPT_TO_COLLEGE = {
    # 人文暨管理學院（6 個系）
    "應用外語系": "人文暨管理學院",
    "航運管理系": "人文暨管理學院",
    "行銷與物流管理系": "人文暨管理學院",
    "觀光休閒系": "人文暨管理學院",
    "資訊管理系": "人文暨管理學院",
    "餐旅管理系": "人文暨管理學院",
    # 海洋資源暨工程學院（3 個系）
    "水產養殖系": "海洋資源暨工程學院",
    "海洋遊憩系": "海洋資源暨工程學院",
    "食品科學系": "海洋資源暨工程學院",
    # 電資工程學院（3 個系）
    "資訊工程系": "電資工程學院",
    "電信工程系": "電資工程學院",
    "電機工程系": "電資工程學院",
}

# ── 5.11 定位資料 ─────────────────────────────────────
# __file__ 取得目前腳本的路徑，resolve() 確保是絕對路徑，
# .parent 取得所在資料夾，儲存為 HERE 供後續路徑組合使用。
HERE = Path(__file__).resolve().parent


def _find_zip_path(start: Path) -> Path:
    """向上搜尋 assets zip，讓程式搬到別層資料夾也能正常執行。

    搜尋邏輯：
    - 從目前資料夾開始，依序往父層找
    - 直到找到 assets/npu-stu-109-114-anon.zip 為止
    - 若一路找到根目錄都沒有，丟出 FileNotFoundError 提醒使用者
    """
    for parent in [start] + list(start.parents):
        candidate = parent / "assets" / "npu-stu-109-114-anon.zip"
        if candidate.exists():
            return candidate
    # 清楚的錯誤訊息比靜默失敗好，讓使用者知道少了哪個檔案
    raise FileNotFoundError("找不到 assets/npu-stu-109-114-anon.zip")


ZIP_PATH = _find_zip_path(HERE)
print("資料來源:", ZIP_PATH)


# ── 5.7 + 5.6 + 5.1 讀 zip 內所有 CSV 成一張 long-form 表 ─
def load_long_frame(zip_path: Path) -> pd.DataFrame:
    """從 zip 壓縮檔讀出所有 CSV，整理成 pandas long-form DataFrame。

    什麼是 long-form（長表）：
    - 每一列代表一個學生（一筆觀測值）
    - 欄位包含：學年、學院、系所
    - 這種格式最適合搭配 seaborn 做分組統計與視覺化

    回傳的 DataFrame 結構範例：
        學年    學院          系所
        109     人文暨管理學院  觀光休閒系
        109     電資工程學院    資訊工程系
        ...
    """
    records = []  # 收集每筆學生資料，最後一次性轉成 DataFrame
    with zipfile.ZipFile(zip_path) as z:
        for info in z.infolist():
            # 跳過非 CSV 檔（例如說明文件）
            if not info.filename.endswith(".csv"):
                continue

            # 依資料命名規則，檔名前三碼即為學年（如 '109'、'114'）
            year = info.filename[:3]

            # 讀出 bytes 後用 utf-8-sig 解碼，自動去除 Excel 存檔產生的 BOM
            text = z.read(info).decode("utf-8-sig")

            # 用 StringIO 把字串包成類檔案物件，再交給 DictReader
            # DictReader 比 reader 更方便：每列直接是 {欄位名: 值} 的 dict
            reader = csv.DictReader(io.StringIO(text))

            for row in reader:
                dept = row.get("系所名稱", "").strip()
                if not dept:
                    # 系所名稱為空則跳過（可能是格式異常的列）
                    continue
                records.append(
                    {
                        "學年": int(year),  # 字串轉整數，方便後續排序與畫圖軸
                        # 查對照表取學院名，查不到歸類為「其他」
                        "學院": DEPT_TO_COLLEGE.get(dept, "其他"),
                        "系所": dept,
                    }
                )
    # 把所有 records list 一次轉成 DataFrame（比逐筆 append 快）
    return pd.DataFrame.from_records(records)


# 讀入資料並印出基本資訊，確認資料正確載入
df = load_long_frame(ZIP_PATH)
print("總筆數:", len(df))  # 應為 109~114 六屆學生總人數
print(df.head())           # 前 5 筆，確認欄位與內容正確

# 樞紐：各學年 × 各學院 的人數
# groupby + size() = 計算每個（學年, 學院）組合的人數
# reset_index(name='人數') = 把多層索引攤平成一般欄位
# 结果是 long-form：每列代表「某學年某學院有幾人」
pivot = df.groupby(["學年", "學院"]).size().reset_index(name="人數")
print("\n各學年各學院:")
# pivot() 把 long-form 轉成 wide-form，方便人工閱讀（學年為列，學院為欄）
print(pivot.pivot(index="學年", columns="學院", values="人數"))


# ── seaborn 繪圖 ──────────────────────────────────────
# set_theme 設定整體風格：
#   style='whitegrid' → 白底＋灰色格線，清晰易讀
#   context='talk'    → 字體較大，適合簡報展示
#   palette='Set2'    → 柔和的定性色盤，各學院顏色好區分
sns.set_theme(style="whitegrid", context="talk", palette="Set2")
_apply_cjk_font()  # sns.set_theme 會重設字型，需再套一次中文字型

# 建立 1 列 2 欄的子圖版面
# figsize=(15, 6)：圖寬 15 英寸、高 6 英寸
# width_ratios=[1.3, 1]：左圖稍寬，右圖稍窄（折線圖需要更多橫向空間）
fig, axes = plt.subplots(1, 2, figsize=(15, 6), gridspec_kw={"width_ratios": [1.3, 1]})

# 圖 A：折線＋散點 —— 各學院逐年趨勢
# hue='學院' → 用不同顏色區分三個學院
# marker='o' → 每個資料點加上圓形標記
# markersize=10  → 標記大小（較大方便滑鼠 hover 辨識）
# linewidth=2.5  → 線條粗細
sns.lineplot(
    data=pivot,
    x="學年",
    y="人數",
    hue="學院",
    marker="o",
    markersize=10,
    linewidth=2.5,
    ax=axes[0],
)
axes[0].set_title("109–114 各學院新生人數趨勢", fontsize=16, pad=12)
# 強制讓 x 軸只顯示 109~114 這六個整數年份，不自動補其他刻度
axes[0].set_xticks(sorted(pivot["學年"].unique()))
# 取出折線圖的圖例控制點，稍後統一放到圖表上方
handles, labels = axes[0].get_legend_handles_labels()
axes[0].get_legend().remove()  # 移除折線圖內部的圖例

# 在每個資料點正上方標註實際人數，方便讀圖時不必對照 y 軸
# annotate() 比 text() 更彈性，支援 offset points 偏移座標
for _, r in pivot.iterrows():
    axes[0].annotate(
        int(r["人數"]),         # 標籤文字：人數（整數）
        (r["學年"], r["人數"]), # 錨點座標（資料點位置）
        textcoords="offset points",  # 偏移單位為點（非資料座標）
        xytext=(0, 8),          # 向上偏移 8 點，避免遮住標記
        ha="center",            # 水平置中對齊
        fontsize=9,
        alpha=0.8,              # 略透明，不會完全蓋住折線
    )

# 圖 B：堆疊長條 —— 每年學院占比
# 先把 long-form 的 pivot 再次 pivot() 轉成 wide-form，
# 讓每一列是一個學年，每一欄是一個學院的人數，才能畫堆疊圖。
# fillna(0) 處理可能缺失的學年/學院組合（若某年某學院無人則補 0）。
pivot_wide = pivot.pivot(index="學年", columns="學院", values="人數").fillna(0)
# kind='bar'      → 長條圖
# stacked=True    → 堆疊顯示，可同時看各學院人數與總人數
# colormap='Set2' → 與折線圖同色盤，視覺一致
# edgecolor='white' → 各段之間加白色邊框，更容易區分
pivot_wide.plot(kind="bar", stacked=True, ax=axes[1], colormap="Set2", width=0.75, edgecolor="white")
axes[1].set_title("各學年學院結構（堆疊）", fontsize=16, pad=12)
axes[1].set_ylabel("人數")
axes[1].tick_params(axis="x", rotation=0)  # x 軸年份標籤保持水平，不旋轉
axes[1].get_legend().remove()  # 移除堆疊圖內自動產生的圖例

# suptitle：大標題，放在最頂端
fig.suptitle("國立澎湖科技大學  109–114 學年新生生源分析", fontsize=18, fontweight="bold", y=0.99)
# 將學院圖例統一放在大標題下方、兩張子圖上方
# bbox_to_anchor=(0.5, 0.91)：水平置中，y=0.91 在大標題下方稍留間距
# ncol=3：三個學院橫排一列，節省垂直空間
fig.legend(handles, labels, title="學院", loc="upper center",
           bbox_to_anchor=(0.5, 0.91), ncol=3, frameon=True, fontsize=11)
# tight_layout 的 rect 參數保留頂部 18% 空間安置大標題與圖例
fig.tight_layout(rect=[0, 0, 1, 0.82])

# ── 5.5 'x' 模式輸出：檔已存在就保留舊的 ────────────────
# 輸出路徑：與程式同一資料夾下的 A08-college-trend.png
OUT = HERE / "A08-college-trend.png"
try:
    # 'xb' = x 模式（只寫、若檔案已存在則拋出 FileExistsError）+ b（二進位）
    # 用二進位模式開，因為 savefig 直接寫 PNG bytes
    with open(OUT, "xb") as f:
        fig.savefig(f, dpi=150, bbox_inches="tight")  # dpi=150 解析度適中，bbox_inches='tight' 不裁切
    print(f"\n圖檔已寫入：{OUT.name}")
except FileExistsError:
    # 若已存在則不覆蓋，避免誤刪之前已確認好的圖檔
    print(f"\n{OUT.name} 已存在，保留舊檔（要重畫請先刪除）")

# 若在互動環境（Jupyter / 一般視窗）則跳出圖形視窗
# 若在無視窗後端（Agg）執行則此行無效（不會報錯）
plt.show()

# ── 延伸挑戰 ──────────────────────────────────────────
# 1) 改畫「各系所」熱力圖：sns.heatmap(pivot_by_dept, annot=True, fmt='d')
# 2) 加一張圓餅圖：114 學年學院占比
# 3) 把年度 x 軸改成 '109學年'~'114學年' 字串（需轉型 + set_xticklabels）
