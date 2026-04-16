"""
UVA 10019（依題目檔內容）簡單好記版

口訣：
1. 讀一行
2. 拆兩個數
3. 印絕對差
4. 重複到 EOF

這題幾乎是最直覺的 I/O 練習題：
- 不需要資料結構
- 不需要排序
- 每行獨立計算即可
"""

import sys


def main() -> None:
    # 一行一行讀到檔尾（EOF）
    for line in sys.stdin:
        line = line.strip()
        if not line:
            # 空白行直接跳過
            continue

        # split() 可自動處理多個空白
        a, b = map(int, line.split())

        # abs(x) 會回傳 x 的絕對值
        print(abs(a - b))


if __name__ == "__main__":
    main()
