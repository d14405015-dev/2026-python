import importlib.util
import io
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout


class CandidateRunner:
    """負責載入與執行受測解答。"""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.solution_path = self._find_solution_path()
        self.module = self._load_module(self.solution_path) if self.solution_path else None

    def _find_solution_path(self):
        preferred_names = [
            "question_10252.py",
            "solution_10252.py",
            "uva_10252.py",
            "main.py",
        ]

        for name in preferred_names:
            path = os.path.join(self.base_dir, name)
            if os.path.isfile(path):
                return path

        # 找不到預設檔名時，選同資料夾第一個非測試 Python 檔。
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
        spec = importlib.util.spec_from_file_location("candidate_solution_10252", file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run(self, input_data: str) -> str:
        if self.solution_path is None:
            raise AssertionError(
                "找不到解答程式，請在同資料夾放入 question_10252.py（或其他 Python 解答檔）。"
            )

        # 優先使用 solve(input_str)，否則改用子行程執行腳本。
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
    """把多筆測資組成題目輸入格式。"""

    lines = [str(len(cases))]
    for points in cases:
        lines.append(str(len(points)))
        for x, y in points:
            lines.append(f"{x} {y}")
    return "\n".join(lines) + "\n"


def one_dim_opt(values):
    """回傳一維最小距離和與最佳整數解個數。"""

    arr = sorted(values)
    n = len(arr)

    # 奇數：中位數唯一；偶數：中間區間內任一整數皆最優。
    if n % 2 == 1:
        med = arr[n // 2]
        best_sum = sum(abs(v - med) for v in arr)
        count = 1
        return best_sum, count

    left = arr[n // 2 - 1]
    right = arr[n // 2]
    best_sum = sum(abs(v - left) for v in arr)
    count = right - left + 1
    return best_sum, count


def reference_answer(points):
    """參考解：最小化曼哈頓距離總和與整數最優點數量。"""

    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    sx, cx = one_dim_opt(xs)
    sy, cy = one_dim_opt(ys)

    return sx + sy, cx * cy


def parse_output_lines(output, expected_cases):
    """解析輸出，每行應為兩個整數：min_sum count。"""

    lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
    if len(lines) != expected_cases:
        raise AssertionError(
            f"輸出行數錯誤，預期 {expected_cases} 行，實際 {len(lines)} 行。\n輸出內容:\n{output}"
        )

    parsed = []
    for line in lines:
        parts = line.split()
        if len(parts) != 2:
            raise AssertionError(f"每行應為兩個整數，實際：{line}")
        try:
            a = int(parts[0])
            b = int(parts[1])
        except ValueError as exc:
            raise AssertionError(f"輸出非整數：{line}") from exc
        parsed.append((a, b))

    return parsed


class TestQuestion10252(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CandidateRunner()

    def assert_cases(self, cases):
        input_data = build_input(cases)
        expected = [reference_answer(points) for points in cases]
        actual_output = self.runner.run(input_data)
        actual = parse_output_lines(actual_output, len(cases))

        self.assertEqual(
            actual,
            expected,
            msg=(
                "答案不正確。\n"
                f"輸入:\n{input_data}\n"
                f"預期: {expected}\n"
                f"實際輸出:\n{actual_output}"
            ),
        )

    def test_single_point(self):
        # 單一點，最小距離和為 0，最佳整數點僅 1 個。
        self.assert_cases([
            [(3, -5)],
        ])

    def test_three_collinear_points(self):
        # 三點共線（對角線），中位數唯一。
        self.assert_cases([
            [(0, 0), (1, 1), (2, 2)],
        ])

    def test_even_points_interval_count(self):
        # 偶數個點時，x 與 y 可能形成最優區間，需計算方案數乘積。
        self.assert_cases([
            [(0, 0), (2, 2)],
        ])

    def test_mixed_negative_and_duplicates(self):
        # 含負座標、重複座標，驗證通用性。
        self.assert_cases([
            [(-1, 0), (3, 2), (5, -2), (0, 4), (0, 4)],
        ])

    def test_multiple_cases_in_one_input(self):
        # 多筆測資一次驗證輸入輸出處理。
        self.assert_cases(
            [
                [(0, 0), (2, 2)],
                [(1, 1), (1, 1), (1, 1)],
                [(-2, 3), (4, -1), (0, 0), (2, 2)],
            ]
        )


if __name__ == "__main__":
    unittest.main()
