# -easy 版本：
# 只記一件事：
# 「看到的字元，回推鍵盤左邊 2 格」。


def solve(input_data: str) -> str:
    row1 = "`1234567890-="
    row2 = "qwertyuiop[]\\"
    row3 = "asdfghjkl;'"
    row4 = "zxcvbnm,./"
    rows = [row1, row2, row3, row4]

    # 建立映射：右邊字 -> 左邊 2 格字
    trans = {}
    for row in rows:
        for i in range(2, len(row)):
            trans[row[i]] = row[i - 2]

    ans = []
    for ch in input_data:
        c = ch.lower()
        if c in trans:
            ans.append(trans[c])
        else:
            # 空白、換行、未定義符號都保留原樣
            ans.append(ch)

    return "".join(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()), end="")


if __name__ == "__main__":
    main()
