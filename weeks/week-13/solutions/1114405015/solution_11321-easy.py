"""UVA 11321 - 逐次放陷阱且不可封死道路（easy 版本）

題目重點：
1. 地圖是 N x M 格子。
2. 每次給一個要放陷阱的位置 (x, y)。
3. 若放下去後「仍存在左邊界到右邊界的路徑」，就輸出 <(_ _)> 並保留陷阱。
4. 若放下去會讓道路封死，就輸出 >_< 並取消這次放置。

容易記憶的作法：
- 每次嘗試放一顆陷阱後，直接做一次 BFS 檢查「左到右是否可達」。
- 可達就接受，不可達就回復。

雖然不是最進階的演算法，但邏輯直觀，對中小型測試非常穩定，
也非常適合教學與單元測試驗證。
"""

from __future__ import annotations

from collections import deque
from typing import List, Set, Tuple
import sys


Point = Tuple[int, int]


def has_path_left_to_right(n: int, m: int, blocked: Set[Point]) -> bool:
    """檢查目前障礙配置是否存在左邊界到右邊界路徑。"""
    q: deque[Point] = deque()
    visited: Set[Point] = set()

    # 左邊界所有未被封鎖的格子都可以當作起點。
    for x in range(n):
        p = (x, 0)
        if p not in blocked:
            q.append(p)
            visited.add(p)

    # 左邊界若全部被封鎖，必定無路可走。
    if not q:
        return False

    while q:
        x, y = q.popleft()

        # 一旦到達右邊界（y == m-1），表示路徑存在。
        if y == m - 1:
            return True

        # 只能上下左右移動，不可走斜角。
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            np = (nx, ny)
            if 0 <= nx < n and 0 <= ny < m and np not in blocked and np not in visited:
                visited.add(np)
                q.append(np)

    return False


def solve(input_text: str) -> str:
    """讀取單筆輸入，回傳逐次判定結果。"""
    nums = list(map(int, input_text.split()))
    if not nums:
        return ""

    idx = 0
    n = nums[idx]
    m = nums[idx + 1]
    t = nums[idx + 2]
    idx += 3

    blocked: Set[Point] = set()
    out_lines: List[str] = []

    for _ in range(t):
        x = nums[idx]
        y = nums[idx + 1]
        idx += 2

        p = (x, y)

        # 題目保證同一格最多被放一次，這裡仍以防禦性寫法保護狀態。
        if p in blocked:
            out_lines.append("<(_ _)>")
            continue

        # 先嘗試放置，再檢查是否封死。
        blocked.add(p)

        if has_path_left_to_right(n, m, blocked):
            out_lines.append("<(_ _)>")
        else:
            blocked.remove(p)
            out_lines.append(">_<")

    return "\n".join(out_lines)


def main() -> None:
    """線上評測入口：由 stdin 讀入、輸出到 stdout。"""
    data = sys.stdin.read()
    result = solve(data)
    if result:
        sys.stdout.write(result)


if __name__ == "__main__":
    main()
