import math


def solve(input_data: str) -> str:
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    out = []

    for line in lines:
        s_str, a_str, unit = line.split()
        s = float(s_str)
        a = float(a_str)

        r = 6440.0 + s

        if unit == "min":
            a = a / 60.0

        if a > 180.0:
            a = 360.0 - a

        theta = math.radians(a)
        arc = r * theta
        chord = 2.0 * r * math.sin(theta / 2.0)

        out.append(f"{arc:.6f} {chord:.6f}")

    return "\n".join(out)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
