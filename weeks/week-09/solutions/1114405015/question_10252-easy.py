"""UVA 10252（課堂版本）- easy 記憶版

這題其實是「找一個整數點 (px, py) 讓曼哈頓距離總和最小」。
核心口訣：
1. 曼哈頓距離可以拆成 x 與 y 兩個獨立問題
2. 一維絕對值總和最小點是中位數（或中位區間）
3. 方案數 = x 維方案數 * y 維方案數

所以流程很固定：
- 收集全部 x、全部 y
- 各做一次一維最佳化
- 合併答案
"""


def read_cases(text):
    """解析輸入成多筆測資。"""

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return []

    t = int(lines[0])
    p = 1
    cases = []

    for _ in range(t):
        n = int(lines[p])
        p += 1

        pts = []
        for _ in range(n):
            x, y = map(int, lines[p].split())
            p += 1
            pts.append((x, y))

        cases.append(pts)

    return cases


def solve_1d(arr):
    """一維版本：回傳 (最小距離和, 最佳整數點個數)。"""

    arr = sorted(arr)
    n = len(arr)

    # 奇數長度：中位數唯一。
    if n % 2 == 1:
        m = arr[n // 2]
        total = 0
        for v in arr:
            total += abs(v - m)
        return total, 1

    # 偶數長度：在 [L, R] 間所有整數都同樣最優。
    l = arr[n // 2 - 1]
    r = arr[n // 2]

    # 取 l 算距離和即可（l~r 內都會得到同值）。
    total = 0
    for v in arr:
        total += abs(v - l)

    ways = r - l + 1
    return total, ways


def solve_one(points):
    """單筆測資求解。"""

    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    sx, cx = solve_1d(xs)
    sy, cy = solve_1d(ys)

    min_sum = sx + sy
    ways = cx * cy
    return min_sum, ways


def solve(text):
    """對外介面：回傳每筆測資一行 `min_sum ways`。"""

    cases = read_cases(text)
    out = []

    for pts in cases:
        a, b = solve_one(pts)
        out.append(f"{a} {b}")

    return "\n".join(out)


def main():
    import sys

    data = sys.stdin.read()
    ans = solve(data)
    if ans:
        print(ans)


if __name__ == "__main__":
    main()
