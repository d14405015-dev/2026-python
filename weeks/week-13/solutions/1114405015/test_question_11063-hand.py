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
    x = 0.5149 * r + 0.3244 * g + 0.1607 * b
    y = 0.2654 * r + 0.6704 * g + 0.0642 * b
    z = 0.0248 * r + 0.1248 * g + 0.8504 * b
    return x, y, z


def build_input(n: int, pixels: Sequence[Pixel]) -> str:
    lines: List[str] = [str(n)]
    idx = 0
    for _ in range(n):
        row: List[str] = []
        for _ in range(n):
            r, g, b = pixels[idx]
            idx += 1
            row.extend([str(r), str(g), str(b)])
        lines.append(" ".join(row))
    return "\n".join(lines) + "\n"


def reference_output(n: int, pixels: Sequence[Pixel]) -> str:
    ys: List[float] = []
    out: List[str] = []
    for r, g, b in pixels:
        x, y, z = xyz_from_rgb(r, g, b)
        ys.append(y)
        out.append(f"{x:.4f} {y:.4f} {z:.4f}")
    out.append(f"The average of Y is {sum(ys) / (n * n):.4f}")
    return "\n".join(out)


def normalize_output(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def _load_runner() -> Callable[[str], str]:
    path = Path(__file__).resolve().parent / "solution_11063-hand.py"
    if not path.exists():
        raise AssertionError("找不到 solution_11063-hand.py")

    spec = importlib.util.spec_from_file_location("student_solution_11063_hand", path)
    if spec is None or spec.loader is None:
        raise AssertionError("無法載入 solution_11063-hand.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

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

    raise AssertionError("找不到可測試介面")


class TestUVA11063Hand(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runner = _load_runner()

    def assert_case(self, n: int, pixels: Sequence[Pixel]) -> None:
        expected = normalize_output(reference_output(n, pixels))
        actual = normalize_output(self.__class__.runner(build_input(n, pixels)))
        self.assertEqual(actual, expected)
        lines = actual.splitlines()
        self.assertEqual(len(lines), n * n + 1)
        self.assertRegex(lines[-1], r"^The average of Y is -?\d+\.\d{4}$")

    def test_single_black_pixel(self) -> None:
        self.assert_case(1, [(0, 0, 0)])

    def test_single_white_pixel(self) -> None:
        self.assert_case(1, [(255, 255, 255)])

    def test_two_by_two_mixed_pixels(self) -> None:
        self.assert_case(2, [(255, 3, 192), (128, 64, 32), (0, 255, 0), (12, 34, 56)])

    def test_random_cases(self) -> None:
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
