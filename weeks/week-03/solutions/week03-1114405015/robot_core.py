"""Robot Lost (UVA 118) 核心邏輯。

此模組不依賴 pygame，方便單元測試與重用。
"""

from dataclasses import dataclass
from typing import Iterable

DIRECTIONS = ("N", "E", "S", "W")
MOVE_VECTOR = {
    "N": (0, 1),
    "E": (1, 0),
    "S": (0, -1),
    "W": (-1, 0),
}


@dataclass
class RobotState:
    x: int
    y: int
    direction: str
    lost: bool = False


def turn_left(direction: str) -> str:
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx - 1) % 4]


def turn_right(direction: str) -> str:
    idx = DIRECTIONS.index(direction)
    return DIRECTIONS[(idx + 1) % 4]


def next_position(x: int, y: int, direction: str) -> tuple[int, int]:
    dx, dy = MOVE_VECTOR[direction]
    return x + dx, y + dy


def in_bounds(x: int, y: int, width: int, height: int) -> bool:
    return 0 <= x <= width and 0 <= y <= height


def apply_instruction(
    state: RobotState,
    instruction: str,
    width: int,
    height: int,
    scents: set[tuple[int, int, str]],
) -> None:
    if state.lost:
        return

    if instruction == "L":
        state.direction = turn_left(state.direction)
        return

    if instruction == "R":
        state.direction = turn_right(state.direction)
        return

    if instruction != "F":
        raise ValueError(f"Unsupported instruction: {instruction}")

    nx, ny = next_position(state.x, state.y, state.direction)

    if in_bounds(nx, ny, width, height):
        state.x, state.y = nx, ny
        return

    scent_key = (state.x, state.y, state.direction)
    if scent_key in scents:
        # 同一位置同一方向曾掉落，忽略這次危險前進。
        return

    scents.add(scent_key)
    state.lost = True


def run_instructions(
    start_x: int,
    start_y: int,
    start_direction: str,
    instructions: Iterable[str],
    width: int,
    height: int,
    scents: set[tuple[int, int, str]],
) -> RobotState:
    if start_direction not in DIRECTIONS:
        raise ValueError(f"Unsupported direction: {start_direction}")

    state = RobotState(start_x, start_y, start_direction)

    if not in_bounds(state.x, state.y, width, height):
        raise ValueError("Robot start position is out of bounds")

    for cmd in instructions:
        apply_instruction(state, cmd, width, height, scents)
        if state.lost:
            break

    return state


def state_text(state: RobotState) -> str:
    suffix = " LOST" if state.lost else ""
    return f"{state.x} {state.y} {state.direction}{suffix}"


def matrix_snapshot(width: int, height: int, state: RobotState) -> list[list[str]]:
    """回傳 10x10 內可視化用矩陣快照（加分項輔助）。"""
    grid = [["." for _ in range(width + 1)] for _ in range(height + 1)]
    if in_bounds(state.x, state.y, width, height):
        grid[height - state.y][state.x] = state.direction
    return grid
