# R19. 轉換+聚合：生成器表達式（1.19）

# 原始數列
nums = [1, 2, 3]
# 生成器表達式 + sum：計算每個元素平方後的總和
sum(x * x for x in nums)

# tuple 內容含不同型別
s = ('ACME', 50, 123.45)
# 先把每個元素轉成字串，再用逗號串接
','.join(str(x) for x in s)

# 投資組合資料：每筆都有名稱與持股數
portfolio = [{'name': 'AOL', 'shares': 20}, {'name': 'YHOO', 'shares': 75}]
# 用生成器只取出 shares 欄位，再求最小持股數
min(s['shares'] for s in portfolio)
# 直接在整筆資料上取最小值，回傳 shares 最小的那一筆 dict
min(portfolio, key=lambda s: s['shares'])
