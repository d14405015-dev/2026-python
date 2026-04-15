# U05. 日期時間的陷阱（3.12–3.15）
# timedelta 不支援月份 / strptime 效能問題
#
# 本檔案重點：
# 1. timedelta 只支援「日」以下單位，月份需自行實現。
# 2. 加月時需處理邊界情況：月份天數不同、年份進位。
# 3. strptime 格式解析相對慢，已知日期格式時可考慮手動解析。

import timeit
import calendar
from datetime import datetime, timedelta

# ── timedelta 不支援月份（3.12）──────────────────────
dt = datetime(2012, 9, 23)
try:
    # timedelta 只支援 days、seconds、microseconds 等固定時間單位
    # 不支援 months 或 years，因為月份天數不固定（28~31 天）
    dt + timedelta(months=1)  # type: ignore[call-arg]
except TypeError as e:
    print(f"TypeError: {e}")  # 'months' is an invalid keyword argument


# 正確做法：用 calendar 取得目標月份天數，並將日期 clamp 到該月最後一天
def add_one_month(dt: datetime) -> datetime:
    # 計算目標年份與月份
    # 例如 2012-01-31 + 1月 -> year=2012, month=2
    year = dt.year
    month = dt.month + 1
    # 處理年份進位：12 月的下一月是下年 1 月
    if month == 13:
        year += 1
        month = 1

    # 計算目標月份的最大天數（考慮閏年）
    # 例如 2 月可能 28 或 29 天
    _, days_in_target_month = calendar.monthrange(year, month)
    # 若原日期是月末（例如 31 日），但目標月份沒那麼多天，
    # 就降到該月最後一天（例如 2 月 29 日或 28 日）
    day = min(dt.day, days_in_target_month)

    # 用 replace 建立新 datetime，月份、年份、日期都更新
    return dt.replace(year=year, month=month, day=day)


# 示例：1 月 31 日 + 1 月 = 2 月的最後一天（閏年 29 日）
print(add_one_month(datetime(2012, 1, 31)))  # 2012-02-29
print(add_one_month(datetime(2012, 9, 23)))  # 2012-10-23

# ── strptime 效能問題（3.15）─────────────────────────
# 準備 336 個日期字串供測試
dates = [f"2012-{m:02d}-{d:02d}" for m in range(1, 13) for d in range(1, 29)]


def use_strptime(s: str) -> datetime:
    # strptime 會解析格式字串並建立 datetime
    # 靈活但涉及正規表示式編譯、多層檢查，成本較高
    return datetime.strptime(s, "%Y-%m-%d")


def use_manual(s: str) -> datetime:
    # 若已知格式固定為 YYYY-MM-DD，直接 split 再轉型通常更快
    y, m, d = s.split("-")
    return datetime(int(y), int(m), int(d))


# 驗證兩種方法結果相同
assert use_strptime("2012-09-20") == use_manual("2012-09-20")

# 簡單效能比較：strptime 通常明顯慢於手動解析
t1 = timeit.timeit(lambda: [use_strptime(d) for d in dates], number=100)
t2 = timeit.timeit(lambda: [use_manual(d) for d in dates], number=100)
print(f"strptime: {t1:.3f}s  手動解析: {t2:.3f}s（快 {t1 / t2:.1f} 倍）")
