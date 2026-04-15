# U04. 數字精度的陷阱與選擇（3.1–3.7）
# 銀行家捨入 / NaN 比較陷阱 / float vs Decimal 選擇
#
# 本檔案重點：
# 1. Python 內建 round() 採用「銀行家捨入」（五取偶）。
# 2. NaN 不可用 == 判斷，必須使用 math.isnan()。
# 3. float 與 Decimal 各有取捨：速度 vs 精確度。

import math
import timeit
from decimal import Decimal, ROUND_HALF_UP

# ── 銀行家捨入（3.1）─────────────────────────────────
# Python round() 用「四捨六入五取偶」，不是日常四捨五入
# 當剛好落在 .5 時，會往最接近的「偶數」捨入，目的是降低整體偏差
print(round(0.5))  # 0（不是 1！）
print(round(2.5))  # 2（不是 3！）
print(round(3.5))  # 4


# 若需傳統四捨五入，用 Decimal + ROUND_HALF_UP
def trad_round(x: float, n: int = 0) -> Decimal:
    # 先轉成 str 再交給 Decimal，可避免直接吃到 float 的二進位誤差
    d = Decimal(str(x))
    # 依小數位數 n 建立量化模板：
    # n=0 -> Decimal('1')，n=2 -> Decimal('0.00')
    fmt = Decimal("1") if n == 0 else Decimal("0." + "0" * n)
    # ROUND_HALF_UP：傳統四捨五入（5 一律進位）
    return d.quantize(fmt, rounding=ROUND_HALF_UP)


print(trad_round(0.5))  # 1
print(trad_round(2.5))  # 3

# ── NaN 無法用 == 比較（3.7）─────────────────────────
# IEEE 754 規範：NaN 與任何值比較都為 False（包含自己）
c = float("nan")
print(c == c)  # False（自己不等於自己！）
print(c == float("nan"))  # False
# 唯一可靠做法：用 math.isnan() 檢查
print(math.isnan(c))  # True（唯一正確的檢測方式）

data = [1.0, float("nan"), 3.0, float("nan"), 5.0]
# 實務清理流程：先過濾 NaN，再做統計或運算，避免污染結果
clean = [x for x in data if not math.isnan(x)]
print(clean)  # [1.0, 3.0, 5.0]

# ── float vs Decimal 選擇（3.2）──────────────────────
# float：快但有誤差（科學/工程適用）
# 十進位小數在二進位浮點常無法精確表示，因此會看到尾差
print(0.1 + 0.2)  # 0.30000000000000004
print(0.1 + 0.2 == 0.3)  # False

# Decimal：精確但慢（金融/會計適用）
# Decimal 以十進位模型運算，適合金額與對帳等精度敏感情境
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))  # True

# 簡單效能比較：同樣次數下，Decimal 通常明顯慢於 float
t1 = timeit.timeit(lambda: 0.1 * 999, number=100_000)
t2 = timeit.timeit(lambda: Decimal("0.1") * 999, number=100_000)
print(f"float: {t1:.3f}s  Decimal: {t2:.3f}s（Decimal 約慢 {t2 / t1:.0f} 倍）")
