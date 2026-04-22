"""UVA 10268（課堂版本）- easy 記憶版

這題是經典的「雞蛋掉落問題」。

好記口訣：
1. 不要直接問「最少幾次測 n 層」
2. 改問「給 t 次、k 顆球，最多能測幾層」
3. 用公式一路長大到 >= n 為止

核心公式：
F(t, k) = F(t-1, k-1) + F(t-1, k) + 1

- 左邊：這次丟球後破掉（樓下）
- 右邊：這次丟球後沒破（樓上）
- +1：本次測試的當前樓層
"""

MORE_TEXT = "More than 63 trials needed."


def read_cases(text: str):
    """讀入所有測資，遇到 k=0 結束。"""

    res = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        k, n = map(int, line.split())
        if k == 0:
            break
        res.append((k, n))

    return res


def solve_one(k: int, n: int):
    """解單筆測資。"""

    if n <= 0:
        return "0"

    # dp[e] = 目前試了 t 次後，e 顆球可覆蓋的最大樓層數
    dp = [0] * (k + 1)

    # 題目上限：如果超過 63 次就輸出固定文字
    for t in range(1, 64):
        # 從大到小更新，保留上一輪值
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1

        if dp[k] >= n:
            return str(t)

    return MORE_TEXT


def solve(text: str) -> str:
    """對外介面。"""

    out = []
    for k, n in read_cases(text):
        out.append(solve_one(k, n))

    return "\n".join(out)


def main():
    import sys

    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
