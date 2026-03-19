# R16. 過濾：推導式 / generator / filter / compress（1.16）

# 原始數列
mylist = [1, 4, -5, 10]
# 清單推導式：篩出大於 0 的數字（立即產生 list）
[n for n in mylist if n > 0]
# 生成器運算式：同樣篩選大於 0，但延後取值、較省記憶體
pos = (n for n in mylist if n > 0)

# 字串資料中混有非整數內容
values = ['1', '2', '-3', '-', 'N/A']

# 自訂過濾條件：判斷字串是否可轉成整數
def is_int(val):
    try:
        # 可成功轉型代表是整數格式
        int(val); return True
    except ValueError:
        # 轉型失敗表示不是整數
        return False

# filter 會保留讓 is_int 回傳 True 的元素
list(filter(is_int, values))

# compress 依布林遮罩（selectors）保留對應位置元素
from itertools import compress
addresses = ['a1', 'a2', 'a3']
counts = [0, 3, 10]
# 先建立條件遮罩：是否大於 5
more5 = [n > 5 for n in counts]
# 只保留 more5 為 True 的地址
list(compress(addresses, more5))
