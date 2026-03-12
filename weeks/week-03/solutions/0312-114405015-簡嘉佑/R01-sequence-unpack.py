# R1. 序列解包（1.1）
#
# 什麼是「序列解包（unpacking）」？
# - 當右邊是一個「可迭代的序列」（例如 tuple、list）時，
#   可以把它的每個元素一次指派給左邊多個變數。
# - 左邊變數數量通常要和右邊元素數量一致，否則會噴 ValueError。

# 範例 1：最基本的 tuple 解包
p = (4, 5)
# 把 p 的第 1 個值給 x、第 2 個值給 y
x, y = p
# 執行後：x == 4, y == 5


# 範例 2：list 中混合不同型別資料
data = ['ACME', 50, 91.1, (2012, 12, 21)]
# data[0] -> 公司名稱（字串）
# data[1] -> 股數（整數）
# data[2] -> 價格（浮點數）
# data[3] -> 日期（tuple）

# 第一次解包：先把日期整包接成一個 date 變數
name, shares, price, date = data
# 執行後：
# name   == 'ACME'
# shares == 50
# price  == 91.1
# date   == (2012, 12, 21)

# 第二次解包：直接做「巢狀解包」
# 也就是把第 4 個元素 (2012, 12, 21) 再拆成 year, mon, day
name, shares, price, (year, mon, day) = data
# 執行後：year == 2012, mon == 12, day == 21


# 範例 3：丟棄不需要的欄位
# 慣例上會用底線 _ 當作「我不打算使用這個值」的占位符。
# 這行表示：只拿中間兩個值 shares、price，前後值都忽略。
_, shares, price, _ = data
