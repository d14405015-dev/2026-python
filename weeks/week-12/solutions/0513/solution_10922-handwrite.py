def solve(n_str: str) -> str:
    current = n_str
    depth = 0
    while len(current) > 1:
        s = sum(int(ch) for ch in current)
        current = str(s)
        depth += 1
    if current == "9":
        return f"9-degree of {n_str} is {depth}."
    else:
        return f"{n_str} is not a multiple of 9."


if __name__ == "__main__":
    while True:
        line = input().strip()
        if line == "0":
            break
        print(solve(line))
