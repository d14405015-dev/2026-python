from typing import List


def parse_cases(input_data: str):
    
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    idx = 0
    cases = []

    while idx < len(lines):
        n = int(lines[idx])
        idx += 1

        forbidden = []
        for _ in range(n):
            nums = list(map(int, lines[idx].split()))
            idx += 1

            positions = []
            for x in nums:
                if x == 0:
                    break
                positions.append(x)
            forbidden.append(set(positions))

        cases.append((n, forbidden))

    return cases


def solve_one_case(n: int, forbidden: List[set]) -> List[str]:

    people = [chr(ord("A") + i) for i in range(n)]
    used = [False] * n
    current = [""] * n

    output_lines: List[str] = []
    prev_perm: List[str] | None = None

    def emit(curr_perm: List[str]):
        
        nonlocal prev_perm

        if prev_perm is None:
            output_lines.append("".join(curr_perm))
            prev_perm = curr_perm[:]
            return

        pivot = 0
        while pivot < n and prev_perm[pivot] == curr_perm[pivot]:
            pivot += 1

        output_lines.append("".join(curr_perm[pivot:]))
        prev_perm = curr_perm[:]

    def dfs(pos: int):

        if pos == n:
            emit(current)
            return

        one_based_pos = pos + 1

        for person_idx in range(n):
            if used[person_idx]:
                continue
            if one_based_pos in forbidden[person_idx]:
                continue

            used[person_idx] = True
            current[pos] = people[person_idx]
            dfs(pos + 1)
            used[person_idx] = False

    dfs(0)
    return output_lines


def solve(input_data: str) -> str:

    cases = parse_cases(input_data)
    all_chunks = []

    for n, forbidden in cases:
        lines = solve_one_case(n, forbidden)
        all_chunks.append("\n".join(lines))

    return "\n".join(all_chunks).rstrip()


def main():
    import sys

    input_data = sys.stdin.read()
    result = solve(input_data)
    if result:
        print(result)


if __name__ == "__main__":
    main()
