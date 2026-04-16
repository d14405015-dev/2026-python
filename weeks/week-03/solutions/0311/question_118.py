"""
UVA 118 - Mutant Flatworld Explorers

這是標準版解法：
- 以清楚可讀為主
- 正確處理「掉落 LOST」與「氣味 scent」規則
- 保留原始輸出格式：x y direction [LOST]
"""

from __future__ import annotations

import sys


# 方向順序（順時針）：北、東、南、西
DIRECTIONS = "NESW"

# 每個方向對應的位移（dx, dy）
MOVE = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


def turn_left(direction: str) -> str:
    """回傳左轉 90 度後的新方向。"""
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx - 1) % 4]


def turn_right(direction: str) -> str:
    """回傳右轉 90 度後的新方向。"""
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx + 1) % 4]


def process_robot(
    x: int,
    y: int,
    direction: str,
    commands: str,
    max_x: int,
    max_y: int,
    scents: set[tuple[int, int, str]],
) -> tuple[int, int, str, bool]:
    """執行單一機器人的所有指令。

    參數說明：
    - x, y, direction：機器人初始位置與朝向
    - commands：指令字串（L, R, F）
    - max_x, max_y：地圖右上角邊界（左下角固定為 0,0）
    - scents：已知氣味集合，元素為 (x, y, direction)

    回傳：
    - 最終 x, y, direction
    - 是否 LOST（True/False）
    """
    for cmd in commands:
        if cmd == "L":
            direction = turn_left(direction)
            continue

        if cmd == "R":
            direction = turn_right(direction)
            continue

        # cmd == 'F'：嘗試往目前方向前進一格
        dx, dy = MOVE[direction]
        next_x = x + dx
        next_y = y + dy

        # 如果下一步會離開地圖，需判斷是否有 scent
        out_of_bounds = not (0 <= next_x <= max_x and 0 <= next_y <= max_y)
        if out_of_bounds:
            # 規則重點：同一「位置 + 朝向」若已有 scent，該 F 要被忽略
            if (x, y, direction) in scents:
                continue

            # 首次在此位置與朝向掉落：留下 scent，並標記 LOST
            scents.add((x, y, direction))
            return x, y, direction, True

        # 沒掉落就正常前進
        x, y = next_x, next_y

    # 指令做完仍在地圖內
    return x, y, direction, False


def solve(data: str) -> str:
    """解析整份輸入並輸出所有機器人最終狀態。"""
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return ""

    # 第一行是地圖右上角座標
    max_x, max_y = map(int, lines[0].split())

    scents: set[tuple[int, int, str]] = set()
    output_lines: list[str] = []

    # 之後每兩行是一組機器人：
    # 第 1 行：x y direction
    # 第 2 行：commands
    idx = 1
    while idx + 1 < len(lines):
        x_str, y_str, direction = lines[idx].split()
        commands = lines[idx + 1]

        x = int(x_str)
        y = int(y_str)

        final_x, final_y, final_direction, lost = process_robot(
            x=x,
            y=y,
            direction=direction,
            commands=commands,
            max_x=max_x,
            max_y=max_y,
            scents=scents,
        )

        if lost:
            output_lines.append(f"{final_x} {final_y} {final_direction} LOST")
        else:
            output_lines.append(f"{final_x} {final_y} {final_direction}")

        idx += 2

    return "\n".join(output_lines)


def main() -> None:
    """程式進入點：讀 stdin，計算後輸出。"""
    data = sys.stdin.read()
    result = solve(data)
    if result:
        print(result)


if __name__ == "__main__":
    main()
