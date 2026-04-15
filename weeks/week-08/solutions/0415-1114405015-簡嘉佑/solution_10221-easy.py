import math


# -easy 版本：
# 口訣三步驟
# 1) 角度統一轉成 degree，且若 >180 就改成 360-angle
# 2) theta = radians(angle)
# 3) arc = r*theta, chord = 2*r*sin(theta/2)


def solve(input_data: str) -> str:
    rows = [line.strip() for line in input_data.splitlines() if line.strip()]
    ans = []

    for row in rows:
        s_str, a_str, unit = row.split()
        s = float(s_str)
        angle = float(a_str)

        r = 6440.0 + s

        # min -> degree
        if unit == "min":
            angle = angle / 60.0

        # Use smaller central angle
        if angle > 180.0:
            angle = 360.0 - angle

        theta = math.radians(angle)

        arc = r * theta
        chord = 2.0 * r * math.sin(theta / 2.0)

        ans.append(f"{arc:.6f} {chord:.6f}")

    return "\n".join(ans)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
