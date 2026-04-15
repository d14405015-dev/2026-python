def solve(input_data: str) -> str:
    row1 = "`1234567890-="
    row2 = "qwertyuiop[]\\"
    row3 = "asdfghjkl;'"
    row4 = "zxcvbnm,./"
    rows = [row1, row2, row3, row4]

    trans = {}
    for row in rows:
        for i in range(2, len(row)):
            trans[row[i]] = row[i - 2]

    out = []
    for ch in input_data:
        c = ch.lower()
        if c in trans:
            out.append(trans[c])
        else:
            out.append(ch)

    return "".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()), end="")


if __name__ == "__main__":
    main()
