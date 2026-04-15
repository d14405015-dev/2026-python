import importlib.util
import math
import pathlib
import re
import subprocess
import sys
import unittest


class TestUVA10221(unittest.TestCase):
    """UVA 10221 - Satellites 單元測試。"""

    @classmethod
    def setUpClass(cls):
        # 預設受測檔案名稱，與本測試檔放在同一資料夾
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10221.py"

    def run_solver(self, input_data: str) -> str:
        """
        支援兩種受測方式：
        1) 匯入後呼叫 solve(input_data) -> str
        2) 若無 solve，則直接以腳本方式執行
        """
        if not self.solution_path.exists():
            self.fail(
                f"找不到受測檔案: {self.solution_path.name}。"
                "請在同一資料夾建立 solution_10221.py。"
            )

        spec = importlib.util.spec_from_file_location("solution_10221", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("無法載入 solution_10221.py。")

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
    def expected_arc_chord(s: int, a: int, unit: str) -> tuple[float, float]:
        """
        根據題意計算期望值：
        1) r = 6440 + s
        2) 角度若為 min 需先換成 deg
        3) 取較小圓心角（若 >180，改成 360-a）
        4) arc = r * theta, chord = 2r*sin(theta/2)
        """
        r = 6440.0 + float(s)

        angle_deg = float(a)
        if unit == "min":
            angle_deg /= 60.0

        if angle_deg > 180.0:
            angle_deg = 360.0 - angle_deg

        theta = math.radians(angle_deg)
        arc = r * theta
        chord = 2.0 * r * math.sin(theta / 2.0)
        return arc, chord

    @staticmethod
    def parse_output_lines(output: str) -> list[tuple[float, float]]:
        """把輸出每一行解析成 (arc, chord) 浮點數。"""
        lines = [line.strip() for line in output.strip().splitlines() if line.strip()]
        parsed: list[tuple[float, float]] = []

        for line in lines:
            parts = line.split()
            if len(parts) != 2:
                raise AssertionError(f"每行應有兩個數值，實際為: {line}")

            # 允許一般浮點格式（含科學記號）
            if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", parts[0]):
                raise AssertionError(f"第一個輸出不是合法數值: {parts[0]}")
            if not re.fullmatch(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", parts[1]):
                raise AssertionError(f"第二個輸出不是合法數值: {parts[1]}")

            parsed.append((float(parts[0]), float(parts[1])))

        return parsed

    def assert_case(self, s: int, a: int, unit: str, tol: float = 1e-5):
        input_data = f"{s} {a} {unit}\n"
        out = self.run_solver(input_data)
        rows = self.parse_output_lines(out)

        self.assertEqual(len(rows), 1, "單一測資輸入時，輸出應只有一行")
        actual_arc, actual_chord = rows[0]
        exp_arc, exp_chord = self.expected_arc_chord(s, a, unit)

        self.assertAlmostEqual(actual_arc, exp_arc, delta=tol)
        self.assertAlmostEqual(actual_chord, exp_chord, delta=tol)

    def test_zero_angle(self):
        """角度為 0：弧長與弦長都應為 0。"""
        self.assert_case(0, 0, "deg")

    def test_straight_angle(self):
        """180 度：弧長為半圓長、弦長為直徑。"""
        self.assert_case(0, 180, "deg")

    def test_over_180_degree(self):
        """超過 180 度時要取較小角，例如 300 度應視為 60 度。"""
        self.assert_case(100, 300, "deg")

    def test_minute_unit(self):
        """分（min）單位換算測試：60 min = 1 deg。"""
        # 先個別比對理論值
        self.assert_case(500, 60, "min")
        self.assert_case(500, 1, "deg")

        # 再直接比較兩次輸出是否一致
        out1 = self.parse_output_lines(self.run_solver("500 60 min\n"))[0]
        out2 = self.parse_output_lines(self.run_solver("500 1 deg\n"))[0]
        self.assertAlmostEqual(out1[0], out2[0], delta=1e-5)
        self.assertAlmostEqual(out1[1], out2[1], delta=1e-5)

    def test_multiple_lines_input(self):
        """多筆輸入：應逐行輸出對應答案。"""
        input_data = """\
500 30 deg
700 60 min
200 45 deg
"""
        output_rows = self.parse_output_lines(self.run_solver(input_data))
        self.assertEqual(len(output_rows), 3)

        cases = [(500, 30, "deg"), (700, 60, "min"), (200, 45, "deg")]
        for i, (s, a, unit) in enumerate(cases):
            exp_arc, exp_chord = self.expected_arc_chord(s, a, unit)
            self.assertAlmostEqual(output_rows[i][0], exp_arc, delta=1e-5)
            self.assertAlmostEqual(output_rows[i][1], exp_chord, delta=1e-5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
