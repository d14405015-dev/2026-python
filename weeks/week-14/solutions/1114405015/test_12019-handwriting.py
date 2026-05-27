import subprocess
import sys


def run_handwriting_solution(input_data):
    process = subprocess.Popen(
        [sys.executable, "solution_12019-handwriting.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input=input_data)
    return stdout, stderr


def test_reference_block():
    input_data = """12
1 10
2 21
3 7
4 4
5 9
6 6
7 11
8 8
9 5
10 10
11 7
12 12
"""
    expected = """Tuesday
Tuesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
Wednesday
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 1: reference block")


def test_year_start():
    input_data = """1
1 1
"""
    expected = """Sunday
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 2: year start")


def test_leap_day():
    input_data = """1
2 29
"""
    expected = """Wednesday
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 3: leap day")


def test_year_end():
    input_data = """1
12 31
"""
    expected = """Monday
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 4: year end")


def test_various_dates():
    input_data = """5
3 14
4 1
6 30
10 31
11 30
"""
    expected = """Wednesday
Sunday
Saturday
Wednesday
Friday
"""
    stdout, stderr = run_handwriting_solution(input_data)
    assert stdout == expected, f"Expected:\n{expected}\nGot:\n{stdout}\nErr:\n{stderr}"
    print("[PASS] Test case 5: various dates")


if __name__ == "__main__":
    print("=" * 60)
    print("hand-written solution test started")
    print("=" * 60)

    try:
        test_reference_block()
        test_year_start()
        test_leap_day()
        test_year_end()
        test_various_dates()

        print("\n" + "=" * 60)
        print("[PASS] All 5 test cases passed!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
