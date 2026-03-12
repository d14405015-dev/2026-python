# R8. 字典運算：min/max/sorted + zip（1.8）

# 字典資料：key 是股票代號，value 是價格
prices = {'ACME': 45.23, 'AAPL': 612.78, 'FB': 10.75}

# zip(prices.values(), prices.keys()) 會產生 (price, name) 形式的配對，
# 例如 (45.23, 'ACME')、(612.78, 'AAPL')...
#
# 這樣做的好處：
# - min / max 會先比較 tuple 的第一欄（也就是價格）
# - 因此可以直接找出最便宜 / 最貴
#
# 回傳值是 tuple，不是單純 key 或 value。
min(zip(prices.values(), prices.keys()))
max(zip(prices.values(), prices.keys()))

# sorted(...) 會把所有 (price, name) 配對依價格由小到大排序
# 回傳值是 list[tuple]
sorted(zip(prices.values(), prices.keys()))


# 另一種寫法：直接在 key 上做 min，比較依據是 prices[k]
# 這一行回傳的是「key」（股票代號），不是 (價格, 代號) tuple
# 例如結果會是 'FB'
min(prices, key=lambda k: prices[k])  # 回傳 key
