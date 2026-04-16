import sys


def process_line(line: str) -> int:
    a_str, b_str = line.split()
    a = int(a_str)
    b = int(b_str)
    return abs(a - b)


def main() -> None:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        print(process_line(line))


if __name__ == "__main__":
    main()
