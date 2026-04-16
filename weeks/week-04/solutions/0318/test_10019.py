import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10019(unittest.TestCase):
    """測試 QUESTION-10019 解答程式是否符合題目檔的 I/O 規格。

    依目前題目敘述內容（Hashmat 差值題型）：
    - 每列輸入 2 個整數
    - 逐列輸出兩數的差的絕對值
    - 持續讀到 EOF
    """

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期放在同一個資料夾。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下要被測試的 10019 解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10019.py",
            "10019-easy.py",
            "10019-manual.py",
            "question_10019.py",
            "solution_10019.py",
            "uva_10019.py",
            "main.py",
        ]

        selected_files = []

        # 先依常見檔名挑選，維持固定測試順序。
        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        # 補上其他名稱含 10019 或 solution 的檔案。
        for path in python_files:
            lowered_name = path.name.lower()
            if ("10019" in lowered_name or "solution" in lowered_name) and path not in selected_files:
                selected_files.append(path)

        # 若仍找不到，至少挑一個非測試 .py，避免整個測試檔無法運作。
        if not selected_files:
            selected_files.append(python_files[0])

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行解答程式並回傳其標準輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10019 的 Python 解答放在同一資料夾中。")

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

    def assert_output(self, input_data, expected_output):
        """逐行比對所有解答檔的輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10019 的 Python 解答放在同一資料夾中。")

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

    def test_single_case(self):
        """單筆資料：基本差值計算。"""
        input_data = "10 12\n"
        expected_output = "2"
        self.assert_output(input_data, expected_output)

    def test_same_numbers(self):
        """兩數相同時，差值應為 0。"""
        input_data = "777 777\n"
        expected_output = "0"
        self.assert_output(input_data, expected_output)

    def test_reversed_order(self):
        """題目可能出現任意順序，應取絕對值。"""
        input_data = "1000 1\n"
        expected_output = "999"
        self.assert_output(input_data, expected_output)

    def test_multiple_lines_until_eof(self):
        """多筆資料，程式需逐列輸出並讀到 EOF。"""
        input_data = (
            "10 12\n"
            "10 10\n"
            "1 1000\n"
            "500 499\n"
        )
        expected_output = (
            "2\n"
            "0\n"
            "999\n"
            "1"
        )
        self.assert_output(input_data, expected_output)

    def test_large_numbers(self):
        """大數測試：接近 64-bit 範圍。"""
        input_data = "0 9223372036854775807\n"
        expected_output = "9223372036854775807"
        self.assert_output(input_data, expected_output)

    def test_input_with_extra_spaces(self):
        """含多餘空白時仍應正確解析（split 可處理連續空白）。"""
        input_data = (
            "   3      8\n"
            "9            4\n"
        )
        expected_output = (
            "5\n"
            "5"
        )
        self.assert_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
