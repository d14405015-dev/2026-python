"""
題目 11417 的 Unit-Test 程式：GCD 之和
測試 GCD 總和計算函式的各種情況
"""

import unittest
import math
from solution_11417 import calculate_gcd_sum


class TestGCDSum(unittest.TestCase):
    """
    測試 GCD 之和計算函式的測試類別
    """
    
    def test_case_n_2(self):
        """
        測試案例 1：N = 2（最小情況）
        期望結果：GCD(1,2) = 1
        """
        # 計算 GCD 之和
        result = calculate_gcd_sum(2)
        
        # 驗證結果
        # GCD(1,2) = 1
        self.assertEqual(result, 1)
    
    def test_case_n_3(self):
        """
        測試案例 2：N = 3
        期望結果：GCD(1,2) + GCD(1,3) + GCD(2,3) = 1 + 1 + 1 = 3
        """
        result = calculate_gcd_sum(3)
        # 1 + 1 + 1 = 3
        self.assertEqual(result, 3)
    
    def test_case_n_4(self):
        """
        測試案例 3：N = 4
        期望結果：
        GCD(1,2)=1 + GCD(1,3)=1 + GCD(1,4)=1 +
        GCD(2,3)=1 + GCD(2,4)=2 + GCD(3,4)=1 = 7
        """
        result = calculate_gcd_sum(4)
        # 1 + 1 + 1 + 1 + 2 + 1 = 7
        self.assertEqual(result, 7)
    
    def test_case_n_5(self):
        """
        測試案例 4：N = 5
        期望結果：計算所有 i<j ≤ 5 的 GCD 之和
        """
        result = calculate_gcd_sum(5)
        
        # 手工計算驗證：
        # i=1: GCD(1,2)=1, GCD(1,3)=1, GCD(1,4)=1, GCD(1,5)=1 → 4
        # i=2: GCD(2,3)=1, GCD(2,4)=2, GCD(2,5)=1 → 4
        # i=3: GCD(3,4)=1, GCD(3,5)=1 → 2
        # i=4: GCD(4,5)=1 → 1
        # 總和: 4 + 4 + 2 + 1 = 11
        self.assertEqual(result, 11)
    
    def test_case_n_6(self):
        """
        測試案例 5：N = 6
        期望結果：計算所有 i<j ≤ 6 的 GCD 之和
        """
        result = calculate_gcd_sum(6)
        
        # 驗證邏輯（不手工計算所有的）
        expected = 0
        for i in range(1, 6):
            for j in range(i + 1, 7):
                expected += math.gcd(i, j)
        
        self.assertEqual(result, expected)
    
    def test_case_n_10(self):
        """
        測試案例 6：N = 10（題目測試案例 1）
        期望結果：67
        """
        result = calculate_gcd_sum(10)
        
        # 題目提供的測試案例
        self.assertEqual(result, 67)
    
    def test_case_n_20(self):
        """
        測試案例 7：N = 20
        期望結果：計算驗證
        """
        result = calculate_gcd_sum(20)
        
        # 驗證用參考值計算
        expected = 0
        for i in range(1, 20):
            for j in range(i + 1, 21):
                expected += math.gcd(i, j)
        
        self.assertEqual(result, expected)
    
    def test_case_n_50(self):
        """
        測試案例 8：N = 50
        期望結果：計算驗證
        """
        result = calculate_gcd_sum(50)
        
        # 驗證用參考值計算
        expected = 0
        for i in range(1, 50):
            for j in range(i + 1, 51):
                expected += math.gcd(i, j)
        
        self.assertEqual(result, expected)
    
    def test_case_n_100(self):
        """
        測試案例 9：N = 100（題目測試案例 2）
        期望結果：13015
        """
        result = calculate_gcd_sum(100)
        
        # 題目提供的測試案例
        self.assertEqual(result, 13015)
    
    def test_case_n_500(self):
        """
        測試案例 10：N = 500（題目測試案例 3，最大值）
        期望結果：442011
        """
        result = calculate_gcd_sum(500)
        
        # 題目提供的測試案例（最大值）
        self.assertEqual(result, 442011)
    
    def test_gcd_relationship(self):
        """
        測試案例 11：驗證 GCD 的對稱性
        期望結果：GCD(a,b) = GCD(b,a)
        """
        # 驗證：GCD 應該滿足對稱性
        self.assertEqual(math.gcd(12, 8), math.gcd(8, 12))
        self.assertEqual(math.gcd(15, 25), math.gcd(25, 15))
        
        # 驗證：互質數字的 GCD
        self.assertEqual(math.gcd(7, 11), 1)
        self.assertEqual(math.gcd(13, 17), 1)
    
    def test_consecutive_numbers_gcd(self):
        """
        測試案例 12：連續整數的 GCD
        期望結果：相鄰整數的 GCD 總是 1
        """
        # 連續整數的 GCD 應該是 1
        for i in range(1, 20):
            self.assertEqual(math.gcd(i, i + 1), 1)
    
    def test_multiple_relation_gcd(self):
        """
        測試案例 13：整數倍數的 GCD
        期望結果：倍數關係的 GCD 應該是較小的數
        """
        # 如果 b = k*a，則 GCD(a,b) = a
        self.assertEqual(math.gcd(5, 10), 5)      # 10 = 2*5
        self.assertEqual(math.gcd(7, 14), 7)      # 14 = 2*7
        self.assertEqual(math.gcd(3, 12), 3)      # 12 = 4*3
    
    def test_prime_numbers_gcd(self):
        """
        測試案例 14：質數之間的 GCD
        期望結果：不同質數的 GCD 應該是 1
        """
        # 不同質數的 GCD 總是 1
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        for i in range(len(primes)):
            for j in range(i + 1, len(primes)):
                self.assertEqual(math.gcd(primes[i], primes[j]), 1)
    
    def test_same_number_gcd(self):
        """
        測試案例 15：相同數字的 GCD
        期望結果：GCD(n,n) 應該等於 n
        """
        # 相同數字的 GCD 應該是該數字本身
        self.assertEqual(math.gcd(5, 5), 5)
        self.assertEqual(math.gcd(12, 12), 12)
        self.assertEqual(math.gcd(100, 100), 100)
    
    def test_incremental_calculation(self):
        """
        測試案例 16：逐步增加 N 值的 GCD 之和
        期望結果：N 較大時，GCD 之和應該逐漸增加
        """
        # 驗證 GCD 之和隨著 N 增加而遞增
        result_2 = calculate_gcd_sum(2)
        result_3 = calculate_gcd_sum(3)
        result_4 = calculate_gcd_sum(4)
        result_5 = calculate_gcd_sum(5)
        
        # 確認單調遞增性質
        self.assertLess(result_2, result_3)
        self.assertLess(result_3, result_4)
        self.assertLess(result_4, result_5)
    
    def test_performance_n_100(self):
        """
        測試案例 17：效能測試
        期望結果：N=100 應該在合理時間內完成
        """
        # 測試 N=100 的執行效率
        import time
        
        start_time = time.time()
        result = calculate_gcd_sum(100)
        end_time = time.time()
        
        # 確認結果正確
        self.assertEqual(result, 13015)
        
        # 確認執行時間合理（應該在 1 秒以內）
        execution_time = end_time - start_time
        self.assertLess(execution_time, 1.0)


if __name__ == '__main__':
    # 執行所有測試
    unittest.main(verbosity=2)
