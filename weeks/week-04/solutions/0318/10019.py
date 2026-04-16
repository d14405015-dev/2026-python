"""
UVA 10019（依目前題目檔內容）：Hashmat the Brave Warrior 類型

題意（根據 QUESTION-10019.md 文字）
- 每列輸入有兩個整數 a, b。
- 對每列輸出 |a - b|（正數差值）。
- 輸入直到 EOF。

解題重點
1. 逐行讀取標準輸入。
2. 跳過空白行，避免 split 後長度不足。
3. 解析兩個整數並輸出絕對差。

時間複雜度：O(L)
- L 為輸入行數，每行僅做常數次運算。
"""

import sys


def process_line(line: str) -> int:
    """將單行字串解析為兩整數，回傳其絕對差值。"""
    a_str, b_str = line.split()
    a = int(a_str)
    b = int(b_str)
    return abs(a - b)


def main() -> None:
    """主程式：逐行讀到 EOF，輸出每列兩數差值。"""
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            # 題目通常不會給空行，但保險起見直接忽略。
            continue

        diff = process_line(line)
        print(diff)


if __name__ == "__main__":
    main()
