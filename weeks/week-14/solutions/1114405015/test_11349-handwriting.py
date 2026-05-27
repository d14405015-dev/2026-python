import subprocess
import sys

def run_handwriting_solution(input_data):
    """
    執行手打程式並返回輸出結果
    """
    process = subprocess.Popen(
        [sys.executable, 'solution_11349-handwriting.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_data)
    return stdout, stderr


def test_case_1():
    """測試案例1：題目提供的測試資料"""
    input_data = """2
N = 3
5 1 3
2 0 2
3 1 5
N = 3
5 1 3
2 0 2
0 1 5
"""
    expected = """Test #1: Symmetric.
Test #2: Non-symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 1: Topic test data")


def test_1x1_matrix():
    """測試案例2：1×1 矩陣"""
    input_data = """1
N = 1
5
"""
    expected = """Test #1: Symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 2: 1x1 matrix")


def test_2x2_symmetric():
    """測試案例3：2×2 對稱矩陣"""
    input_data = """1
N = 2
1 2
2 1
"""
    expected = """Test #1: Symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 3: 2x2 symmetric matrix")


def test_2x2_non_symmetric():
    """測試案例4：2×2 非對稱矩陣"""
    input_data = """1
N = 2
1 2
3 1
"""
    expected = """Test #1: Non-symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 4: 2x2 non-symmetric matrix")


def test_with_negative():
    """測試案例5：包含負數"""
    input_data = """1
N = 2
-1 0
0 -1
"""
    expected = """Test #1: Non-symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 5: Contains negative numbers")


def test_all_zeros():
    """測試案例6：全零矩陣"""
    input_data = """1
N = 3
0 0 0
0 0 0
0 0 0
"""
    expected = """Test #1: Symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 6: All zeros matrix")


def test_identity_matrix():
    """測試案例7：單位矩陣"""
    input_data = """1
N = 3
1 0 0
0 1 0
0 0 1
"""
    expected = """Test #1: Symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 7: Identity matrix")


def test_4x4_symmetric():
    """測試案例8：4×4 對稱矩陣"""
    input_data = """1
N = 4
1 2 3 4
5 6 7 5
5 7 6 5
4 3 2 1
"""
    expected = """Test #1: Symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 8: 4x4 symmetric matrix")


def test_4x4_non_symmetric():
    """測試案例9：4×4 非對稱矩陣"""
    input_data = """1
N = 4
1 2 3 4
5 6 7 5
5 7 6 5
4 3 2 9
"""
    expected = """Test #1: Non-symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 9: 4x4 non-symmetric matrix")


def test_multiple_tests():
    """測試案例10：多組測試資料"""
    input_data = """3
N = 1
7
N = 2
9 0
0 9
N = 2
1 2
3 4
"""
    expected = """Test #1: Symmetric.
Test #2: Symmetric.
Test #3: Non-symmetric.
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 10: Multiple test data")


if __name__ == '__main__':
    print("=" * 60)
    print("hand-written solution test started")
    print("=" * 60)
    
    try:
        test_case_1()
        test_1x1_matrix()
        test_2x2_symmetric()
        test_2x2_non_symmetric()
        test_with_negative()
        test_all_zeros()
        test_identity_matrix()
        test_4x4_symmetric()
        test_4x4_non_symmetric()
        test_multiple_tests()
        
        print("\n" + "=" * 60)
        print("[PASS] All 10 test cases passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
