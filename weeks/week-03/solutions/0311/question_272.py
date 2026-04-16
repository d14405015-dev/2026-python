"""
UVA 272 - TEX Quotes

題意重點：
- 將輸入中的普通雙引號 ", 依出現順序交替替換成：
  1) 開始引號：``
  2) 結束引號：''
- 其他字元（包含換行）都必須完全保留。

這是標準版：
- 使用明確函式切分流程
- 便於閱讀與測試
"""

from __future__ import annotations

import sys


def transform_tex_quotes(text: str) -> str:
    """把普通雙引號轉成 TeX 方向性雙引號。

    規則：
    - 第一個遇到的 ": 替換為 ``
    - 第二個遇到的 ": 替換為 ''
    - 第三個再回到 ``，依此交替

    注意：
    - 題目保證整體雙引號數量為偶數。
    - 只替換字元 ", 其他字元原樣保留。
    """
    result: list[str] = []

    # open_quote = True 表示下一個 " 應該是「開引號」``
    open_quote = True

    for ch in text:
        if ch == '"':
            if open_quote:
                result.append("``")
            else:
                result.append("''")
            open_quote = not open_quote
        else:
            result.append(ch)

    return "".join(result)


def main() -> None:
    """程式進入點：讀取 stdin，轉換後直接輸出。"""
    data = sys.stdin.read()
    output = transform_tex_quotes(data)
    # 使用 end="" 才不會多印額外換行，完整保留原始換行結構
    print(output, end="")


if __name__ == "__main__":
    main()
