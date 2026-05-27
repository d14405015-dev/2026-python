"""
題目 11349 的簡化版本測試程式
直觀、易於維護的測試方式
"""

import unittest


def check_symmetric(matrix, n):
    """
    簡化的對稱矩陣檢查函式
    
    參數：
        matrix: n×n 的整數矩陣
        n: 矩陣的維度
    
    回傳：
        True 如果是對稱矩陣，False 否則
    """
    # 檢查 1：所有元素都必須非負
    for i in range(n):
        for j in range(n):
            if matrix[i][j] < 0:
                return False
    
    # 檢查 2：中心對稱
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[n - 1 - i][n - 1 - j]:
                return False
    
    return True


class TestSymmetricMatrixEasy(unittest.TestCase):
    """
    簡化版本的對稱矩陣測試
    """
    
    def test_example_1(self):
        """題目測試案例 1：應該是對稱矩陣"""
        m = [[5, 1, 3],
             [2, 0, 2],
             [3, 1, 5]]
        self.assertTrue(check_symmetric(m, 3))
    
    def test_example_2(self):
        """題目測試案例 2：應該不是對稱矩陣"""
        m = [[5, 1, 3],
             [2, 0, 2],
             [0, 1, 5]]  # 左下角不對稱
        self.assertFalse(check_symmetric(m, 3))
    
    def test_1x1(self):
        """最小矩陣：1×1"""
        m = [[7]]
        self.assertTrue(check_symmetric(m, 1))
    
    def test_2x2_symmetric(self):
        """2×2 對稱矩陣"""
        m = [[1, 2],
             [2, 1]]
        self.assertTrue(check_symmetric(m, 2))
    
    def test_2x2_not_symmetric(self):
        """2×2 非對稱矩陣"""
        m = [[1, 2],
             [3, 1]]
        self.assertFalse(check_symmetric(m, 2))
    
    def test_negative_number(self):
        """包含負數應該被拒絕"""
        m = [[-1, 0],
             [0, -1]]
        self.assertFalse(check_symmetric(m, 2))
    
    def test_all_zeros(self):
        """全零矩陣是對稱的"""
        m = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
        self.assertTrue(check_symmetric(m, 3))
    
    def test_identity_matrix(self):
        """單位矩陣是對稱的"""
        m = [[1, 0, 0],
             [0, 1, 0],
             [0, 0, 1]]
        self.assertTrue(check_symmetric(m, 3))
    
    def test_4x4_symmetric(self):
        """4×4 對稱矩陣"""
        m = [[1, 2, 3, 4],
             [5, 6, 7, 5],
             [5, 7, 6, 5],
             [4, 3, 2, 1]]
        self.assertTrue(check_symmetric(m, 4))
    
    def test_4x4_not_symmetric(self):
        """4×4 不對稱矩陣"""
        m = [[1, 2, 3, 4],
             [5, 6, 7, 5],
             [5, 7, 6, 5],
             [4, 3, 2, 2]]  # 右下角應該是 1
        self.assertFalse(check_symmetric(m, 4))


if __name__ == '__main__':
    unittest.main(verbosity=2)
