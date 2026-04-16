import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10035(unittest.TestCase):
    """測試 QUESTION-10035 解答程式：Primary Arithmetic（進位次數統計）。

    題目重點：
    - 每列輸入兩個正整數 a, b
    - 計算 a + b 時從個位數到最高位的進位次數
    - 遇到輸入 0 0 結束，不應再輸出任何內容
    - 輸出句型：
      - 0 次進位：No carry operation.
      - 1 次進位：1 carry operation.
      - 多次進位：X carry operations.
    """

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期位於同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下要被測試的 10035 解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10035.py",
            "10035-easy.py",
            "10035-manual.py",
            "question_10035.py",
            "solution_10035.py",
            "uva_10035.py",
            "main.py",
        ]

        selected_files = []

        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            lowered_name = path.name.lower()
            if ("10035" in lowered_name or "solution" in lowered_name) and path not in selected_files:
                selected_files.append(path)

        if not selected_files:
            selected_files.append(python_files[0])

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行指定解答程式並回傳標準輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10035 的 Python 解答放在同一資料夾中。")

        completed = subprocess.run(
            [sys.executable, str(solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            cwd=self.base_dir,
            check=False,
        )

        if completed.returncode != 0:
            self.fail(
                f"解答程式 {solution_path.name} 執行失敗。\n"
                f"exit code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )

        return completed.stdout

    @staticmethod
    def expected_message(a, b):
        """用直觀模擬法計算進位次數，並回傳題目要求句型。"""
        carry = 0
        carry_count = 0
        x = a
        y = b

        while x > 0 or y > 0:
            digit_sum = (x % 10) + (y % 10) + carry
            if digit_sum >= 10:
                carry = 1
                carry_count += 1
            else:
                carry = 0

            x //= 10
            y //= 10

        if carry_count == 0:
            return "No carry operation."
        if carry_count == 1:
            return "1 carry operation."
        return f"{carry_count} carry operations."

    def assert_output(self, input_data, expected_output):
        """逐行比對所有解答檔的輸出結果。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10035 的 Python 解答放在同一資料夾中。")

        expected_lines = [line.rstrip() for line in expected_output.strip().splitlines()]

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name):
                actual_output = self.run_solution(solution_path, input_data)
                actual_lines = [line.rstrip() for line in actual_output.strip().splitlines()]
                self.assertEqual(
                    actual_lines,
                    expected_lines,
                    msg=(
                        f"\n解答程式：{solution_path.name}"
                        f"\n輸入：\n{input_data}"
                        f"\n期望輸出：\n{expected_output.strip()}"
                        f"\n實際輸出：\n{actual_output.strip()}"
                    ),
                )

    def test_no_carry(self):
        """基本案例：相加不產生任何進位。"""
        input_data = "123 456\n0 0\n"
        expected_output = "No carry operation."
        self.assert_output(input_data, expected_output)

    def test_multiple_carries(self):
        """基本案例：會產生多次進位（555 + 555 共有 3 次進位）。"""
        input_data = "555 555\n0 0\n"
        expected_output = "3 carry operations."
        self.assert_output(input_data, expected_output)

    def test_sample_style_multiple_lines(self):
        """多筆資料案例：檢查多行輸出與句型轉換。"""
        pairs = [(123, 456), (555, 555), (123, 594)]
        input_data = "\n".join(f"{a} {b}" for a, b in pairs) + "\n0 0\n"
        expected_output = "\n".join(self.expected_message(a, b) for a, b in pairs)
        self.assert_output(input_data, expected_output)

    def test_carry_chain(self):
        """連鎖進位案例：例如 9999 + 1 會一路進位。"""
        input_data = "9999 1\n0 0\n"
        expected_output = "4 carry operations."
        self.assert_output(input_data, expected_output)

    def test_different_length_numbers(self):
        """位數不同案例：長短位數混合時仍要正確計算。"""
        a, b = 1, 999999999
        input_data = f"{a} {b}\n0 0\n"
        expected_output = self.expected_message(a, b)
        self.assert_output(input_data, expected_output)

    def test_terminate_immediately(self):
        """終止案例：第一行就是 0 0，應該沒有任何輸出。"""
        input_data = "0 0\n"

        if not self.solution_paths:
            self.skipTest("找不到解答程式。")

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name):
                actual_output = self.run_solution(solution_path, input_data).strip()
                self.assertEqual(
                    actual_output,
                    "",
                    msg=f"{solution_path.name}：遇到 0 0 應直接結束且不輸出，實際輸出：{repr(actual_output)}",
                )

    def test_mixed_complex_cases(self):
        """混合案例：同時驗證 0 次、1 次、多次進位。"""
        pairs = [(10, 90), (11, 19), (95, 17), (999, 0)]
        input_data = "\n".join(f"{a} {b}" for a, b in pairs) + "\n0 0\n"
        expected_output = "\n".join(self.expected_message(a, b) for a, b in pairs)
        self.assert_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
