"""
UVA 10008 字母頻率統計 ─ 簡單好記版

【口訣記憶法】
  1. 數：用字典統計每個字母出現幾次（大小寫當同一個）
  2. 排：次數多的排前面；次數一樣時，字母順序小的排前面
  3. 印：只印有出現過的字母

【關鍵技巧】
  Python 的 sorted() 可以傳 key=(-次數, 字母) 一次搞定兩層排序！
  負號讓次數「降序」，字母字串本身就是「升序」。
"""

import sys


def main():
    data = sys.stdin.read().splitlines()

    n = int(data[0])        # 步驟 0：讀取列數
    lines = data[1: n + 1]  # 取密文的 n 列

    # 步驟 1：數——統計所有字母（大小寫轉成大寫統一計算）
    counts = {}  # 字典：{'A': 3, 'B': 1, ...}
    for line in lines:
        for ch in line:
            if ch.isalpha():           # 只處理字母，忽略數字與空白
                letter = ch.upper()    # 大小寫統一為大寫
                counts[letter] = counts.get(letter, 0) + 1  # 次數加 1

    # 步驟 2：排——(-次數, 字母) 作為排序鍵
    # -次數：負號讓次數大的排前（降序）
    # 字母：字母相同次數時，A 在 B 之前（升序）
    sorted_letters = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    # 步驟 3：印——逐行輸出「字母 次數」
    for letter, count in sorted_letters:
        print(f"{letter} {count}")


if __name__ == '__main__':
    main()
