import importlib.util
import io
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from itertools import permutations


class CandidateRunner:
    """負責載入並執行使用者解答程式。"""

    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.solution_path = self._find_solution_path()
        self.module = self._load_module(self.solution_path) if self.solution_path else None

    def _find_solution_path(self):
        preferred_names = [
            "question_10226.py",
            "solution_10226.py",
            "uva_10226.py",
            "main.py",
        ]

        for name in preferred_names:
            path = os.path.join(self.base_dir, name)
            if os.path.isfile(path):
                return path

        # 若找不到預設檔名，則退而求其次挑第一個非測試檔 Python 檔。
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
        module_name = "candidate_solution_10226"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run(self, input_data):
        if self.solution_path is None:
            raise AssertionError(
                "找不到解答程式。請在同資料夾放入 question_10226.py（或其他 Python 解答檔）。"
            )

        # 優先嘗試呼叫 solve(input_str) 介面，便於做單元測試。
        if self.module is not None and hasattr(self.module, "solve"):
            solve_fn = getattr(self.module, "solve")
            with io.StringIO() as buffer, redirect_stdout(buffer):
                returned = solve_fn(input_data)
                printed = buffer.getvalue()

            if isinstance(returned, str):
                return returned
            return printed

        # 若無 solve，則以子行程執行整支腳本，模擬線上判題環境。
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


def format_single_case_input(forbidden_positions):
    """把單一測資轉成題目輸入格式。"""

    n = len(forbidden_positions)
    lines = [str(n)]
    for positions in forbidden_positions:
        if positions:
            lines.append(" ".join(map(str, positions + [0])))
        else:
            lines.append("0")
    return "\n".join(lines) + "\n"


def build_expected_output(forbidden_positions):
    """依題意產生正確輸出：字典序列舉 + 只輸出和前一個排列不同的尾段。"""

    n = len(forbidden_positions)
    people = [chr(ord("A") + i) for i in range(n)]

    valid = []
    for perm in permutations(people):
        ok = True
        for idx, person in enumerate(perm):
            person_index = ord(person) - ord("A")
            position_1_based = idx + 1
            if position_1_based in forbidden_positions[person_index]:
                ok = False
                break
        if ok:
            valid.append(perm)

    if not valid:
        return ""

    lines = ["".join(valid[0])]
    for prev, curr in zip(valid, valid[1:]):
        pivot = 0
        while pivot < n and prev[pivot] == curr[pivot]:
            pivot += 1
        lines.append("".join(curr[pivot:]))

    return "\n".join(lines)


def normalize_output(text):
    """避免行尾空白或最後多一行造成誤判。"""

    stripped = text.strip()
    if not stripped:
        return ""
    return "\n".join(line.rstrip() for line in stripped.splitlines())


class TestQuestion10226(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = CandidateRunner()

    def assert_case(self, forbidden_positions):
        input_data = format_single_case_input(forbidden_positions)
        expected = build_expected_output(forbidden_positions)
        actual = self.runner.run(input_data)
        self.assertEqual(normalize_output(actual), normalize_output(expected))

    def test_n1_no_constraint(self):
        # 1 人無限制，只有一種排列。
        self.assert_case([[]])

    def test_n3_partial_constraints(self):
        # A 不要在 1，B 不要在 2，C 不限制。
        self.assert_case([[1], [2], []])

    def test_n4_multiple_constraints(self):
        # 混合多個限制，驗證字典序與差異輸出邏輯。
        self.assert_case([[2], [1, 3], [4], []])

    def test_n3_no_valid_permutation(self):
        # A 不能在 1/2/3，必定無解，預期空輸出。
        self.assert_case([[1, 2, 3], [], []])


if __name__ == "__main__":
    unittest.main()
