# R11. 命名切片 slice（1.11）

# 這是一筆「固定欄位寬度」的文字紀錄（fixed-width record）。
# 不同欄位被放在字串的固定位置上。
record = '....................100 .......513.25 ..........'

# slice(start, stop) 代表切 [start:stop]（含 start，不含 stop）。
# 這裡把「股數」欄位位置命名成 SHARES，
# 好處是後面讀程式時比直接寫 [20:23] 更清楚。
SHARES = slice(20, 23)

# 同理，PRICE 代表價格欄位在字串中的位置。
PRICE = slice(31, 37)

# 取出股數與價格後，先做型別轉換再計算成本：
# - record[SHARES] -> 例如 '100'，轉成 int
# - record[PRICE]  -> 例如 '513.25'，轉成 float
# 最後 cost = 股數 * 價格
cost = int(record[SHARES]) * float(record[PRICE])
