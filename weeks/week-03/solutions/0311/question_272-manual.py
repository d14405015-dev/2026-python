"""UVA 272 manual version.

Hand-typed style implementation:
- English-only comments
- Minimal and easy to type
"""

from __future__ import annotations

import sys


def main() -> None:
    data = sys.stdin.read()

    out: list[str] = []
    open_quote = True

    for ch in data:
        if ch == '"':
            if open_quote:
                out.append("``")
            else:
                out.append("''")
            open_quote = not open_quote
        else:
            out.append(ch)

    print("".join(out), end="")


if __name__ == "__main__":
    main()
