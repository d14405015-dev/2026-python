# U06. 時區操作最佳實踐：UTC 優先（3.16）
# 為什麼？本地時間有夏令時跳躍問題，內部計算應一律用 UTC
#
# 本檔案重點：
# 1. 夏令時 (DST) 在邊界時間會造成時間跳躍或重複。
# 2. 直接在本地時間計算可能產生不存在的時間（如 2:15 被跳過）。
# 3. UTC 沒有 DST，內部計算應優先用 UTC，最後才轉回本地顯示。
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

utc = ZoneInfo("UTC")
central = ZoneInfo("America/Chicago")

# 問題：直接在本地時間加減，夏令時邊界會出錯
# 美國 2013-03-10 凌晨 2:00 時鐘往前撥一小時（夏令時開始）
# 於是 2:00~2:59 這一小時被「跳過」，時間直接跳到 3:00
local_dt = datetime(2013, 3, 10, 1, 45, tzinfo=central)
wrong = local_dt + timedelta(minutes=30)
print(f"錯誤結果：{wrong}")  # 2:15（不存在的時間！）

# 正確做法：先轉 UTC 計算，再轉回本地
# astimezone(utc)：把本地時間轉成等價的 UTC 時間
utc_dt = local_dt.astimezone(utc)
# 在 UTC 中進行加法（無 DST 干擾）
correct = utc_dt + timedelta(minutes=30)
# 最後再轉回本地時間顯示
print(f"正確結果：{correct.astimezone(central)}")  # 3:15（跳過了 2:xx）

# 最佳實踐：輸入→UTC→計算→輸出時轉本地
# 步驟 1：使用者輸入通常是不含時區的字串
user_input = "2012-12-21 09:30:00"
# 步驟 2：加上本地時區資訊
naive = datetime.strptime(user_input, "%Y-%m-%d %H:%M:%S")
# 步驟 3：把本地時間轉成 UTC（内部統一用 UTC 存儲）
aware = naive.replace(tzinfo=central).astimezone(utc)
print(f"存 UTC：{aware}")
# 步驟 4：顯示時根據目標時區轉換
print(f"顯示台北：{aware.astimezone(ZoneInfo('Asia/Taipei'))}")
