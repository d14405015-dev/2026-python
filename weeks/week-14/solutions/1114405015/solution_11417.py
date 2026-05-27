"""
題目 11417：GCD（最大公因數）之和
計算所有 1 ≤ i < j ≤ N 的數對的 GCD 總和
"""

import math


def calculate_gcd_sum(n):
    """
    計算所有 1 ≤ i < j ≤ N 的數對的 GCD 之和。
    
    參數：
        n: 正整數 N（2 ≤ N ≤ 500）
    
    回傳：
        所有 GCD 的總和
    """
    # 初始化總和為 0
    total = 0
    
    # 外層迴圈：i 從 1 到 N-1
    for i in range(1, n):
        # 內層迴圈：j 從 i+1 到 N
        for j in range(i + 1, n + 1):
            # 計算 GCD(i, j) 並累加到總和
            total += math.gcd(i, j)
    
    return total


def solve():
    """
    主程序：讀取輸入並計算 GCD 總和。
    """
    # 持續讀取輸入直到 N = 0
    while True:
        # 讀取一個正整數 N
        n = int(input())
        
        # 如果 N = 0，結束程式
        if n == 0:
            break
        
        # 計算 GCD 總和
        result = calculate_gcd_sum(n)
        
        # 輸出結果
        print(result)


if __name__ == "__main__":
    solve()
