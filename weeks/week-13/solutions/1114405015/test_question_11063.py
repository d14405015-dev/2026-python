"""UVA 11063 單元測試：RGB 轉 XYZ 並計算平均亮度 Y。

使用方式：
1. 將你的 11063 解答程式放在同一資料夾，檔名建議為 solution_11063.py。
2. 解答可提供以下任一介面：
   - solve(input_text: str) -> str
   - process(input_text: str) -> str
   - process_input(input_text: str) -> str
   - main()（由測試代入 stdin 並擷取 stdout）
3. 執行：python -m unittest -v test_question_11063.py
"""

from __future__ import annotations

import importlib.util
import io
import random
import re
import sys
import unittest
from pathlib import Path
from typing import Callable, List, Sequence, Tuple


Pixel = Tuple[int, int, int]


def xyz_from_rgb(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """依題目公式將 RGB 轉為 XYZ。"""
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return x, y, z


def build_input(n: int, pixels: Sequence[Pixel]) -> str:
    """把像素資料組成題目指定的輸入字串。"""
    assert len(pixels) == n * n
    lines: List[str] = [str(n)]
    idx = 0
    for _ in range(n):
        row_tokens: List[str] = []
        for _ in range(n):
            r, g, b = pixels[idx]
            idx += 1
            row_tokens.extend([str(r), str(g), str(b)])
        lines.append(" ".join(row_tokens))
    return "\n".join(lines) + "\n"


def reference_output(n: int, pixels: Sequence[Pixel]) -> str:
    """用參考實作產生正確輸出，作為測試基準。"""
    ys: List[float] = []
    out_lines: List[str] = []

    for r, g, b in pixels:
        x, y, z = xyz_from_rgb(r, g, b)
        ys.append(y)
        out_lines.append(f"{x:.4f} {y:.4f} {z:.4f}")

    avg_y = sum(ys) / (n * n)
    out_lines.append(f"The average of Y is {avg_y:.4f}")
    return "\n".join(out_lines)


def normalize_output(text: str) -> str:
    """正規化輸出：去除每行尾端空白，統一換行。"""
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return "\n".join(lines)


def _load_student_runner() -> Callable[[str], str]:
    """載入學生解答並回傳統一呼叫介面 runner(input_text) -> output_text。"""
    current_dir = Path(__file__).resolve().parent
    candidate_files = [
        "solution_11063-easy.py",
        "solution_11063-hand.py",
        "solution_11063.py",
        "question_11063.py",
        "uva_11063.py",
    ]

    target_file = None
    for filename in candidate_files:
        path = current_dir / filename
        if path.exists():
            target_file = path
            break

    if target_file is None:
        raise AssertionError(
            "找不到 11063 解答檔。請在同資料夾放置 solution_11063.py（或候選檔名）。"
        )

    spec = importlib.util.spec_from_file_location("student_solution_11063", target_file)
    if spec is None or spec.loader is None:
        raise AssertionError(f"無法載入解答檔：{target_file.name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 優先使用純函式介面，測試會更穩定。
    for fn_name in ["solve", "process", "process_input"]:
        fn = getattr(module, fn_name, None)
        if callable(fn):
            def runner(input_text: str, _fn=fn) -> str:
                result = _fn(input_text)
                if isinstance(result, str):
                    return result
                if isinstance(result, list):
                    return "\n".join(map(str, result))
                return str(result)

            return runner

    # 若只有 main()，就模擬 stdin/stdout 來執行。
    main_fn = getattr(module, "main", None)
    if callable(main_fn):
        def runner(input_text: str, _main=main_fn) -> str:
            old_stdin, old_stdout = sys.stdin, sys.stdout
            try:
                sys.stdin = io.StringIO(input_text)
                sys.stdout = io.StringIO()
                _main()
                return sys.stdout.getvalue()
            finally:
                sys.stdin, sys.stdout = old_stdin, old_stdout

        return runner

    raise AssertionError(
        f"在 {target_file.name} 中找不到 solve/process/process_input/main 可用介面。"
    )


class TestUVA11063(unittest.TestCase):
    """驗證數值正確性、輸出格式與平均亮度計算。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_student_runner()

    def assert_case(self, n: int, pixels: Sequence[Pixel]) -> None:
        """以參考輸出對照學生輸出。"""
        input_text = build_input(n, pixels)
        expected = normalize_output(reference_output(n, pixels))
        actual = normalize_output(self.__class__.runner(input_text))

        # 先做完整文字比對，確保格式與四捨五入位數一致。
        self.assertEqual(actual, expected)

        # 再做結構檢查：應該有 n*n 行像素 + 1 行平均亮度。
        lines = actual.splitlines()
        self.assertEqual(len(lines), n * n + 1)
        self.assertRegex(lines[-1], r"^The average of Y is -?\d+\.\d{4}$")

    def test_single_black_pixel(self) -> None:
        """最小像素值全零。"""
        self.assert_case(1, [(0, 0, 0)])

    def test_single_white_pixel(self) -> None:
        """最大像素值全 255。"""
        self.assert_case(1, [(255, 255, 255)])

    def test_two_by_two_mixed_pixels(self) -> None:
        """2x2 混合案例，檢查一般情況。"""
        pixels = [
            (255, 3, 192),
            (128, 64, 32),
            (0, 255, 0),
            (12, 34, 56),
        ]
        self.assert_case(2, pixels)

    def test_random_cases(self) -> None:
        """隨機回歸測試，提升正確性信心。"""
        rng = random.Random(11063)
        for _ in range(30):
            n = rng.randint(1, 5)
            pixels = [
                (rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255))
                for _ in range(n * n)
            ]
            self.assert_case(n, pixels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
