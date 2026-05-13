import sys

def solve(s, d):
    if (s + d) % 2 != 0:
        return "impossible"
    big = (s + d) // 2
    small = (s - d) // 2
    if small < 0:
        return "impossible"
    return f"{big} {small}"

def main():
    data = sys.stdin.read().split()
    i = 0
    n = int(data[i]); i += 1
    for _ in range(n):
        s = int(data[i]); i += 1
        d = int(data[i]); i += 1
        print(solve(s, d))

if __name__ == "__main__":
    main()
