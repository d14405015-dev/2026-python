# R2. 解包數量不固定：星號解包（1.2）

def drop_first_last(grades):
    # 這行是「星號解包」的核心示範：
    # - first 會拿到第一個元素
    # - last 會拿到最後一個元素
    # - *middle 會拿到中間所有元素（型別一定是 list）
    #
    # 例如 grades = [98, 87, 92, 85, 90]
    # -> first=98, middle=[87, 92, 85], last=90
    first, *middle, last = grades

    # 這個函式要做的是：忽略頭尾成績，只計算中間成績平均
    # sum(middle) 是中間成績總和
    # len(middle) 是中間成績筆數
    # 注意：若 grades 長度太短，middle 可能為空，會有除以 0 的風險
    return sum(middle) / len(middle)


# 另一個星號解包範例：資料欄位數不固定
record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')

# 前兩個欄位固定解包給 name / email
# 其餘欄位（可能 0 個、1 個或多個）全部收進 phone_numbers
# phone_numbers 會是 list，不是 tuple
name, email, *phone_numbers = record


# 星號也可以放在最前面：
# - current 取得最後一個元素（例如目前值）
# - trailing 取得前面所有元素（例如歷史資料）
# 同樣地，trailing 的型別會是 list
*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
