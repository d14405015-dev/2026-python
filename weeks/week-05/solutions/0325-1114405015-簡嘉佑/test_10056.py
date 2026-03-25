"""UVA 10056 單元測試 — What is the Probability?

題目摘要：
  N 個玩家輪流擲骰子，每次擲出「成功事件」的機率為 p。
  玩家依序 1, 2, ..., N, 1, 2, ... 輪流，第一個成功者獲勝。
  求第 i 個玩家獲勝的機率。

數學推導：
  設 q = 1 - p（單次失敗機率）。
  玩家 i 的第 1 輪獲勝機率 = q^(i-1) * p
  （前面 i-1 人全失敗，第 i 人成功）
  每多走完一整輪（N 個人全失敗），機率再乘以 q^N。
  整體為等比級數（公比 r = q^N）：
    P(玩家 i 獲勝) = q^(i-1) * p * (1 + r + r^2 + …)
                   = q^(i-1) * p / (1 - q^N)

輸入格式：
  第一行：測試組數 S
  接下來 S 行，每行：「N p i」
    N = 玩家數，p = 成功機率，i = 指定玩家序號（1 ≤ i ≤ N）

輸出格式：
  每組輸出一行，機率精確到小數點後四位。

使用方式：
  python test_10056.py                         # 測試 10056.py（預設）
  TARGET_SOLUTION=10056-manual.py python test_10056.py  # 測試手打版本
"""

import os
import random
import subprocess
import sys
import unittest
from pathlib import Path


class TestUVA10056(unittest.TestCase):
    """UVA 10056（確定第 i 個玩家獲勝機率）單元測試。"""

    # 透過環境變數 TARGET_SOLUTION 指定受測檔案，預設為 10056.py。
    # 這樣同一份測試就能同時驗證 10056.py 和 10056-manual.py。
    SOLUTION_FILE = Path(__file__).with_name(
        os.getenv("TARGET_SOLUTION", "10056.py")
    )

    # ------------------------------------------------------------------ #
    # 輔助方法                                                             #
    # ------------------------------------------------------------------ #

    def run_solution(self, input_data: str) -> list[str]:
        """執行受測程式，以 stdin 傳入題目輸入，回傳整理後的輸出行列表。

        先確認受測檔案存在，再透過 subprocess 模擬 OJ 的 stdin/stdout 環境。
        """
        # 若檔案不存在，提前告知明確的錯誤訊息。
        self.assertTrue(
            self.SOLUTION_FILE.exists(),
            f"找不到受測檔案：{self.SOLUTION_FILE}，請先建立 10056.py",
        )

        # subprocess.run 模擬 OJ 執行環境，捕捉 stdout 與 stderr。
        # check=False：不讓 subprocess 在 return code != 0 時自動拋出例外，
        #             改由下方 assertEqual 輸出更易讀的錯誤訊息。
        completed = subprocess.run(
            [sys.executable, str(self.SOLUTION_FILE)],
            input=input_data,
            text=True,
            capture_output=True,  # 同時捕捉 stdout 與 stderr，避免輸出混進終端機。
            check=False,
        )

        # 程式必須正常結束（return code = 0），非零代表程式崩潰。
        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "程式執行失敗。\n"
                f"return code: {completed.returncode}\n"
                f"stderr:\n{completed.stderr}"
            ),
        )

        # 去除空白行與前後空白，避免格式差異影響比對。
        return [line.strip() for line in completed.stdout.splitlines() if line.strip()]

    @staticmethod
    def oracle(n: int, p: float, i: int) -> float:
        """以數學公式計算第 i 個玩家的獲勝機率（參考正解）。

        推導過程詳見模組說明；此函式作為測試的「ground truth」。
        公式：P = q^(i-1) * p / (1 - q^N)，其中 q = 1 - p。

        特殊情況：
          - p = 1.0：第 1 個玩家必勝（機率 = 1），其他玩家機率 = 0。
          - p = 0.0：無人能獲勝（機率 = 0），題目保證此情況不出現。
        """
        q = 1.0 - p  # 單次失敗機率

        # p >= 1.0 時分母 1 - q^N = 1，直接判斷。
        if p >= 1.0:
            return 1.0 if i == 1 else 0.0

        # p = 0 時以防萬一返回 0（理論上題目不應有此輸入）。
        if p <= 0.0:
            return 0.0

        # 等比級數公式：q^(i-1) * p / (1 - q^N)
        return (q ** (i - 1)) * p / (1.0 - q ** n)

    @staticmethod
    def build_input(cases: list[tuple[int, float, int]]) -> str:
        """把測試案例清單組成題目要求的輸入格式字串。

        格式：
          第一行：測試組數 S
          接下來每行：「N p i」（p 格式化為 6 位小數，貼近 UVA 真實輸入）
        """
        # 第一行：總組數
        lines = [str(len(cases))]
        for n, p, i in cases:
            # p 格式化為 6 位小數，與 UVA 輸入格式一致（如 0.166667）。
            lines.append(f"{n} {p:.6f} {i}")
        return "\n".join(lines) + "\n"

    def assert_close(
        self,
        actual_lines: list[str],
        cases: list[tuple[int, float, int]],
        tol: float = 1e-4,
    ) -> None:
        """逐行比較浮點數輸出，允許 1e-4 的絕對誤差（對應 4 位小數精度）。

        先確認行數相符，再逐行解析浮點數並與 oracle 值比對。
        """
        # 輸出行數必須等於測試組數。
        self.assertEqual(
            len(actual_lines),
            len(cases),
            msg=f"輸出行數 {len(actual_lines)} 與預期組數 {len(cases)} 不符",
        )

        for idx, ((n, p, i), line) in enumerate(zip(cases, actual_lines)):
            expected_val = self.oracle(n, p, i)

            # 將輸出行解析為浮點數；解析失敗表示輸出格式不對。
            try:
                actual_val = float(line)
            except ValueError:
                self.fail(
                    f"第 {idx + 1} 行輸出無法解析為浮點數：{line!r}"
                )

            # 使用 assertAlmostEqual 的 delta 參數進行絕對誤差比較。
            self.assertAlmostEqual(
                actual_val,
                expected_val,
                delta=tol,
                msg=(
                    f"第 {idx + 1} 組（N={n}, p={p:.6f}, i={i}）："
                    f"輸出 {actual_val:.6f}，預期 {expected_val:.6f}"
                ),
            )

    # ------------------------------------------------------------------ #
    # 測試案例                                                             #
    # ------------------------------------------------------------------ #

    def test_basic_case(self) -> None:
        """固定案例：涵蓋不同玩家數、不同機率與不同指定玩家序號。

        以下幾組具代表性的情境：
          1. 三玩家 p=1/6，驗證玩家 1、2、3 的各自機率（三者合計應為 1）。
          2. 單一玩家（N=1），無論 p 為何，玩家 1 的機率必定為 1。
          3. 兩玩家 p=0.5，玩家 1 ≈ 0.6667，玩家 2 ≈ 0.3333。

        三玩家 p=1/6 推導：
          q = 5/6，q^3 = 125/216，分母 = 1 - 125/216 = 91/216
          玩家 1：(5/6)^0 * (1/6) / (91/216) = 36/91 ≈ 0.3956
          玩家 2：(5/6)^1 * (1/6) / (91/216) = 30/91 ≈ 0.3297
          玩家 3：(5/6)^2 * (1/6) / (91/216) = 25/91 ≈ 0.2747
          合計：36+30+25 = 91，91/91 = 1 ✓
        """
        cases: list[tuple[int, float, int]] = [
            # ── 三玩家、正常骰子（p ≈ 1/6） ──────────────────────────
            (3, 1.0 / 6.0, 1),   # 約 0.3956
            (3, 1.0 / 6.0, 2),   # 約 0.3297
            (3, 1.0 / 6.0, 3),   # 約 0.2747
            # ── 單一玩家，必勝 ─────────────────────────────────────────
            (1, 0.5,        1),   # 1.0000
            # ── 兩玩家、p=0.5 ────────────────────────────────────────
            (2, 0.5,        1),   # 約 0.6667
            (2, 0.5,        2),   # 約 0.3333
            # ── 高機率 p=0.9，玩家 1 幾乎必勝 ────────────────────────
            (5, 0.9,        1),   # 約 0.9901
            (5, 0.9,        2),   # 約 0.0990（遠小於玩家 1）
            # ── 低機率 p=0.1，後排玩家機率較低但差距不大 ─────────────
            (4, 0.1,        4),   # 約 0.2187
        ]

        input_data = self.build_input(cases)
        actual = self.run_solution(input_data)
        # 以 oracle 公式逐行驗證，允許 1e-4 絕對誤差（4 位小數精度）。
        self.assert_close(actual, cases)

    def test_random_cases(self) -> None:
        """隨機產生 50 組（N, p, i），以 oracle 公式全部比對。

        固定亂數種子 10056，確保每次測試產生相同的資料，便於重現比對。
        N 範圍：1 ～ 20；p 範圍：0.05 ～ 0.95 以避免極端值。
        """
        # 固定種子以確保可重現。
        random.seed(10056)

        cases: list[tuple[int, float, int]] = []
        for _ in range(50):
            n = random.randint(1, 20)               # 玩家數（1 ～ 20，涵蓋單玩家到多玩家）
            # p 限定在 0.05 ～ 0.95 避免 p→0 導致分母趨近 0 的數值不穩定，
            # round 到 6 位小數模擬 UVA 輸入的浮點精度。
            p = round(random.uniform(0.05, 0.95), 6)
            i = random.randint(1, n)                # 指定玩家序號（1 ≤ i ≤ N）
            cases.append((n, p, i))

        input_data = self.build_input(cases)
        actual = self.run_solution(input_data)
        # 與 oracle 逐行比對；允許 1e-4 絕對誤差。
        self.assert_close(actual, cases)


if __name__ == "__main__":
    # verbosity=2：輸出每個測試方法名稱與結果（ok / FAIL / ERROR），
    # 方便在終端機直接看到哪一個測試通過、哪一個失敗。
    unittest.main(verbosity=2)
