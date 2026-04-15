import importlib.util
import pathlib
import subprocess
import sys
import unittest


class TestUVA10222(unittest.TestCase):
    """UVA 10222 - Decode the Mad man 單元測試。"""

    @classmethod
    def setUpClass(cls):
        # 預設受測檔名為 solution_10222.py，與本測試檔位於同一資料夾
        cls.base_dir = pathlib.Path(__file__).resolve().parent
        cls.solution_path = cls.base_dir / "solution_10222.py"

        # 題目給的是標準鍵盤配置；本測試依規則「輸入字元向左回推 2 個鍵」解碼
        # 例如 r -> e（與題目敘述範例一致）
        cls.rows = [
            "`1234567890-=",
            "qwertyuiop[]\\",
            "asdfghjkl;'",
            "zxcvbnm,./",
        ]

    def run_solver(self, input_data: str) -> str:
        """執行受測程式，支援 solve(input_data) 與腳本兩種介面。"""
        if not self.solution_path.exists():
            self.fail(
                f"找不到受測檔案: {self.solution_path.name}。"
                "請在同一資料夾建立 solution_10222.py。"
            )

        spec = importlib.util.spec_from_file_location("solution_10222", self.solution_path)
        if spec is None or spec.loader is None:
            self.fail("無法載入 solution_10222.py。")

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

    def expected_decode(self, text: str) -> str:
        """根據題目規則進行預期解碼：每個字元往左回推 2 個鍵。"""
        out = []

        for ch in text:
            if ch == "\n":
                out.append(ch)
                continue

            lowered = ch.lower()
            replaced = False
            for row in self.rows:
                idx = row.find(lowered)
                if idx >= 2:
                    out.append(row[idx - 2])
                    replaced = True
                    break

            # 空白或不在映射中的字元，保持原樣
            if not replaced:
                out.append(ch)

        return "".join(out)

    def assert_decoded(self, input_data: str):
        actual = self.run_solver(input_data)
        expected = self.expected_decode(input_data)
        self.assertEqual(actual.rstrip("\n"), expected.rstrip("\n"))

    def test_single_char_example(self):
        """題目示例：r 應解碼為 e。"""
        self.assert_decoded("r\n")

    def test_letters_symbols_and_space(self):
        """混合字母、符號、空白。"""
        self.assert_decoded("jr;;p ypw;f [t ept;f!\n")

    def test_numbers_and_punctuation(self):
        """測試數字與標點符號映射。"""
        self.assert_decoded("34567890-= []\\ ;' ,./\n")

    def test_multi_line_input(self):
        """多行輸入應逐行解碼，保留換行結構。"""
        data = "r\nqwerty\n12345\n"
        self.assert_decoded(data)

    def test_keep_unmapped_chars(self):
        """不在鍵盤映射內的字元（例如 !）應保持原樣。"""
        self.assert_decoded("r! t?\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
