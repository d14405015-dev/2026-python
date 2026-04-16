import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path


class TestQuestion10071(unittest.TestCase):
    """測試 QUESTION-10071 解答程式是否能正確計算符合條件的六元組數量。"""

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期都放在同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下與 10071 題目對應的解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10071.py",
            "10071-easy.py",
            "10071-manual.py",
            "question_10071.py",
            "solution_10071.py",
            "uva_10071.py",
            "main.py",
        ]

        selected_files = []

        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            lowered_name = path.name.lower()
            if ("10071" in lowered_name or "solution" in lowered_name) and path not in selected_files:
                selected_files.append(path)

        if not selected_files:
            return []

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行學生解答程式，並回傳標準輸出內容。"""
        if not self.solution_paths:
            self.skipTest("找不到 QUESTION-10071 的解答程式。請先把對應 Python 檔放在同一個資料夾中。")

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

        return completed.stdout.strip()

    def brute_force_count(self, numbers):
        """用暴力法計算正確答案。

        因為單元測試只會用很小的集合，
        直接枚舉所有 a, b, c, d, e, f 是可行的，
        也能避免人工手算答案時出錯。
        """
        count = 0
        for a, b, c, d, e, f in product(numbers, repeat=6):
            if a + b + c + d + e == f:
                count += 1
        return count

    def assert_count(self, numbers):
        """把集合轉成題目輸入格式，並驗證所有解答檔的輸出。"""
        if not self.solution_paths:
            self.skipTest("找不到 QUESTION-10071 的解答程式。請先把對應 Python 檔放在同一個資料夾中。")

        input_data = str(len(numbers)) + "\n" + "\n".join(map(str, numbers)) + "\n"
        expected_output = str(self.brute_force_count(numbers))

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name, numbers=numbers):
                actual_output = self.run_solution(solution_path, input_data)
                self.assertEqual(actual_output, expected_output)

    def test_single_zero(self):
        # 只有 0 時，唯一成立的情況就是六個位置全部都選 0。
        self.assert_count([0])

    def test_single_positive_number(self):
        # 只有正數時，五個相同正數相加不可能仍等於集合中的原數字。
        self.assert_count([1])

    def test_zero_and_one(self):
        # 包含 0 與 1，可以測到「部分位置選 0、部分位置選 1」的組合情況。
        self.assert_count([0, 1])

    def test_negative_zero_positive(self):
        # 同時含有負數、0、正數，可測到較平衡的加總組合。
        self.assert_count([-1, 0, 1])

    def test_sparse_values(self):
        # 使用間距較大的值，檢查程式是否正確處理非連續數字。
        self.assert_count([-2, 0, 2])


if __name__ == "__main__":
    unittest.main()