"""UVA 11063 - RGB 轉 XYZ（easy 版本）

這份程式刻意採用「步驟清楚、容易記憶」的寫法：
1. 讀入 n 與 n*n 個像素 (R, G, B)
2. 逐像素套用題目給的線性轉換公式得到 (X, Y, Z)
3. 每個像素輸出一行，數值固定到小數點後 4 位
4. 最後輸出整張影像的平均亮度 Y

重點提醒：
- 題目允許誤差 0.0001，使用 Python 格式化 {value:.4f} 即可符合。
- 平均亮度是所有像素 Y 的平均值，不是 X、Y、Z 三者平均。
"""

from __future__ import annotations

import sys
from typing import List, Tuple


def rgb_to_xyz(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """把一個像素的 RGB 轉成 XYZ。

    公式完全照題目：
    X = 0.5149*R + 0.3244*G + 0.1607*B
    Y = 0.2654*R + 0.6704*G + 0.0642*B
    Z = 0.0248*R + 0.1248*G + 0.8504*B
    """
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return x, y, z


def solve(input_text: str) -> str:
    """處理一整份輸入字串並回傳題目要求的完整輸出字串。"""
    tokens = list(map(int, input_text.split()))
    if not tokens:
        return ""

    idx = 0
    n = tokens[idx]
    idx += 1

    total_pixels = n * n
    y_sum = 0.0
    out_lines: List[str] = []

    # 影像共有 n*n 個像素；每個像素依序讀 3 個整數 (R, G, B)
    for _ in range(total_pixels):
        r = tokens[idx]
        g = tokens[idx + 1]
        b = tokens[idx + 2]
        idx += 3

        x, y, z = rgb_to_xyz(r, g, b)
        y_sum += y

        # 每個像素輸出一行，X Y Z 皆四捨五入到小數點後第 4 位
        out_lines.append(f"{x:.4f} {y:.4f} {z:.4f}")

    # 最後一行輸出平均亮度
    avg_y = y_sum / total_pixels
    out_lines.append(f"The average of Y is {avg_y:.4f}")

    return "\n".join(out_lines)


def main() -> None:
    """線上評測入口：從標準輸入讀資料，將結果印到標準輸出。"""
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
