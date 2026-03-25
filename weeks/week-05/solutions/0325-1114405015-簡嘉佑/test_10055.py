import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class TestUVA10055(unittest.TestCase):
    """UVA 10055（依題面內容：函數增減性反轉與區間查詢）單元測試。"""

    # 可用環境變數 TARGET_SOLUTION 指定受測檔案，預設為 10055.py。
    SOLUTION_FILE = Path(__file__).with_name(os.getenv("TARGET_SOLUTION", "10055.py"))

    def run_solution(self, input_data: str) -> list[str]:
        """執行受測程式，回傳整理過的輸出行。"""
        # 先確認受測檔案存在，讓錯誤訊息更明確。
        self.assertTrue(
            self.SOLUTION_FILE.exists(),
            f"找不到受測檔案：{self.SOLUTION_FILE}，請先建立 10055.py",
        )

        # 透過 subprocess 模擬 OJ 的 stdin/stdout 執行環境。
        completed = subprocess.run(
            [sys.executable, str(self.SOLUTION_FILE)],
            input=input_data,
            text=True,
            capture_output=True,
            check=False,
        )

        # 要求程式正常結束（return code = 0），否則印出 stderr 方便除錯。
        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        # 去除空白行，避免格式差異影響比較。
        return [line.strip() for line in completed.stdout.splitlines() if line.strip()]

    @staticmethod
    def expected_outputs(n: int, ops: list[tuple[int, ...]]) -> list[str]:
        """以直觀模擬方式計算所有查詢的正確輸出，作為參考正解。

        用暴力模擬（O(N) 查詢）取代 Fenwick Tree，邏輯簡單可信，
        適合拿來驗證受測程式是否正確。
        """
        # state[i] = 0 表示 fi 是增函數，1 表示減函數；初始全為增函數。
        state = [0] * (n + 1)
        ans: list[str] = []

        for op in ops:
            if op[0] == 1:
                _, i = op
                # v=1：用 XOR 反轉第 i 個函數的增減性（0→1 或 1→0）。
                state[i] ^= 1
            else:
                _, l, r = op
                # v=2：計算區間 [l, r] 內減函數個數。
                # 奇數個減函數 -> 複合結果為減函數(1)；偶數 -> 增函數(0)。
                parity = sum(state[l : r + 1]) % 2
                ans.append(str(parity))

        return ans

    @staticmethod
    def build_input(n: int, ops: list[tuple[int, ...]]) -> str:
        """把操作序列組成題目要求的輸入格式。

        格式：第一行 「N Q」，接下來每行一個操作。
        """
        # 第一行：函數數量 N 與操作數量 Q。
        lines = [f"{n} {len(ops)}"]
        # 每個操作獨立一行，欄位以空白分隔。
        for op in ops:
            lines.append(" ".join(map(str, op)))
        return "\n".join(lines) + "\n"

    def test_basic_case(self) -> None:
        """固定案例：涵蓋反轉、單點查詢、多次查詢與重複反轉。"""
        n = 5
        ops: list[tuple[int, ...]] = [
            (2, 1, 5),  # 初始全增函數，區間內 0 個減函數，答案 0
            (1, 3),     # f3 反轉為減函數
            (2, 1, 5),  # 區間有 1 個減函數（f3），答案 1
            (2, 2, 4),  # 區間 [2,4] 只含 f3 為減，答案 1
            (1, 3),     # f3 再次反轉回增函數
            (2, 2, 4),  # 區間再查詢，0 個減函數，答案 0
            (1, 1),     # f1 反轉為減函數
            (1, 5),     # f5 反轉為減函數
            (2, 1, 5),  # f1、f5 為減，共 2 個，偶數，答案 0
            (2, 5, 5),  # 單點查詢 f5（減函數），答案 1
        ]

        input_data = self.build_input(n, ops)
        # 以參考模擬器計算預期值，再與受測程式輸出逐行比對。
        expected = self.expected_outputs(n, ops)
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)

    def test_random_cases(self) -> None:
        """隨機操作測試：避免只對固定資料過關。"""
        # 固定亂數種子，確保每次執行可重現相同的操作序列。
        random.seed(10055)

        n = 40   # 函數總數
        q = 120  # 操作總數
        ops: list[tuple[int, ...]] = []

        for _ in range(q):
            # 45% 機率產生 update（v=1），其餘產生 query（v=2），
            # 確保測試中兩種操作都有足夠的覆蓋率。
            if random.random() < 0.45:
                i = random.randint(1, n)
                ops.append((1, i))
            else:
                l = random.randint(1, n)
                r = random.randint(l, n)  # 確保 l <= r
                ops.append((2, l, r))

        input_data = self.build_input(n, ops)
        # 預期值由暴力模擬即時計算，與受測程式輸出逐行比對。
        expected = self.expected_outputs(n, ops)
        actual = self.run_solution(input_data)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
