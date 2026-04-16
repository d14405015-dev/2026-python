"""UVA 118（Mutant Flatworld Explorers）單元測試。

用途：
- 自動掃描同資料夾下 `question_118*.py` 解答程式。
- 透過 subprocess 執行解答，餵入測資並比對輸出。

執行方式：
- 在目前資料夾執行：python -m unittest -v test_question_118.py
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


# 測試檔所在目錄（solutions/0311）
BASE_DIR = Path(__file__).resolve().parent


# UVA 118 常見標準範例：
# 第 2 台機器人會 LOST，並在掉落前位置留下 scent。
SAMPLE_INPUT = """5 3
1 1 E
RFRFRFRF
3 2 N
FRRFLLFFRRFLL
0 3 W
LLFFFLFLFL
"""

SAMPLE_EXPECTED_OUTPUT = """1 1 E
3 3 N LOST
2 3 S
"""


# 額外案例：驗證 scent 生效。
# 1) 第一台在 (1,1,E) 嘗試前進會掉落，留下 scent。
# 2) 第二台同位置同方向再執行 F，應忽略該指令，不會掉落。
EXTRA_CASES = [
    (
        """1 1
1 1 E
F
1 1 E
F
""",
        """1 1 E LOST
1 1 E
""",
    ),
    (
        """2 2
0 0 N
RFFLFF
""",
        """2 2 N
""",
    ),
]


def discover_solution_scripts() -> list[Path]:
    """找出需要測試的 UVA 118 解答程式。

    規則：
    - 只測目前資料夾下檔名符合 `question_118*.py` 的檔案。
    - 排除測試檔與本測試檔本身。
    """
    scripts: list[Path] = []
    for path in sorted(BASE_DIR.glob("question_118*.py")):
        if path.name == Path(__file__).name:
            continue
        if path.name.startswith("test_"):
            continue
        scripts.append(path)
    return scripts


def run_script(script_path: Path, input_data: str) -> str:
    """執行解答程式並回傳標準輸出。

    使用 sys.executable，確保與目前測試環境使用相同 Python 版本。
    """
    completed = subprocess.run(
        [sys.executable, str(script_path)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=str(BASE_DIR),
        check=False,
    )

    if completed.returncode != 0:
        raise AssertionError(
            f"程式執行失敗：{script_path.name}\n"
            f"return code: {completed.returncode}\n"
            f"stderr:\n{completed.stderr}"
        )

    return completed.stdout


def normalize_output(text: str) -> str:
    """正規化輸出，避免平台換行與尾端空白差異造成誤判。"""
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]

    # 移除尾端空行，再補一個統一換行，讓字串比對穩定。
    while lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines) + "\n"


class TestUVA118Solutions(unittest.TestCase):
    """驗證本資料夾所有 UVA 118 解答程式。"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.scripts = discover_solution_scripts()

    def test_found_solution_scripts(self) -> None:
        """確認至少有一個可測試的解答程式。"""
        self.assertTrue(
            self.scripts,
            "找不到 question_118*.py 解答檔，請先放入解答程式。",
        )

    def test_sample_case(self) -> None:
        """驗證 UVA 118 的標準範例輸入輸出。"""
        expected = normalize_output(SAMPLE_EXPECTED_OUTPUT)

        for script in self.scripts:
            with self.subTest(script=script.name):
                actual = normalize_output(run_script(script, SAMPLE_INPUT))
                self.assertEqual(actual, expected)

    def test_extra_cases(self) -> None:
        """驗證 scent 行為與基本移動方向是否正確。"""
        for script in self.scripts:
            for case_input, case_expected in EXTRA_CASES:
                with self.subTest(script=script.name):
                    actual = normalize_output(run_script(script, case_input))
                    expected = normalize_output(case_expected)
                    self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
