"""
題目 11349：對稱矩陣正簡單版本
簡化邏輯、易於理解和記憶
"""

# 讀取測試資料組數
T = int(input())

# 逐個測試案例處理
for test_num in range(1, T + 1):
    # 讀取矩陣大小（格式：N = 3）
    line = input().strip()
    n = int(line.split('=')[1])
    
    # 讀取 n×n 的矩陣
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 檢查是否為對稱矩陣
    is_symmetric = True
    
    # 檢查 1：所有元素都必須非負（≥ 0）
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                is_symmetric = False
                break
        if not is_symmetric:
            break
    
    # 檢查 2：中心對稱性 → M[i][j] = M[n-1-i][n-1-j]
    if is_symmetric:
        for i in range(n):
            for j in range(n):
                # 比較對稱位置的元素
                # [i][j] 和 [n-1-i][n-1-j] 必須相等
                if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                    is_symmetric = False
                    break
            if not is_symmetric:
                break
    
    # 輸出結果
    if is_symmetric:
        print(f"Test #{test_num}: Symmetric.")
    else:
        print(f"Test #{test_num}: Non-symmetric.")
