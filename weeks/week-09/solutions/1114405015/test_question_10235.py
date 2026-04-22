import importlib.util
import io
import os
import re
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

MOD = 1_000_000_007


class CandidateRunner:
    """負責載入並執行受測解答程式。"""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.solution_path = self._find_solution_path()
        self.module = self._load_module(self.solution_path) if self.solution_path else None

    def _find_solution_path(self):
        preferred_names = [
            "question_10235.py",
            "solution_10235.py",
            "uva_10235.py",
            "main.py",
        ]

        for name in preferred_names:
            path = os.path.join(self.base_dir, name)
            if os.path.isfile(path):
                return path

        # 若找不到固定檔名，退而求其次找同資料夾內第一個非測試檔 Python。
        for name in sorted(os.listdir(self.base_dir)):
            if not name.endswith(".py"):
                continue
            if name.startswith("test_"):
                continue
            if name == os.path.basename(__file__):
                continue
            return os.path.join(self.base_dir, name)

        return None

    def _load_module(self, file_path):
        spec = importlib.util.spec_from_file_location("candidate_solution_10235", file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run(self, input_data: str) -> str:
        if self.solution_path is None:
            raise AssertionError(
                "找不到解答程式，請在同資料夾放入 question_10235.py（或其他 Python 解答檔）。"
            )

        # 優先使用 solve(input_str) 介面，沒有再改用子行程執行腳本。
        if self.module is not None and hasattr(self.module, "solve"):
            solve_fn = getattr(self.module, "solve")
            with io.StringIO() as buf, redirect_stdout(buf):
                returned = solve_fn(input_data)
                printed = buf.getvalue()

            if isinstance(returned, str):
                return returned
            return printed

        completed = subprocess.run(
            [sys.executable, self.solution_path],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            raise AssertionError(
                f"解答程式執行失敗（exit code={completed.returncode}）：\n{completed.stderr}"
            )
        return completed.stdout


def build_input(cases):
    """將多筆測資轉成題目輸入字串。"""

    lines = [str(len(cases))]
    for grid in cases:
        n = len(grid)
        m = len(grid[0]) if n else 0
        lines.append(f"{n} {m}")
        lines.extend(grid)
    return "\n".join(lines) + "\n"


def parse_case_lines(output: str):
    """解析 `Case i: ans` 格式，回傳答案整數列表。"""

    lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
    results = []
    pattern = re.compile(r"^Case\s+\d+\s*:\s*(-?\d+)\s*$")

    for line in lines:
        match = pattern.match(line)
        if not match:
            raise AssertionError(f"輸出格式錯誤，預期 `Case i: ans`，實際：{line}")
        results.append(int(match.group(1)))

    return results


def count_cycle_covers_bruteforce(grid):
    """用暴力法計算答案（僅適合小測資）。

    規則模型：
    - `1` 格子必須被蛇覆蓋，且在鄰接圖中的度數必須剛好為 2。
    - `0` 格子不能被使用。
    - 鄰接採上下左右（四連通）。

    若所有使用節點度數都為 2，則每個連通分量都是一個環，
    等價於題目「每條蛇都咬自己尾巴」的條件。
    """

    n = len(grid)
    m = len(grid[0])

    vertices = []
    id_of = {}
    for r in range(n):
        for c in range(m):
            if grid[r][c] == "1":
                id_of[(r, c)] = len(vertices)
                vertices.append((r, c))

    v_count = len(vertices)
    if v_count == 0:
        # 沒有可放蛇的格子，視為一種合法方式（擺 0 條蛇）。
        return 1

    edges = []
    for i, (r, c) in enumerate(vertices):
        for dr, dc in ((1, 0), (0, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in id_of:
                j = id_of[(nr, nc)]
                edges.append((i, j))

    deg = [0] * v_count

    def dfs_edge(idx):
        if idx == len(edges):
            return 1 if all(d == 2 for d in deg) else 0

        u, v = edges[idx]

        # 不選這條邊
        total = dfs_edge(idx + 1)

        # 選這條邊，但不能讓任何點度數超過 2
        if deg[u] < 2 and deg[v] < 2:
            deg[u] += 1
            deg[v] += 1
            total += dfs_edge(idx + 1)
            deg[u] -= 1
            deg[v] -= 1

        return total

    return dfs_edge(0) % MOD


def build_expected_output(cases):
    """產生每筆 `Case i: ans` 的期望輸出。"""

    lines = []
    for idx, grid in enumerate(cases, start=1):
        ans = count_cycle_covers_bruteforce(grid)
        lines.append(f"Case {idx}: {ans}")
    return "\n".join(lines)


class TestQuestion10235(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CandidateRunner()

    def assert_cases(self, cases):
        input_data = build_input(cases)
        expected = build_expected_output(cases)
        actual = self.runner.run(input_data)

        expected_vals = parse_case_lines(expected)
        actual_vals = parse_case_lines(actual)

        self.assertEqual(
            actual_vals,
            expected_vals,
            msg=(
                "答案或輸出順序不符。\n"
                f"輸入:\n{input_data}\n"
                f"預期:\n{expected}\n"
                f"實際:\n{actual}"
            ),
        )

    def test_single_empty_cell(self):
        # 只有一個可用格（1x1），不可能形成環，答案應為 0。
        self.assert_cases([
            ["1"],
        ])

    def test_all_socket_grid(self):
        # 全部是插座（0），可以一條蛇都不擺，答案應為 1。
        self.assert_cases([
            ["00", "00"],
        ])

    def test_simple_square_cycle(self):
        # 2x2 全 1，恰好一個 4-cycle，答案為 1。
        self.assert_cases([
            ["11", "11"],
        ])

    def test_multiple_cases_mixed(self):
        # 一次測多筆，驗證 Case 編號與多筆輸出格式。
        self.assert_cases(
            [
                ["111", "111"],   # 2x3 長方形，存在環覆蓋
                ["101", "111"],   # 含障礙，檢查限制處理
                ["10", "01"],     # 兩個孤立可用格，不可能成環
            ]
        )


if __name__ == "__main__":
    unittest.main()
