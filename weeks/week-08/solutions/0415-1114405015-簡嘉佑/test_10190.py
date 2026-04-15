import importlib.util
import pathlib
import re
import subprocess
import sys
import unittest


class TestUVA10190(unittest.TestCase):
    """UVA 10190 單元測試（自動傘 / 雨量計算）。"""

    @classmethod
    def setUpClass(cls):
        # 預設受測檔名：solution_10190.py（與本測試檔放同資料夾）
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10190.py"

    def run_solver(self, input_data: str) -> str:
        """
        執行受測程式，支援兩種介面：
        1) solve(input_data) -> str
        2) 直接執行腳本並讀取 stdout
        """
        if not self.solution_path.exists():
            self.fail(
                f"找不到受測檔案: {self.solution_path.name}。"
                "請在同一資料夾建立 solution_10190.py。"
            )

        spec = importlib.util.spec_from_file_location("solution_10190", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("無法載入 solution_10190.py。")

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

    def parse_output_value(self, output: str) -> float:
        """解析輸出值，並驗證格式為小數點後兩位。"""
        text = output.strip()
        self.assertTrue(text, "輸出不可為空。")

        # 題目要求精確到小數點後兩位，這裡強制檢查格式
        self.assertRegex(text, r"^-?\d+\.\d{2}$", "輸出格式需為小數點後兩位，例如 123.45")

        return float(text)

    def assert_volume(self, input_data: str, expected: float):
        actual_text = self.run_solver(input_data)
        actual_value = self.parse_output_value(actual_text)
        self.assertAlmostEqual(actual_value, expected, places=2)

    def test_no_umbrella(self):
        """N=0：沒有任何傘，雨量 = W * T * V。"""
        input_data = """\
0 10 5 3
"""
        self.assert_volume(input_data, 150.00)

    def test_single_stationary_umbrella(self):
        """單把靜止傘：未覆蓋長度固定。"""
        input_data = """\
1 10 5 2
2 4 0
"""
        # 覆蓋 4，未覆蓋 6 => 6 * 5 * 2 = 60
        self.assert_volume(input_data, 60.00)

    def test_two_stationary_non_overlapping(self):
        """兩把靜止傘不重疊：聯集長度為各自長度加總。"""
        input_data = """\
2 10 4 1
0 3 0
6 2 0
"""
        # 聯集覆蓋 5，未覆蓋 5 => 5 * 4 * 1 = 20
        self.assert_volume(input_data, 20.00)

    def test_two_stationary_overlapping(self):
        """兩把靜止傘重疊：覆蓋長度要算聯集，不可重複加總。"""
        input_data = """\
2 10 3 2
1 5 0
4 4 0
"""
        # [1,6] 與 [4,8] 聯集為 [1,8]，覆蓋 7，未覆蓋 3 => 3 * 3 * 2 = 18
        self.assert_volume(input_data, 18.00)

    def test_full_coverage_stationary(self):
        """全覆蓋情況：整段路都被遮住，雨量應為 0。"""
        input_data = """\
2 10 7 5
0 4 0
4 6 0
"""
        self.assert_volume(input_data, 0.00)

    def test_single_moving_umbrella(self):
        """單把移動傘：雖位置變化，但覆蓋長度固定。"""
        input_data = """\
1 10 5 3
2 4 1
"""
        # 單把傘長度固定 4，未覆蓋固定 6 => 6 * 5 * 3 = 90
        self.assert_volume(input_data, 90.00)


if __name__ == "__main__":
    unittest.main(verbosity=2)
