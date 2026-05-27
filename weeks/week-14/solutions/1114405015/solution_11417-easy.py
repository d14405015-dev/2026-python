"""
題目 11417：GCD 簡化版本
計算所有 1 ≤ i < j ≤ N 的數對的 GCD 之和（簡化邏輯、易於理解）
"""

import math

# 持續讀取輸入直到遇到 0
while True:
    # 讀取一個正整數 N
    n = int(input())
    
    # 如果 N = 0，結束程式
    if n == 0:
        break
    
    # 初始化總和為 0
    total = 0
    
    # 外層迴圈：i 從 1 到 N-1
    for i in range(1, n):
        # 內層迴圈：j 從 i+1 到 N
        for j in range(i + 1, n + 1):
            # 計算 GCD(i, j) 並累加到總和
            total += math.gcd(i, j)
    
    # 輸出結果
    print(total)
