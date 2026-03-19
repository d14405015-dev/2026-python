# R18. namedtuple（1.18）

# 從 collections 匯入 namedtuple，用來建立具欄位名稱的 tuple 類型
from collections import namedtuple

# 定義 Subscriber 類型，包含 addr 與 joined 兩個欄位
Subscriber = namedtuple('Subscriber', ['addr', 'joined'])
# 建立 Subscriber 實例
sub = Subscriber('jonesy@example.com', '2012-10-19')
# 可用屬性名稱存取欄位值（比純 tuple 索引更易讀）
sub.addr

# 定義 Stock 類型，包含名稱、股數與價格
Stock = namedtuple('Stock', ['name', 'shares', 'price'])
# 建立 Stock 實例
s = Stock('ACME', 100, 123.45)
# namedtuple 不可變，使用 _replace 產生修改後的新實例
s = s._replace(shares=75)
