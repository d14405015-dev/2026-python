from typing import Dict


def build_decode_map() -> Dict[str, str]:
    """
    建立解碼對照表。

    題意可視為：打字時手向右偏，
    因此看到的字元要往鍵盤左側回推，
    才是原本想打的字。

    本作業測試採用的規則為「回推 2 個鍵」，
    並且題述示例 r -> e 亦符合此規則。
    """
    rows = [
        "`1234567890-=",
        "qwertyuiop[]\\",
        "asdfghjkl;'",
        "zxcvbnm,./",
    ]

    mp: Dict[str, str] = {}
    for row in rows:
        for i in range(2, len(row)):
            mp[row[i]] = row[i - 2]
    return mp


def solve(input_data: str) -> str:
    """
    將整段輸入逐字解碼。

    規則：
    1. 在映射表中的字元，轉成對應左移字元。
    2. 不在映射中的字元（例如空白、驚嘆號）保持原樣。
    3. 換行保留，確保多行輸入可逐行輸出。
    """
    decode_map = build_decode_map()
    out = []

    for ch in input_data:
        lower = ch.lower()
        if lower in decode_map:
            out.append(decode_map[lower])
        else:
            out.append(ch)

    return "".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()), end="")


if __name__ == "__main__":
    main()
