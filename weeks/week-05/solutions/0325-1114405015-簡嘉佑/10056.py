"""UVA 10056 - What is the Probability?

題意：N 個玩家輪流擲骰子，每次成功機率為 p。
     依序 1, 2, ..., N, 1, 2, ... 輪流，第一個成功者獲勝。
     求第 i 個玩家的獲勝機率，輸出 4 位小數。

數學推導：
  設 q = 1 - p（單次失敗機率）。

  玩家 i 在第 k 輪（k = 0, 1, 2, ...）獲勝的機率：
    → 前面 (k*N + i-1) 次全部失敗，再由玩家 i 成功
    → q^(k*N + i-1) * p

  對所有輪次加總（等比級數，公比 r = q^N < 1）：
    P = q^(i-1) * p * (1 + q^N + q^(2N) + ...)
      = q^(i-1) * p / (1 - q^N)

  特殊情況：p = 1 時，玩家 1 機率為 1，其餘為 0。
"""

import sys


def win_prob(n: int, p: float, i: int) -> float:
    """計算第 i 個玩家的獲勝機率。

    Args:
        n: 玩家總數
        p: 單次成功機率
        i: 指定玩家序號（1-indexed）

    Returns:
        玩家 i 的獲勝機率
    """
    # q 是「這次擲骰子失敗」的機率，即 1 減去成功機率。
    q = 1.0 - p

    # 特殊情況：p = 1 代表每次擲一定成功。
    # 第 1 個玩家在第一輪就必然獲勝，其他玩家永遠輪不到，機率為 0。
    if p >= 1.0:
        return 1.0 if i == 1 else 0.0

    # ── 等比級數推導 ──────────────────────────────────────────────
    # 玩家 i 在「第 0 輪」獲勝：前面 (i-1) 人都失敗，玩家 i 成功
    #   機率 = q^(i-1) * p
    #
    # 玩家 i 在「第 1 輪」獲勝：第 0 輪 N 個人全失敗（機率 q^N），
    #   再重複上述情境
    #   機率 = q^N * q^(i-1) * p
    #
    # 依此類推，各輪機率形成公比 r = q^N 的等比級數，
    # 無窮加總（|r| < 1 時收斂）：
    #   P = q^(i-1) * p * (1 + q^N + q^(2N) + ...)
    #     = q^(i-1) * p / (1 - q^N)
    return (q ** (i - 1)) * p / (1.0 - q ** n)


def solve(data: str) -> str:
    """解析所有輸入並組合輸出字串。

    先把整個輸入切分成 token 串列，再用 idx 指標依序讀取，
    這樣不用逐行解析，對各種空白/換行格式都有容錯能力。
    """
    # 把整個輸入切成數字 token，方便依序讀取。
    tokens = data.split()
    idx = 0

    # 第一個數字是測試組數 S。
    s = int(tokens[idx]); idx += 1

    results = []
    for _ in range(s):
        # 每組輸入依序讀取：玩家數 N、成功機率 p、指定玩家序號 i。
        n = int(tokens[idx]);   idx += 1  # 玩家總數（N ≤ 1000）
        p = float(tokens[idx]); idx += 1  # 每次成功機率（0 < p ≤ 1）
        i = int(tokens[idx]);   idx += 1  # 要查詢的玩家序號（1 ≤ i ≤ N）

        # 呼叫 win_prob 取得機率，再格式化成 4 位小數。
        prob = win_prob(n, p, i)
        results.append(f"{prob:.4f}")

    # 每組答案各佔一行，用換行符號串接。
    return "\n".join(results)


def main() -> None:
    """程式進入點：從 stdin 讀取所有輸入，計算後輸出到 stdout。

    一次讀入全部資料（sys.stdin.read()），
    比逐行 input() 效率更高，也是 OJ 題目的常見做法。
    """
    data = sys.stdin.read()
    print(solve(data))


if __name__ == "__main__":
    main()
