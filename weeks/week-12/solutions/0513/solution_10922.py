"""
========================================================
題目：UVA 10922 — 2 the 9s
來源：ZeroJudge a915
========================================================

【題目大意】
  判斷一個正整數是否為 9 的倍數。
  若是，計算其「9 的深度（9-degree）」：
    不斷對各位數字加總，直到剩一位數為止，
    加總的次數就是 9 的深度。

【數學原理】
  - 一個數的各位數字之和與該數除以 9 的餘數相同（同餘 mod 9）
  - 若各位和最終為 9，則原數被 9 整除
  - 若各位和最終為 1-8，則不被 9 整除

【輸出格式】
  - 不是 9 的倍數："{X} is not a multiple of 9."
  - 是 9 的倍數  ："9-degree of {X} is {Y}."
"""

import sys


def digit_sum(n_str: str) -> int:
    """
    計算字串表示的數字各位數字之總和。

    參數：
        n_str (str)：數字字串，例如 "18"、"999"

    回傳：
        int：各位數字加總
    """
    return sum(int(ch) for ch in n_str)


def solve(n_str: str) -> str:
    """
    判斷正整數（字串形式）是否為 9 的倍數，並計算 9 的深度。

    參數：
        n_str (str)：輸入正整數（字串，可能非常長）

    回傳：
        str：對應的輸出字串
    """
    current = n_str
    depth = 0

    # 不斷加總各位數字，直到只剩一位數為止
    while len(current) > 1:
        s = digit_sum(current)
        current = str(s)
        depth += 1

    # 最終只剩一位數：若為 9 則是 9 的倍數
    if current == "9":
        return f"9-degree of {n_str} is {depth}."
    else:
        return f"{n_str} is not a multiple of 9."


def main():
    """主程式：讀取標準輸入，依行處理直到遇到 0。"""
    while True:
        line = input().strip()
        if line == "0":
            break
        print(solve(line))


if __name__ == "__main__":
    main()
