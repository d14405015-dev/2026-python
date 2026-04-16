import sys


def main():
    data = sys.stdin.read().splitlines()
    if not data:
        return

    n = int(data[0])
    lines = data[1:n + 1]

    # Count letters case-insensitively.
    counts = {}
    for line in lines:
        for ch in line:
            if ch.isalpha():
                letter = ch.upper()
                counts[letter] = counts.get(letter, 0) + 1

    # Sort by frequency descending, then alphabet ascending.
    ordered = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    for letter, freq in ordered:
        print(f"{letter} {freq}")


if __name__ == "__main__":
    main()
