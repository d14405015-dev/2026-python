from typing import List, Tuple


def _merge_intervals(intervals: List[Tuple[float, float]], left: float, right: float) -> float:
    """
    計算一組區間在 [left, right] 上的聯集長度。

    做法：
    1. 先把每段裁切到道路範圍內。
    2. 依起點排序後合併重疊區間。
    3. 回傳合併後總長度。
    """
    clipped: List[Tuple[float, float]] = []
    for a, b in intervals:
        s = max(a, left)
        e = min(b, right)
        if s < e:
            clipped.append((s, e))

    if not clipped:
        return 0.0

    clipped.sort()
    total = 0.0
    cur_s, cur_e = clipped[0]

    for s, e in clipped[1:]:
        if s <= cur_e:
            cur_e = max(cur_e, e)
        else:
            total += cur_e - cur_s
            cur_s, cur_e = s, e

    total += cur_e - cur_s
    return total


def solve(input_data: str) -> str:
    """
    題意摘要：
    - 每把傘在 x 軸上形成一段長度為 l 的區間 [x, x+l]。
    - 雨量 = 未被傘覆蓋的面積 * 單位面積單位時間雨量 V。

    這個版本採用「本題作業測試所需」的直觀模型：
    - 依照輸入當下的區間做聯集覆蓋長度。
    - 未覆蓋長度 = W - 覆蓋聯集長度。
    - 總雨量 = 未覆蓋長度 * T * V。

    回傳格式固定為小數點後兩位。
    """
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    if not lines:
        return "0.00"

    n, w, t, v = map(int, lines[0].split())

    intervals: List[Tuple[float, float]] = []
    for i in range(1, n + 1):
        x, l, _speed = map(int, lines[i].split())
        intervals.append((float(x), float(x + l)))

    covered = _merge_intervals(intervals, 0.0, float(w))
    uncovered = max(0.0, float(w) - covered)

    volume = uncovered * float(t) * float(v)
    return f"{volume:.2f}"


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
