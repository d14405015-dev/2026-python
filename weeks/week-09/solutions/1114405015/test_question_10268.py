import importlib.util
import io
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout


MORE_TEXT = "More than 63 trials needed."


class CandidateRunner:
    """負責載入與執行受測解答程式。"""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.solution_path = self._find_solution_path()
        self.module = self._load_module(self.solution_path) if self.solution_path else None

    def _find_solution_path(self):
        preferred_names = [
            "question_10268.py",
            "solution_10268.py",
            "uva_10268.py",
            "main.py",
        ]

        for name in preferred_names:
            path = os.path.join(self.base_dir, name)
            if os.path.isfile(path):
                return path

        # 找不到預設檔名時，退而求其次找第一個非測試 Python 檔。
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
        spec = importlib.util.spec_from_file_location("candidate_solution_10268", file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run(self, input_data: str) -> str:
        if self.solution_path is None:
            raise AssertionError(
                "找不到解答程式，請在同資料夾放入 question_10268.py（或其他 Python 解答檔）。"
            )

        # 優先使用 solve(input_str)；若沒有則以子行程執行腳本。
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
    """把多筆 (k, n) 組成題目輸入，末尾自動補 k=0。"""

    lines = [f"{k} {n}" for k, n in cases]
    lines.append("0 0")
    return "\n".join(lines) + "\n"


def min_trials_or_more(k, n):
    """參考解：回傳最少次數，若超過 63 則回傳指定字串。"""

    if n <= 0:
        return "0"

    # dp[e] = 在目前 trial 次數下，e 顆球可測的最大樓層數
    dp = [0] * (k + 1)

    for t in range(1, 64):
        # 由大到小更新，避免覆蓋到上一輪 (t-1) 的值。
        for e in range(k, 0, -1):
            dp[e] = dp[e] + dp[e - 1] + 1

        if dp[k] >= n:
            return str(t)

    return MORE_TEXT


def reference_outputs(cases):
    return [min_trials_or_more(k, n) for k, n in cases]


def normalize_output_lines(text):
    """標準化輸出行，移除前後空白與空行。"""

    return [line.strip() for line in text.strip().splitlines() if line.strip()]


class TestQuestion10268(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CandidateRunner()

    def assert_cases(self, cases):
        input_data = build_input(cases)
        expected = reference_outputs(cases)
        actual_text = self.runner.run(input_data)
        actual = normalize_output_lines(actual_text)

        self.assertEqual(
            actual,
            expected,
            msg=(
                "答案或輸出格式不正確。\n"
                f"輸入:\n{input_data}\n"
                f"預期:\n{expected}\n"
                f"實際:\n{actual_text}"
            ),
        )

    def test_single_ball_small_building(self):
        # 一顆球時只能線性測試，n=10 需要 10 次。
        self.assert_cases([(1, 10)])

    def test_two_balls_typical_case(self):
        # 兩顆球，測常見樓層數，驗證最少次數計算。
        self.assert_cases([(2, 100)])

    def test_multiple_cases_in_one_input(self):
        # 多筆輸入一起測，驗證逐行輸出與終止條件處理。
        self.assert_cases(
            [
                (3, 14),
                (2, 36),
                (4, 500),
            ]
        )

    def test_zero_floor(self):
        # 0 層樓不需測試，答案應為 0。
        self.assert_cases([(5, 0)])

    def test_more_than_63_trials(self):
        # k=1 且 n 很大，會超過 63 次，需輸出固定字串。
        self.assert_cases([(1, 10**18)])


if __name__ == "__main__":
    unittest.main()
