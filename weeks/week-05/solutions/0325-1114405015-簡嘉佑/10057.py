"""UVA 10057 - A Weird Calculator

題意：給定 n 個無號整數 X1, X2, ..., Xn，
     找一個整數 A 使下式最小：
       |X1-A| + |X2-A| + ... + |Xn-A|

     對每組測資輸出一行，含三個整數（空白分隔）：
       A    ─ 使算式最小的整數（多個可行值時取最小）
       cnt  ─ 陣列中等於 A 的元素個數（即最小差為 0 的個數）
       poss ─ 使算式最小的整數 A 共有幾種

數學原理：絕對偏差總和在「中位數」處達到最小值。
  排序後以 0-indexed 標記：
    下中位數索引 lower = (n-1) // 2
    上中位數索引 upper = n // 2
  ‧ n 奇數：lower == upper，A 唯一，poss = 1。
  ‧ n 偶數：lower < upper，任何介於 X[lower]～X[upper] 的整數都可行，
            poss = X[upper] - X[lower] + 1。

輸入格式：多組測資到 EOF；每組先讀 n，再讀 n 個整數。
"""

import sys


def compute(xs: list[int]) -> tuple[int, int, int]:
    """對一組已讀入的陣列計算三個輸出值。

    Args:
        xs: 原始（未排序）整數陣列

    Returns:
        (a, cnt, poss)
        a    : 下中位數（最小可行 A）
        cnt  : 陣列中等於 a 的元素個數
        poss : 可行 A 的整數種數
    """
    xs.sort()       # 排序後才能用索引取中位數
    n = len(xs)

    # 下中位數索引：n=1→0, n=2→0, n=3→1, n=4→1, n=5→2
    lower = (n - 1) // 2
    # 上中位數索引：n=1→0, n=2→1, n=3→1, n=4→2, n=5→2
    upper = n // 2

    a = xs[lower]                           # 可行 A 的最小值
    cnt = xs.count(a)                       # 等於 a 的元素個數（最小差為 0）
    poss = xs[upper] - xs[lower] + 1        # 可行 A 共幾種整數

    return a, cnt, poss


def solve(data: str) -> str:
    """解析全部輸入並組合輸出字串。

    使用 token 方式讀取，對任意換行格式都有容錯能力。
    """
    tokens = data.split()
    idx = 0
    results: list[str] = []

    while idx < len(tokens):
        n = int(tokens[idx]); idx += 1          # 陣列長度

        # 讀取 n 個元素
        xs = [int(tokens[idx + k]) for k in range(n)]
        idx += n

        a, cnt, poss = compute(xs)
        results.append(f"{a} {cnt} {poss}")

    return "\n".join(results)


def main() -> None:
    """從 stdin 一次讀入所有輸入，輸出每組結果到 stdout。"""
    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
