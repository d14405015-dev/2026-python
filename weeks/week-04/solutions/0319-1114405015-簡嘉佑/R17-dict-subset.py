# R17. 字典子集（1.17）

# 原始股價字典：鍵是股票代號，值是價格
prices = {'ACME': 45.23, 'AAPL': 612.78, 'IBM': 205.55}
# 用字典推導式建立子集：只保留價格大於 200 的項目
p1 = {k: v for k, v in prices.items() if v > 200}

# 技術股代號集合（用於條件比對）
tech_names = {'AAPL', 'IBM'}
# 建立另一個子集：只保留鍵存在於 tech_names 的項目
p2 = {k: v for k, v in prices.items() if k in tech_names}
