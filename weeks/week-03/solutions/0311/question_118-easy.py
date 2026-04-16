"""
UVA 118 - easy 版本

這份程式刻意維持「容易手打、容易記」：
- 結構直線
- 變數命名簡單
- 邏輯集中在一個主迴圈

規則記憶：
1. L / R 只改方向，不移動
2. F 要先看下一步是否出界
3. 出界時若有 scent -> 忽略這次 F
4. 出界時若無 scent -> 留 scent 並 LOST
"""

from __future__ import annotations

import sys


def main() -> None:
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    if not lines:
        return

    max_x, max_y = map(int, lines[0].split())

    # 方向用順時針陣列，方便做左轉/右轉。
    dirs = ["N", "E", "S", "W"]

    # 每個方向對應位移。
    step = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0),
    }

    # scent 紀錄格式：(x, y, direction)
    scents: set[tuple[int, int, str]] = set()

    out: list[str] = []
    i = 1

    while i + 1 < len(lines):
        x_s, y_s, d = lines[i].split()
        cmds = lines[i + 1]

        x = int(x_s)
        y = int(y_s)
        lost = False

        for c in cmds:
            if c == "L":
                d = dirs[(dirs.index(d) - 1) % 4]
                continue

            if c == "R":
                d = dirs[(dirs.index(d) + 1) % 4]
                continue

            # c == 'F'
            dx, dy = step[d]
            nx = x + dx
            ny = y + dy

            # 準備走出地圖：要看 scent 規則。
            if nx < 0 or nx > max_x or ny < 0 or ny > max_y:
                if (x, y, d) in scents:
                    # 同一個危險點已有人掉過，這次前進指令忽略。
                    continue

                # 第一次從此點此方向掉落：留下 scent，機器人結束。
                scents.add((x, y, d))
                lost = True
                break

            # 還在地圖內就正常前進。
            x, y = nx, ny

        if lost:
            out.append(f"{x} {y} {d} LOST")
        else:
            out.append(f"{x} {y} {d}")

        i += 2

    if out:
        print("\n".join(out))


if __name__ == "__main__":
    main()
