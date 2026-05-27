"""
題目 11349：對稱矩陣檢查 (UVA 11349 — Symmetric Matrix)
判斷矩陣是否為對稱矩陣（中心對稱 + 所有元素非負）
"""


def check_symmetric_matrix(matrix, n):
    """
    檢查矩陣是否為對稱矩陣。
    
    對稱矩陣的定義：
    1. 所有元素都是非負數（≥ 0）
    2. 矩陣關於中心點對稱，即 M[i][j] = M[n-1-i][n-1-j]
    
    參數：
        matrix: n×n 的整數矩陣
        n: 矩陣的維度
    
    回傳：
        True 如果是對稱矩陣，False 否則
    """
    # 檢查所有元素是否都是非負數
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                return False
    
    # 檢查中心對稱性：M[i][j] = M[n-1-i][n-1-j]
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                return False
    
    return True


def solve():
    """
    主程序：讀取輸入並判斷每個矩陣是否為對稱矩陣。
    """
    # 讀取測試資料組數
    T = int(input())
    
    # 逐組處理測試資料
    for test_num in range(1, T + 1):
        # 讀取矩陣維度（格式：N = n）
        line = input().strip()  # 例如：N = 3
        n = int(line.split('=')[1].strip())
        
        # 讀取矩陣的 n 行數據
        matrix = []
        for _ in range(n):
            row = list(map(int, input().split()))
            matrix.append(row)
        
        # 檢查矩陣是否為對稱矩陣
        if check_symmetric_matrix(matrix, n):
            print(f"Test #{test_num}: Symmetric.")
        else:
            print(f"Test #{test_num}: Non-symmetric.")


if __name__ == "__main__":
    solve()
