import importlib.util
import math
import pathlib
import re
import subprocess
import sys
import unittest


class TestUVA10193(unittest.TestCase):
    """UVA 10193 單元測試。"""

    @classmethod
    def setUpClass(cls):
        # 預設受測檔名：solution_10193.py（與本測試檔放同資料夾）
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10193.py"

    def run_solver(self, input_data: str) -> str:
        """
        支援兩種受測介面：
        1) solve(input_data) -> str
        2) 直接執行腳本，從 stdin 讀取、stdout 輸出
        """
        if not self.solution_path.exists():
            self.fail(
                f"找不到受測檔案: {self.solution_path.name}。"
                "請在同一資料夾建立 solution_10193.py。"
            )

        spec = importlib.util.spec_from_file_location("solution_10193", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("無法載入 solution_10193.py。")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "solve") and callable(module.solve):
            result = module.solve(input_data)
            self.assertIsInstance(result, str, "solve(input_data) 必須回傳字串。")
            return result

        completed = subprocess.run(
            [sys.executable, str(self.solution_path)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            self.fail(
                "受測程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            )
        return completed.stdout

    @staticmethod
    def parse_output_value(output: str) -> int:
        """解析輸出為整數，並檢查格式。"""
        text = output.strip()
        if not text:
            raise AssertionError("輸出不可為空。")
        if not re.fullmatch(r"-?\d+", text):
            raise AssertionError(f"輸出格式錯誤，應為整數，實際為: {text}")
        return int(text)

    @staticmethod
    def expected_min_sum(a: int) -> int:
        """
        由公式推導：
        arctan(1/a) = arctan(1/b) + arctan(1/c)
        可化為：bc - a(b + c) = 1
        再化為：
            (b - a)(c - a) = a^2 + 1

        令 d = b-a, e = c-a，則 d*e = a^2+1，
        且 b+c = 2a + d + e。
        因此只要在所有因數配對中最小化 d+e 即可。
        """
        n = a * a + 1
        best = 10**30
        root = int(math.isqrt(n))
        for d in range(1, root + 1):
            if n % d == 0:
                e = n // d
                best = min(best, 2 * a + d + e)
        return best

    def assert_answer(self, a: int, expected: int):
        actual = self.parse_output_value(self.run_solver(f"{a}\n"))
        self.assertEqual(actual, expected)

    def test_a_1(self):
        """a=1 的基本案例。"""
        self.assert_answer(1, 5)

    def test_a_3(self):
        """a=3 的案例。"""
        self.assert_answer(3, 13)

    def test_a_7(self):
        """a=7 的案例。"""
        self.assert_answer(7, 29)

    def test_a_8(self):
        """a=8 的案例。"""
        self.assert_answer(8, 34)

    def test_a_10(self):
        """a=10 的案例。"""
        self.assert_answer(10, 122)

    def test_small_range_exhaustive(self):
        """小範圍窮舉驗證：a=1..50 都要符合最小 b+c。"""
        for a in range(1, 51):
            expected = self.expected_min_sum(a)
            actual = self.parse_output_value(self.run_solver(f"{a}\n"))
            self.assertEqual(actual, expected, f"a={a} 時答案錯誤")


if __name__ == "__main__":
    unittest.main(verbosity=2)
