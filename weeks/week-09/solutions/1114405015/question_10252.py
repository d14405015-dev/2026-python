def parse_input(data):
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if not lines:
        return []

    t = int(lines[0])
    idx = 1
    cases = []

    for _ in range(t):
        n = int(lines[idx])
        idx += 1

        points = []
        for _ in range(n):
            x, y = map(int, lines[idx].split())
            idx += 1
            points.append((x, y))

        cases.append(points)

    return cases


def one_dim_opt(values):
    arr = sorted(values)
    n = len(arr)

    if n % 2 == 1:
        med = arr[n // 2]
        best_sum = sum(abs(v - med) for v in arr)
        return best_sum, 1

    left = arr[n // 2 - 1]
    right = arr[n // 2]

    best_sum = sum(abs(v - left) for v in arr)
    count = right - left + 1
    return best_sum, count


def solve_case(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]

    sx, cx = one_dim_opt(xs)
    sy, cy = one_dim_opt(ys)

    min_sum = sx + sy
    count = cx * cy
    return min_sum, count


def solve(data):
    cases = parse_input(data)
    out_lines = []

    for points in cases:
        min_sum, count = solve_case(points)
        out_lines.append(f"{min_sum} {count}")

    return "\n".join(out_lines)


def main():
    import sys

    data = sys.stdin.read()
    out = solve(data)
    if out:
        print(out)


if __name__ == "__main__":
    main()
