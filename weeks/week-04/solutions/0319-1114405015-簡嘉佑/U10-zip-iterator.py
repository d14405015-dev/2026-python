# U10. zip 為何只能用一次（1.8）

# 範例字典：股票代號 -> 價格
prices = {'A': 2.0, 'B': 1.0}
# zip 會回傳迭代器，逐項配對 (value, key)
z = zip(prices.values(), prices.keys())

# 第一次計算最小值時，會把 z 的內容一路讀完
min(z)  # OK（消耗掉迭代器）
# 第二次再用同一個 z 時，已無資料可讀
# max(z)  # 會失敗：因為 z 已經被消耗完
