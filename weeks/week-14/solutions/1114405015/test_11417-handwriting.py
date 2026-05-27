import subprocess
import sys
import math


def run_handwriting_solution(input_data):
    """
    執行手打程式並返回輸出結果
    """
    process = subprocess.Popen(
        [sys.executable, 'solution_11417-handwriting.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_data)
    return stdout, stderr


def test_case_1():
    """測試案例1：題目提供的測試資料 N=10"""
    input_data = """10
0
"""
    expected = """67
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 1: N=10, expected 67")


def test_case_2():
    """測試案例2：題目提供的測試資料 N=100"""
    input_data = """100
0
"""
    expected = """13015
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 2: N=100, expected 13015")


def test_case_3():
    """測試案例3：題目提供的測試資料 N=500"""
    input_data = """500
0
"""
    expected = """442011
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 3: N=500, expected 442011")


def test_n_2():
    """測試案例4：N=2（最小情況）"""
    input_data = """2
0
"""
    expected = """1
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 4: N=2, expected 1")


def test_n_3():
    """測試案例5：N=3"""
    input_data = """3
0
"""
    expected = """3
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 5: N=3, expected 3")


def test_n_4():
    """測試案例6：N=4"""
    input_data = """4
0
"""
    expected = """7
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 6: N=4, expected 7")


def test_n_5():
    """測試案例7：N=5"""
    input_data = """5
0
"""
    expected = """11
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 7: N=5, expected 11")


def test_n_20():
    """測試案例8：N=20"""
    input_data = """20
0
"""
    expected_val = 0
    for i in range(1, 20):
        for j in range(i + 1, 21):
            expected_val += math.gcd(i, j)
    expected = f"{expected_val}\n"
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 8: N=20")


def test_n_50():
    """測試案例9：N=50"""
    input_data = """50
0
"""
    expected_val = 0
    for i in range(1, 50):
        for j in range(i + 1, 51):
            expected_val += math.gcd(i, j)
    expected = f"{expected_val}\n"
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 9: N=50")


def test_multiple_inputs():
    """測試案例10：多組輸入"""
    input_data = """2
3
4
0
"""
    expected = """1
3
7
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}"
    print("[PASS] Test case 10: Multiple inputs")


if __name__ == '__main__':
    print("=" * 60)
    print("hand-written solution test started")
    print("=" * 60)
    
    try:
        test_case_1()
        test_case_2()
        test_case_3()
        test_n_2()
        test_n_3()
        test_n_4()
        test_n_5()
        test_n_20()
        test_n_50()
        test_multiple_inputs()
        
        print("\n" + "=" * 60)
        print("[PASS] All 10 test cases passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
