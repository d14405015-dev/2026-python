import sys


class FenwickTree:
    def __init__(self, size):
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index, delta):
        while index <= self.size:
            self.tree[index] += delta
            index += index & -index

    def find_kth(self, kth):
        # Find the kth available number in the current set.
        index = 0
        prefix = 0
        bit = 1

        while bit < self.size:
            bit <<= 1

        while bit > 0:
            next_index = index + bit
            if next_index <= self.size and prefix + self.tree[next_index] < kth:
                index = next_index
                prefix += self.tree[next_index]
            bit >>= 1

        return index + 1


def solve(data):
    values = data.split()
    if not values:
        return ""

    cow_count = int(values[0])
    smaller_before = [0] * (cow_count + 1)

    for position in range(2, cow_count + 1):
        smaller_before[position] = int(values[position - 1])

    available = FenwickTree(cow_count)
    for label in range(1, cow_count + 1):
        available.add(label, 1)

    answer = [0] * (cow_count + 1)

    for position in range(cow_count, 0, -1):
        kth = smaller_before[position] + 1
        answer[position] = available.find_kth(kth)
        available.add(answer[position], -1)

    return "\n".join(str(number) for number in answer[1:]) + "\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()