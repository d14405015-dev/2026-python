# U9. groupby 為何一定要先 sort（1.15）

# 匯入 groupby：依指定鍵把「連續」資料分組
from itertools import groupby
# 匯入 itemgetter：快速取出 dict 的指定欄位值
from operator import itemgetter

# 範例資料：故意讓同日期資料不相鄰
rows = [
    {'date': '07/02/2012', 'x': 1},
    {'date': '07/01/2012', 'x': 2},
    {'date': '07/02/2012', 'x': 3},
]

# 沒排序：07/02 會被分成兩段（因為 groupby 只看「連續」）
for k, g in groupby(rows, key=itemgetter('date')):
    # 轉成 list 方便觀察每個群組內容
    list(g)

# 排序後：同 date 才會連在一起，分組才正確
# 先依 date 排序，讓相同鍵值變成連續區段
rows.sort(key=itemgetter('date'))
for k, g in groupby(rows, key=itemgetter('date')):
    # 此時每個日期只會得到一組完整資料
    list(g)
