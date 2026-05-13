def solve(n: int) -> str:
    binary_str = bin(n)[2:]
    parity = bin(n).count('1')
    return f"The parity of {binary_str} is {parity} (mod 2)."


if __name__ == "__main__":
    while True:
        line = input().strip()
        n = int(line)
        if n == 0:
            break
        print(solve(n))
