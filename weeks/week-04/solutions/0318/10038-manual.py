import sys


def is_jolly(sequence):
    n = len(sequence)
    if n <= 1:
        return True

    seen = set()

    for i in range(1, n):
        diff = abs(sequence[i] - sequence[i - 1])
        if diff < 1 or diff > n - 1 or diff in seen:
            return False
        seen.add(diff)

    return len(seen) == n - 1


def main():
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue

        nums = list(map(int, line.split()))
        n = nums[0]
        seq = nums[1:1 + n]

        if len(seq) != n:
            print("Not jolly")
            continue

        print("Jolly" if is_jolly(seq) else "Not jolly")


if __name__ == "__main__":
    main()
