from typing import List, Tuple


# -easy 版本：
# 核心口訣只有三步：
# 1) 把每把傘變成區間 [x, x+l]
# 2) 做區間合併，求覆蓋總長度
# 3) 用 (W - 覆蓋) * T * V 算雨量


def solve(input_data: str) -> str:
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    if not lines:
        return "0.00"

    n, w, t, v = map(int, lines[0].split())

    segs: List[Tuple[int, int]] = []
    for i in range(1, n + 1):
        x, l, _ = map(int, lines[i].split())
        left = max(0, x)
        right = min(w, x + l)
        if left < right:
            segs.append((left, right))

    # 沒有任何有效覆蓋區間
    if not segs:
        return f"{w * t * v:.2f}"

    # 先依左端點排序，準備做合併
    segs.sort()

    covered = 0
    cur_l, cur_r = segs[0]

    for l, r in segs[1:]:
        if l <= cur_r:
            # 重疊或相接，延長目前區段
            cur_r = max(cur_r, r)
        else:
            # 不重疊，先結算前一段，再開新段
            covered += cur_r - cur_l
            cur_l, cur_r = l, r

    covered += cur_r - cur_l

    uncovered = max(0, w - covered)
    ans = uncovered * t * v
    return f"{ans:.2f}"


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
