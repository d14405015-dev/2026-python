import subprocess
import sys
import math


def run_handwriting_solution(input_data):
    process = subprocess.Popen(
        [sys.executable, "solution_11461-handwriting.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input=input_data)
    return stdout, stderr


def count_square_numbers(a, b):
    right = math.isqrt(b)
    left = math.isqrt(a - 1) + 1
    if right < left:
        return 0
    return right - left + 1


def test_sample_case_1():
    input_data = """1 4
0 0
"""
    expected = """2
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 1: [1,4] -> 2")


def test_sample_case_2():
    input_data = """1 10
0 0
"""
    expected = """3
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 2: [1,10] -> 3")


def test_sample_case_3():
    input_data = """1 100000
0 0
"""
    expected = """316
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 3: [1,100000] -> 316")


def test_single_square():
    input_data = """49 49
0 0
"""
    expected = """1
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 4: [49,49] -> 1")


def test_single_non_square():
    input_data = """50 50
0 0
"""
    expected = """0
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 5: [50,50] -> 0")


def test_no_square_range():
    input_data = """2 3
0 0
"""
    expected = """0
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 6: [2,3] -> 0")


def test_middle_range():
    input_data = """10 100
0 0
"""
    expected = """7
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 7: [10,100] -> 7")


def test_upper_boundary_close():
    input_data = """99856 100000
0 0
"""
    expected = """1
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 8: [99856,100000] -> 1")


def test_upper_boundary_no_square():
    input_data = """99900 100000
0 0
"""
    expected = """0
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 9: [99900,100000] -> 0")


def test_multiple_inputs():
    input_data = """1 4
1 10
1 100000
0 0
"""
    expected = """2
3
316
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 10: multiple input lines")


def test_random_checks_with_formula():
    pairs = [(1, 1), (15, 35), (36, 49), (400, 500), (50000, 60000)]
    lines = [f"{a} {b}" for a, b in pairs]
    input_data = "\n".join(lines) + "\n0 0\n"

    expected_lines = [str(count_square_numbers(a, b)) for a, b in pairs]
    expected = "\n".join(expected_lines) + "\n"

    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 11: formula cross-check")


if __name__ == "__main__":
    print("=" * 60)
    print("hand-written solution test started")
    print("=" * 60)

    try:
        test_sample_case_1()
        test_sample_case_2()
        test_sample_case_3()
        test_single_square()
        test_single_non_square()
        test_no_square_range()
        test_middle_range()
        test_upper_boundary_close()
        test_upper_boundary_no_square()
        test_multiple_inputs()
        test_random_checks_with_formula()

        print("\n" + "=" * 60)
        print("[PASS] All 11 test cases passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
