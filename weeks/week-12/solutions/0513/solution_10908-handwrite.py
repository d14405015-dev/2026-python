import sys

def solve_query(grid, r, c):
    m = len(grid)
    n = len(grid[0])
    ch = grid[r][c]
    h = 0
    while True:
        nh = h + 1
        if r - nh < 0 or r + nh >= m or c - nh < 0 or c + nh >= n:
            break
        ok = True
        for dr in range(-nh, nh + 1):
            for dc in range(-nh, nh + 1):
                if grid[r + dr][c + dc] != ch:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            break
        h = nh
    return 2 * h + 1

def main():
    data = sys.stdin.read().split("\n")
    i = 0
    t = int(data[i]); i += 1
    for _ in range(t):
        m, n, q = map(int, data[i].split()); i += 1
        grid = []
        for _ in range(m):
            grid.append(data[i]); i += 1
        print(f"{m} {n} {q}")
        for _ in range(q):
            r, c = map(int, data[i].split()); i += 1
            print(solve_query(grid, r, c))

if __name__ == "__main__":
    main()
