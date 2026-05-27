"""
題目 11349 的 Unit-Test 程式：對稱矩陣檢查
測試對稱矩陣判定函式的各種情況
"""

import unittest
from solution_11349 import check_symmetric_matrix


class TestSymmetricMatrix(unittest.TestCase):
    """
    測試對稱矩陣檢查函式的測試類別
    """
    
    def test_case_1_symmetric_3x3(self):
        """
        測試案例 1：3×3 對稱矩陣
        期望結果：應該判定為對稱矩陣
        """
        # 建立測試矩陣
        matrix = [
            [5, 1, 3],
            [2, 0, 2],
            [3, 1, 5]
        ]
        # 判定為對稱
        self.assertTrue(check_symmetric_matrix(matrix, 3))
    
    def test_case_2_non_symmetric_3x3(self):
        """
        測試案例 2：3×3 非對稱矩陣
        期望結果：應該判定為非對稱矩陣
        """
        # 建立測試矩陣（M[0][2] ≠ M[2][0]）
        matrix = [
            [5, 1, 3],
            [2, 0, 2],
            [0, 1, 5]  # 右下角與左上角不對稱
        ]
        # 判定為非對稱
        self.assertFalse(check_symmetric_matrix(matrix, 3))
    
    def test_1x1_symmetric(self):
        """
        測試案例 3：1×1 對稱矩陣
        期望結果：應該判定為對稱矩陣
        單一元素的矩陣總是對稱的（如果元素非負）
        """
        matrix = [[5]]
        self.assertTrue(check_symmetric_matrix(matrix, 1))
    
    def test_2x2_symmetric(self):
        """
        測試案例 4：2×2 對稱矩陣
        期望結果：應該判定為對稱矩陣
        
        矩陣結構：
        [a b]
        [b a]
        
        中心對稱檢查：M[0][0]=M[1][1]、M[0][1]=M[1][0]
        """
        matrix = [
            [1, 2],
            [2, 1]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 2))
    
    def test_2x2_non_symmetric(self):
        """
        測試案例 5：2×2 非對稱矩陣
        期望結果：應該判定為非對稱矩陣
        """
        matrix = [
            [1, 2],
            [3, 1]
        ]
        self.assertFalse(check_symmetric_matrix(matrix, 2))
    
    def test_negative_values(self):
        """
        測試案例 6：含有負值的矩陣
        期望結果：應該判定為非對稱（因為包含負數）
        對稱矩陣要求所有元素都非負
        """
        matrix = [
            [-1, 0],
            [0, -1]
        ]
        self.assertFalse(check_symmetric_matrix(matrix, 2))
    
    def test_4x4_symmetric(self):
        """
        測試案例 7：4×4 對稱矩陣
        期望結果：應該判定為對稱矩陣
        
        矩陣中心對稱示例：
        [1 2 3 4]
        [5 6 7 5]
        [5 7 6 5]
        [4 3 2 1]
        """
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 5],
            [5, 7, 6, 5],
            [4, 3, 2, 1]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 4))
    
    def test_4x4_non_symmetric(self):
        """
        測試案例 8：4×4 非對稱矩陣
        期望結果：應該判定為非對稱矩陣
        """
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 5],
            [5, 7, 6, 5],
            [4, 3, 2, 2]  # 右下角應該是 1，不是 2
        ]
        self.assertFalse(check_symmetric_matrix(matrix, 4))
    
    def test_all_zeros(self):
        """
        測試案例 9：全零矩陣
        期望結果：應該判定為對稱矩陣
        零矩陣總是對稱的
        """
        matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 3))
    
    def test_identity_matrix(self):
        """
        測試案例 10：單位矩陣
        期望結果：應該判定為對稱矩陣
        單位矩陣中心對稱且所有元素非負
        
        [1 0 0]
        [0 1 0]
        [0 0 1]
        """
        matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 3))
    
    def test_large_numbers(self):
        """
        測試案例 11：大數值矩陣
        期望結果：應該能正確處理大數值（範圍在 -2³² 到 2³²）
        """
        # 使用接近 2³² 的大數值
        large_num = 2147483647  # 2³² - 1
        matrix = [
            [large_num, 0],
            [0, large_num]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 2))
    
    def test_3x3_asymmetric_center(self):
        """
        測試案例 12：3×3 矩陣，中心元素不相同
        期望結果：應該判定為非對稱矩陣
        3×3 矩陣的中心元素 M[1][1] 需要等於自己（這總是成立）
        但其他位置可能不對稱
        """
        matrix = [
            [1, 2, 3],
            [2, 5, 2],
            [4, 2, 1]  # M[0][0]=1 ≠ M[2][2]=1，但 M[0][2]=3 ≠ M[2][0]=4
        ]
        self.assertFalse(check_symmetric_matrix(matrix, 3))
    
    def test_boundary_value_zero(self):
        """
        測試案例 13：邊界值測試：零值
        期望結果：應該正確判定
        零是有效的非負數
        """
        matrix = [
            [0, 1],
            [1, 0]
        ]
        self.assertTrue(check_symmetric_matrix(matrix, 2))


if __name__ == '__main__':
    # 執行所有測試
    unittest.main(verbosity=2)
