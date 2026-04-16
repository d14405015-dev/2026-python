import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10038(unittest.TestCase):
    """測試 QUESTION-10038 解答程式：Jolly Jumpers。

    題目判定規則：
    - 序列長度為 n。
    - 相鄰兩數差的絕對值集合，必須剛好包含 1 到 n-1 的每個整數各一次。
    - 若符合輸出 "Jolly"，否則輸出 "Not jolly"。
    """

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式都預期放在同一個學生資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下要被測試的 10038 解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10038.py",
            "10038-easy.py",
            "10038-manual.py",
            "question_10038.py",
            "solution_10038.py",
            "uva_10038.py",
            "main.py",
        ]

        selected_files = []

        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            lowered_name = path.name.lower()
            if ("10038" in lowered_name or "solution" in lowered_name) and path not in selected_files:
                selected_files.append(path)

        if not selected_files:
            selected_files.append(python_files[0])

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行解答程式並回傳標準輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10038 的 Python 解答放在同一資料夾中。")

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
        """逐行比對所有解答檔輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10038 的 Python 解答放在同一資料夾中。")

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

    def test_sample_like_mixed(self):
        """綜合案例：包含一組 Jolly 與一組 Not jolly。"""
        input_data = (
            "4 1 4 2 3\n"
            "5 1 4 2 -1 6\n"
        )
        expected_output = (
            "Jolly\n"
            "Not jolly"
        )
        self.assert_output(input_data, expected_output)

    def test_single_element_is_jolly(self):
        """n=1 時沒有相鄰差，視為 Jolly。"""
        input_data = "1 100\n"
        expected_output = "Jolly"
        self.assert_output(input_data, expected_output)

    def test_missing_difference(self):
        """缺少必要差值時應為 Not jolly。"""
        input_data = "4 1 2 3 4\n"  # 差值為 1,1,1，缺少 2 與 3
        expected_output = "Not jolly"
        self.assert_output(input_data, expected_output)

    def test_repeated_difference(self):
        """差值重複且無法覆蓋 1..n-1，應為 Not jolly。"""
        input_data = "5 10 7 4 1 -2\n"  # 差值全為 3
        expected_output = "Not jolly"
        self.assert_output(input_data, expected_output)

    def test_negative_values_jolly(self):
        """包含負數時仍可為 Jolly。"""
        input_data = "4 -1 -4 -2 -3\n"
        expected_output = "Jolly"
        self.assert_output(input_data, expected_output)

    def test_large_jump_out_of_range(self):
        """若出現超過 n-1 的差值，應為 Not jolly。"""
        input_data = "4 1 10 2 3\n"  # 首差為 9，超過 n-1=3
        expected_output = "Not jolly"
        self.assert_output(input_data, expected_output)

    def test_multiple_lines_until_eof(self):
        """多筆輸入直到 EOF，確認每行都正確判定。"""
        input_data = (
            "4 1 4 2 3\n"
            "4 1 2 3 4\n"
            "1 7\n"
            "5 5 1 4 2 3\n"
        )
        expected_output = (
            "Jolly\n"
            "Not jolly\n"
            "Jolly\n"
            "Jolly"
        )
        self.assert_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
