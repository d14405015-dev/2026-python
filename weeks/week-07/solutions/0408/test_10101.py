import subprocess
import sys
import unittest
from pathlib import Path


class TestQuestion10101(unittest.TestCase):
    """測試 QUESTION-10101 解答程式是否正確處理「移動一根木棒」。"""

    DIGIT_MASKS = {
        0: 0b1111110,
        1: 0b0110000,
        2: 0b1101101,
        3: 0b1111001,
        4: 0b0110011,
        5: 0b1011011,
        6: 0b1011111,
        7: 0b1110000,
        8: 0b1111111,
        9: 0b1111011,
    }

    MASK_TO_DIGIT = {mask: digit for digit, mask in DIGIT_MASKS.items()}

    @classmethod
    def setUpClass(cls):
        # 測試檔與解答程式預期都放在同一個學生作業資料夾中。
        cls.base_dir = Path(__file__).resolve().parent
        cls.solution_paths = cls._find_solution_files()

    @classmethod
    def _find_solution_files(cls):
        """找出同目錄下與 10101 題目對應的解答檔。"""
        python_files = sorted(
            path
            for path in cls.base_dir.glob("*.py")
            if path.name != Path(__file__).name and not path.name.startswith("test_")
        )

        if not python_files:
            return []

        preferred_names = [
            "10101.py",
            "10101-easy.py",
            "10101-manual.py",
            "question_10101.py",
            "solution_10101.py",
            "uva_10101.py",
        ]

        selected_files = []
        for preferred_name in preferred_names:
            for path in python_files:
                if path.name.lower() == preferred_name and path not in selected_files:
                    selected_files.append(path)

        for path in python_files:
            if "10101" in path.name.lower() and path not in selected_files:
                selected_files.append(path)

        return selected_files

    def run_solution(self, solution_path, input_data):
        """執行學生解答程式，回傳標準輸出內容（去除首尾空白）。"""
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

    def parse_expression_value(self, expression):
        """計算只含 + / - 的整條算式值（支援負號）。"""
        index = 0
        total = 0
        while index < len(expression):
            sign = 1
            if expression[index] == "+":
                index += 1
            elif expression[index] == "-":
                sign = -1
                index += 1

            start = index
            while index < len(expression) and expression[index].isdigit():
                index += 1
            total += sign * int(expression[start:index])

        return total

    def is_equation_true(self, expression):
        """檢查等式是否成立。"""
        equal_index = expression.index("=")
        left_value = self.parse_expression_value(expression[:equal_index])
        right_value = self.parse_expression_value(expression[equal_index + 1:])
        return left_value == right_value

    def enumerate_one_move_results(self, expression):
        """列舉從 expression 出發，移動一根木棒後可得到的所有合法等式字串。"""
        chars = list(expression)
        digit_positions = [idx for idx, ch in enumerate(chars) if ch.isdigit()]

        results = set()

        for source_pos in digit_positions:
            source_digit = int(chars[source_pos])
            source_mask = self.DIGIT_MASKS[source_digit]

            for target_pos in digit_positions:
                target_digit = int(chars[target_pos])
                target_mask = self.DIGIT_MASKS[target_digit]

                for remove_bit in range(7):
                    remove_mask = 1 << remove_bit
                    if not (source_mask & remove_mask):
                        continue

                    source_after_remove = source_mask ^ remove_mask

                    for add_bit in range(7):
                        add_mask = 1 << add_bit

                        if source_pos == target_pos:
                            if remove_bit == add_bit:
                                continue
                            if source_mask & add_mask:
                                continue
                            target_after_add = source_after_remove | add_mask
                            if target_after_add not in self.MASK_TO_DIGIT:
                                continue

                            candidate = chars[:]
                            candidate[source_pos] = str(self.MASK_TO_DIGIT[target_after_add])
                        else:
                            if target_mask & add_mask:
                                continue
                            if source_after_remove not in self.MASK_TO_DIGIT:
                                continue

                            target_after_add = target_mask | add_mask
                            if target_after_add not in self.MASK_TO_DIGIT:
                                continue

                            candidate = chars[:]
                            candidate[source_pos] = str(self.MASK_TO_DIGIT[source_after_remove])
                            candidate[target_pos] = str(self.MASK_TO_DIGIT[target_after_add])

                        candidate_expression = "".join(candidate)
                        if self.is_equation_true(candidate_expression):
                            results.add(candidate_expression + "#")

        return results

    def assert_valid_output(self, input_line):
        """驗證程式輸出是否符合題意。

        - 若有可行解：輸出必須是其中一個合法解
        - 若無可行解：輸出必須是 No
        """
        hash_index = input_line.find("#")
        base_expression = input_line[:hash_index]
        expected_results = self.enumerate_one_move_results(base_expression)

        if not self.solution_paths:
            self.skipTest("找不到 QUESTION-10101 的解答程式。請先把對應 Python 檔放在同一個資料夾中。")

        for solution_path in self.solution_paths:
            with self.subTest(solution=solution_path.name, expression=input_line):
                actual = self.run_solution(solution_path, input_line + "\n")
                if expected_results:
                    self.assertIn(actual, expected_results)
                else:
                    self.assertEqual(actual, "No")

    def test_addition_case(self):
        # 基本加法案例。
        self.assert_valid_output("1+1=3#")

    def test_subtraction_case(self):
        # 基本減法案例。
        self.assert_valid_output("9-3=5#")

    def test_with_zero(self):
        # 包含 0 的案例。
        self.assert_valid_output("5+3=9#")

    def test_multi_digit_case(self):
        # 多位數案例，確保位值變化處理正確。
        self.assert_valid_output("19-5=13#")

    def test_no_solution_case(self):
        # 無解案例。
        self.assert_valid_output("1+1=4#")

    def test_hash_suffix_ignored(self):
        # # 後面額外字元應忽略。
        self.assert_valid_output("1+1=3#ignored")

    def test_already_true_equation(self):
        # 就算原式成立，仍需檢查輸出是否符合「移動一根木棒後」的合法結果。
        self.assert_valid_output("3+3=6#")


if __name__ == "__main__":
    unittest.main()
