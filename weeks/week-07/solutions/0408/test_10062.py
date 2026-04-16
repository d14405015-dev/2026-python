import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10062(unittest.TestCase):
    """測試 QUESTION-10062 解答程式是否能正確還原乳牛的排列順序。"""

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式都預期放在同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下要被測試的解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10062.py",
            "10062-easy.py",
            "question_10062.py",
            "solution_10062.py",
            "uva_10062.py",
            "main.py",
        ]

        selected_files = []

        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            lowered_name = path.name.lower()
            if ("10062" in lowered_name or "solution" in lowered_name) and path not in selected_files:
                selected_files.append(path)

        if not selected_files:
            selected_files.append(python_files[0])

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行學生解答程式，並回傳標準輸出內容。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10062 的 Python 解答放在同一個資料夾中。")

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
        """以逐行比較方式驗證所有解答檔的輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到解答程式。請先把 QUESTION-10062 的 Python 解答放在同一個資料夾中。")

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name):
                actual_output = self.run_solution(solution_path, input_data)
                self.assertEqual(actual_output.splitlines(), expected_output.splitlines())

    def test_single_cow(self):
        # 只有一頭乳牛時，不需要任何額外資訊，答案固定是 1。
        input_data = "1\n"
        expected_output = "1\n"
        self.assert_output(input_data, expected_output)

    def test_two_cows_reverse_order(self):
        # 第二個位置前面沒有比牠小的牛，代表排列為 2, 1。
        input_data = "2\n0\n"
        expected_output = "2\n1\n"
        self.assert_output(input_data, expected_output)

    def test_already_sorted(self):
        # 若每個位置前面比自己小的牛數量依序為 1, 2, 3，表示整體已經遞增排序。
        input_data = "4\n1\n2\n3\n"
        expected_output = "1\n2\n3\n4\n"
        self.assert_output(input_data, expected_output)

    def test_completely_descending(self):
        # 全部都是 0 代表每頭牛前面都沒有更小的編號，因此是完全遞減的排列。
        input_data = "4\n0\n0\n0\n"
        expected_output = "4\n3\n2\n1\n"
        self.assert_output(input_data, expected_output)

    def test_mixed_order_case(self):
        # 這組資料對應到排列 4, 2, 5, 1, 3，可檢查一般情況的還原是否正確。
        input_data = "5\n0\n2\n0\n2\n"
        expected_output = "4\n2\n5\n1\n3\n"
        self.assert_output(input_data, expected_output)

    def test_another_mixed_order_case(self):
        # 這組資料對應到排列 2, 3, 1，可避免只通過單一模式的硬寫答案。
        input_data = "3\n1\n0\n"
        expected_output = "2\n3\n1\n"
        self.assert_output(input_data, expected_output)


if __name__ == "__main__":
    unittest.main()