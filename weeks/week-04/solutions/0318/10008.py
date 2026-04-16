"""
UVA 10008 / ZeroJudge a001：密文字母頻率統計

解題核心思路
────────────
1. 讀取 n 列文字，將所有字元轉為大寫後只保留 A–Z。
2. 用長度 26 的計數陣列累加每個字母的出現次數。
3. 排序規則：次數由大到小；次數相同時，按字母順序（A < B < … < Z）。
4. 只輸出出現過（次數 > 0）的字母。
"""

import sys


def count_letters(lines: list[str]) -> list[int]:
    """
    統計 lines 中 A–Z 各字母的出現次數（大小寫不分）。

    回傳長度 26 的整數列表，index 0 對應 A，index 25 對應 Z。
    """
    counts = [0] * 26  # 初始化 26 個字母的計數器，全為 0

    for line in lines:
        for ch in line:
            if ch.isalpha():
                # 將字母轉大寫後計算其在 A–Z 中的位置
                counts[ord(ch.upper()) - ord('A')] += 1

    return counts


def sorted_result(counts: list[int]) -> list[tuple[str, int]]:
    """
    將計數結果排序：
    - 主排序：次數由大到小（降序）
    - 副排序：字母由小到大（升序，即 A 優先）
    - 過濾掉次數為 0 的字母

    回傳 (字母字串, 次數) 的排序列表。
    """
    result = []
    for i, count in enumerate(counts):
        if count > 0:
            letter = chr(ord('A') + i)  # index 轉回字母
            result.append((letter, count))

    # Python 的 sort 是穩定排序，先按字母升序排（副排序條件），
    # 再按次數降序排（主排序條件），即可達到題目要求。
    result.sort(key=lambda x: x[0])           # 先按字母排序（A→Z）
    result.sort(key=lambda x: x[1], reverse=True)  # 再按次數降序排（穩定，不破壞字母序）

    return result


def main():
    data = sys.stdin.read().splitlines()

    if not data:
        return

    n = int(data[0])          # 第一列：接下來有幾列密文
    lines = data[1: n + 1]    # 取接下來的 n 列（可能含空行）

    counts = count_letters(lines)
    sorted_letters = sorted_result(counts)

    for letter, count in sorted_letters:
        print(f"{letter} {count}")


if __name__ == '__main__':
    main()
