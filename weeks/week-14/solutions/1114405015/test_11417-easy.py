"""
題目 11417 簡化版本的測試程式
直觀、易於維護的測試方式
"""

import unittest
import math


def calculate_gcd_sum(n):
    """
    簡化的 GCD 之和計算函式
    
    參數：
        n: 正整數 N（2 ≤ N ≤ 500）
    
    回傳：
        所有 GCD 的總和
    """
    # 初始化總和為 0
    total = 0
    
    # 計算所有 i < j ≤ n 的 GCD 之和
    for i in range(1, n):
        for j in range(i + 1, n + 1):
            total += math.gcd(i, j)
    
    return total


class TestGCDSumEasy(unittest.TestCase):
    """
    簡化版本的 GCD 之和測試
    """
    
    def test_n_2(self):
        """
        測試案例 1：N = 2（最小情況）
        期望結果：GCD(1,2) = 1
        """
        result = calculate_gcd_sum(2)
        self.assertEqual(result, 1)
    
    def test_n_3(self):
        """
        測試案例 2：N = 3
        期望結果：GCD(1,2) + GCD(1,3) + GCD(2,3) = 1 + 1 + 1 = 3
        """
        result = calculate_gcd_sum(3)
        self.assertEqual(result, 3)
    
    def test_n_4(self):
        """
        測試案例 3：N = 4
        期望結果：1 + 1 + 1 + 1 + 2 + 1 = 7
        """
        result = calculate_gcd_sum(4)
        self.assertEqual(result, 7)
    
    def test_n_5(self):
        """
        測試案例 4：N = 5
        期望結果：計算所有 i < j ≤ 5 的 GCD 之和 = 11
        """
        result = calculate_gcd_sum(5)
        self.assertEqual(result, 11)
    
    def test_n_10(self):
        """
        測試案例 5：N = 10（題目測試案例 1）
        期望結果：67
        """
        result = calculate_gcd_sum(10)
        self.assertEqual(result, 67)
    
    def test_n_20(self):
        """
        測試案例 6：N = 20
        期望結果：驗證邏輯正確性
        """
        result = calculate_gcd_sum(20)
        
        # 使用參考計算驗證
        expected = 0
        for i in range(1, 20):
            for j in range(i + 1, 21):
                expected += math.gcd(i, j)
        
        self.assertEqual(result, expected)
    
    def test_n_50(self):
        """
        測試案例 7：N = 50
        期望結果：驗證邏輯正確性
        """
        result = calculate_gcd_sum(50)
        
        # 使用參考計算驗證
        expected = 0
        for i in range(1, 50):
            for j in range(i + 1, 51):
                expected += math.gcd(i, j)
        
        self.assertEqual(result, expected)
    
    def test_n_100(self):
        """
        測試案例 8：N = 100（題目測試案例 2）
        期望結果：13015
        """
        result = calculate_gcd_sum(100)
        self.assertEqual(result, 13015)
    
    def test_n_500(self):
        """
        測試案例 9：N = 500（題目測試案例 3，最大值）
        期望結果：442011
        """
        result = calculate_gcd_sum(500)
        self.assertEqual(result, 442011)
    
    def test_consecutive_gcd_is_one(self):
        """
        測試案例 10：連續整數的 GCD 應該是 1
        期望結果：GCD(n, n+1) = 1
        """
        # 連續整數的 GCD 總是 1
        for i in range(1, 20):
            self.assertEqual(math.gcd(i, i + 1), 1)
    
    def test_multiple_gcd(self):
        """
        測試案例 11：倍數關係的 GCD
        期望結果：GCD(a, k*a) = a
        """
        # 倍數關係的 GCD 應該是較小的數
        self.assertEqual(math.gcd(5, 10), 5)
        self.assertEqual(math.gcd(7, 14), 7)
        self.assertEqual(math.gcd(3, 12), 3)
    
    def test_incremental_growth(self):
        """
        測試案例 12：GCD 之和應隨著 N 增加而遞增
        期望結果：N 越大，GCD 之和越大
        """
        result_2 = calculate_gcd_sum(2)
        result_3 = calculate_gcd_sum(3)
        result_4 = calculate_gcd_sum(4)
        result_5 = calculate_gcd_sum(5)
        
        # 驗證單調遞增
        self.assertLess(result_2, result_3)
        self.assertLess(result_3, result_4)
        self.assertLess(result_4, result_5)


if __name__ == '__main__':
    # 執行所有測試
    unittest.main(verbosity=2)
