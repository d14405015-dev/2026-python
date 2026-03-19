# R15. 分組 groupby（1.15）

# 匯入 groupby：可依照指定鍵值把連續資料分成群組
from itertools import groupby
# 匯入 itemgetter：快速取得 dict 中指定欄位的值（例如 'date'）
from operator import itemgetter

# 範例資料：每筆資料都有日期與地址
rows = [{'date': '07/01/2012', 'address': '...'}, {'date': '07/02/2012', 'address': '...'}]
# 使用 groupby 前要先依同一個 key 排序，才能正確分組
rows.sort(key=itemgetter('date'))

# 依照 date 分組；date 是群組鍵，items 是該日期對應的資料迭代器
for date, items in groupby(rows, key=itemgetter('date')):
    # 逐筆走訪該日期群組中的資料
    for i in items:
        # 目前不做處理，保留給後續實作
        pass
