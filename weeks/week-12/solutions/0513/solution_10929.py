"""
========================================================
題目：UVA 10929 — 11 的倍數判斷
來源：ZeroJudge a922
========================================================

【問題概述】
  給定一個最多 1000 位的正整數 N（以字串形式存儲）
  判斷 N 是否為 11 的倍數

【11 的倍數判斷法則】
  若一個整數為 11 的倍數，則其「奇數位數字之和」與「偶數位數字之和」
  的差，也是 11 的倍數（可以是負數、0、或正數）

【位數計數方式（從右到左）】
  以 "12345" 為例：
    位置  5 4 3 2 1
    數字  1 2 3 4 5
  位 1, 3, 5 為奇數位（從右計）
  位 2, 4 為偶數位（從右計）
"""


def is_multiple_of_11(n_str: str) -> bool:
    """
    判斷字串 n_str 是否為 11 的倍數
    
    演算法：
      1. 從右到左（逆序）遍歷每一位數字
      2. 奇數位（第 1, 3, 5...位）的數字相加 → odd_sum
      3. 偶數位（第 2, 4, 6...位）的數字相加 → even_sum
      4. 檢查 (odd_sum - even_sum) 是否為 11 的倍數
      
    Args:
      n_str (str): 正整數的字串表示
    
    Returns:
      bool: True 若 n_str 為 11 的倍數，否則 False
    
    時間複雜度: O(n)，其中 n 是字串長度
    空間複雜度: O(1)，只使用固定空間
    """
    odd_sum = 0      # 奇數位（第 1, 3, 5... 位）數字之和
    even_sum = 0     # 偶數位（第 2, 4, 6... 位）數字之和
    
    # 從右到左逐位掃描（逆序）
    # enumerate(reversed(n_str)) 給出位置和對應的數字
    for position, digit_char in enumerate(reversed(n_str)):
        # 將字元轉換為整數
        digit = int(digit_char)
        
        # position 是 0-indexed 的逆序位置，所以：
        # position 0, 2, 4... 對應原數的位 1, 3, 5...（奇數位）
        # position 1, 3, 5... 對應原數的位 2, 4, 6...（偶數位）
        if position % 2 == 0:
            # 奇數位
            odd_sum += digit
        else:
            # 偶數位
            even_sum += digit
    
    # 判斷差是否為 11 的倍數
    # 若差能被 11 整除，則該數是 11 的倍數
    diff = odd_sum - even_sum
    return diff % 11 == 0


def solve(n_str: str) -> str:
    """
    主要求解函式，返回格式化後的判斷結果
    
    Args:
      n_str (str): 正整數的字串表示
    
    Returns:
      str: 格式化的字串，表示是否為 11 的倍數
           格式: "N is a multiple of 11." 或 "N is not a multiple of 11."
    """
    if is_multiple_of_11(n_str):
        return f"{n_str} is a multiple of 11."
    else:
        return f"{n_str} is not a multiple of 11."


def main():
    """
    主程式入口
    
    流程：
      1. 讀取輸入的整數字串
      2. 若輸入為 "0"，代表終止
      3. 否則輸出該數的判斷結果
      4. 重複直到輸入 "0"
    """
    while True:
        # 讀取一行標準輸入
        line = input().strip()
        
        # 若為 "0"（終止符），結束程式
        if line == "0":
            break
        
        # 否則輸出判斷結果
        print(solve(line))


if __name__ == "__main__":
    main()
