import sys


def carry_count(a: int, b: int) -> int:
    carry = 0
    total = 0

    while a > 0 or b > 0:
        digit_sum = (a % 10) + (b % 10) + carry
        if digit_sum >= 10:
            carry = 1
            total += 1
        else:
            carry = 0

        a //= 10
        b //= 10

    return total


def to_sentence(k: int) -> str:
    if k == 0:
        return "No carry operation."
    if k == 1:
        return "1 carry operation."
    return f"{k} carry operations."


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        a, b = map(int, line.split())
        if a == 0 and b == 0:
            break

        print(to_sentence(carry_count(a, b)))


if __name__ == "__main__":
    main()
