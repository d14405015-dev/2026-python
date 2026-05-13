"""
========================================================
題目：UVA 10931 — Parity（奇偶性）
來源：ZeroJudge a924
========================================================

【問題概述】
  給定一個整數 I（1 ≤ I ≤ 2,147,483,647）
  1. 將其轉換為二進位表示（不含前導零）
  2. 計算二進位中 1 的個數
  3. 輸出該整數的「奇偶性」（漢明重量）

【奇偶性定義】
  整數的「奇偶性（Parity）」= 其二進位表示中 1 的個數
  也稱為「Hamming Weight」或「Population Count」

【輸出格式】
  The parity of {二進位字串} is {1的個數} (mod 2).

【例子計算】
  1 的二進位：1          → 1 個 1
  2 的二進位：10         → 1 個 1
  10 的二進位：1010      → 2 個 1
  21 的二進位：10101     → 3 個 1
"""


def get_binary_representation(n: int) -> str:
    """
    將十進位整數 n 轉換為二進位字串表示（不含 "0b" 前綴）
    
    Python 的 bin() 函式返回 "0b..." 格式
    我們去掉前 2 個字元得到純二進位字串
    
    Args:
      n (int): 十進位整數（1 ≤ n ≤ 2,147,483,647）
    
    Returns:
      str: 二進位表示，不含前導零
           例如：1 → "1", 2 → "10", 10 → "1010", 21 → "10101"
    
    時間複雜度: O(log n)，因為二進位字串長度是 log₂(n)
    """
    return bin(n)[2:]  # bin(n) 返回 "0b...", 取 [2:] 去掉 "0b"


def count_ones_in_binary(n: int) -> int:
    """
    計算整數 n 的二進位表示中 1 的個數（漢明重量）
    
    Python 的 bin() 將整數轉為二進位字串
    然後計算該字串中 '1' 字元的個數
    
    Args:
      n (int): 十進位整數（1 ≤ n ≤ 2,147,483,647）
    
    Returns:
      int: 二進位表示中 1 的個數
           例如：1 → 1, 2 → 1, 3 → 2, 10 → 2, 21 → 3
    
    時間複雜度: O(log n)
    
    備註：
      Python 也提供 int.bit_count() 方法（Python 3.10+）
      但使用 bin().count('1') 更通用
    """
    return bin(n).count('1')


def solve(n: int) -> str:
    """
    主要求解函式
    
    功能：
      1. 取得整數 n 的二進位表示
      2. 計算二進位中 1 的個數
      3. 格式化並返回輸出字串
    
    Args:
      n (int): 十進位整數輸入
    
    Returns:
      str: 格式化的輸出字串
           格式："The parity of {二進位} is {1的個數} (mod 2)."
           例如："The parity of 1010 is 2 (mod 2)."
    
    時間複雜度: O(log n)
    """
    # 取得二進位表示
    binary_repr = get_binary_representation(n)
    
    # 計算 1 的個數
    parity_count = count_ones_in_binary(n)
    
    # 格式化輸出
    return f"The parity of {binary_repr} is {parity_count} (mod 2)."


def main():
    """
    主程式入口
    
    流程：
      1. 不斷讀取整數
      2. 若為 0，終止程式
      3. 否則輸出該整數的奇偶性判斷結果
      4. 重複直到輸入 0
    """
    while True:
        # 讀取一行輸入
        line = input().strip()
        
        # 轉換為整數
        n = int(line)
        
        # 若為 0，終止
        if n == 0:
            break
        
        # 輸出結果
        print(solve(n))


if __name__ == "__main__":
    main()
