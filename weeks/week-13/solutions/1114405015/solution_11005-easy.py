"""UVA 11005 - Cheapest Base（容易記憶版本）

解題核心：
1. 對每個查詢數字 N，逐一嘗試 base 2 到 36。
2. 把 N 轉為該進位後，累加每一位數字的印刷成本。
3. 找出最小成本，收集所有達到最小成本的進位。

這份程式同時提供：
- 可被單元測試呼叫的函式：cheapest_bases(costs, n)
- 可直接提交到線上評測的主程式：main()
"""

from __future__ import annotations

from typing import List
import sys


def representation_cost(costs: List[int], n: int, base: int) -> int:
    """計算數字 n 在指定進位 base 的表示成本。

    參數說明：
    - costs: 長度 36 的成本陣列，索引 0~35 分別對應字元 0~9、A~Z。
    - n: 十進位整數（題目範圍允許到 2,000,000,000）。
    - base: 進位制（2~36）。

    特殊情況：
    - 當 n == 0 時，表示法就是單一數字 0，因此成本是 costs[0]。
    """
    if n == 0:
        return costs[0]

    # 使用「反覆除 base 取餘數」的方式分解各位數。
    # 每次 n % base 取得最低位數字，累加其成本後再做 n //= base。
    total = 0
    value = n
    while value > 0:
        digit = value % base
        total += costs[digit]
        value //= base
    return total


def cheapest_bases(costs: List[int], n: int) -> List[int]:
    """回傳數字 n 的所有最低成本進位（2~36，升序）。"""
    best_cost = None
    best_bases: List[int] = []

    # 固定枚舉 2 到 36 進位，邏輯直觀、容易記憶。
    for base in range(2, 37):
        current_cost = representation_cost(costs, n, base)

        # 第一個進位先初始化最佳解。
        if best_cost is None:
            best_cost = current_cost
            best_bases = [base]
            continue

        # 找到更小成本：更新最佳成本並重置最佳進位清單。
        if current_cost < best_cost:
            best_cost = current_cost
            best_bases = [base]
        # 找到同成本：加入並列最佳進位。
        elif current_cost == best_cost:
            best_bases.append(base)

    return best_bases


def parse_input(text: str) -> List[str]:
    """處理 UVA 輸入格式並回傳完整輸出行（含空行）。"""
    tokens = list(map(int, text.split()))
    if not tokens:
        return []

    idx = 0
    t = tokens[idx]
    idx += 1

    out_lines: List[str] = []

    for case_no in range(1, t + 1):
        # 每組測資有 36 個字元成本（題目描述為 4 行、每行 9 個）。
        costs = tokens[idx : idx + 36]
        idx += 36

        q = tokens[idx]
        idx += 1

        out_lines.append(f"Case {case_no}:")

        for _ in range(q):
            n = tokens[idx]
            idx += 1
            bases = cheapest_bases(costs, n)
            bases_text = " ".join(map(str, bases))
            out_lines.append(f"Cheapest base(s) for number {n}: {bases_text}")

        # 題目要求測資與測資之間要有空行。
        if case_no != t:
            out_lines.append("")

    return out_lines


def main() -> None:
    """線上評測進入點：讀 stdin，輸出答案到 stdout。"""
    data = sys.stdin.read()
    lines = parse_input(data)
    if lines:
        sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
