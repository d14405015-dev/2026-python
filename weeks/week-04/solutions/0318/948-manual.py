import sys


def check_ok(coin, heavy, weighings):
    # Check if 'coin' being the fake (heavy or light) is consistent with all weighings.
    for left, right, result in weighings:
        if result == '=':
            # Both sides are genuine; fake coin cannot appear here.
            if coin in left or coin in right:
                return False
        elif result == '<':
            
            if coin in left:
                if heavy:
                    return False
            elif coin in right:
                if not heavy:
                    return False
            else:
                return False
        else:  # '>'
            
            if coin in left:
                if not heavy:
                    return False
            elif coin in right:
                if heavy:
                    return False
            else:
                return False
    return True


def find_fake(n, weighings):
    
    candidates = []
    for coin in range(1, n + 1):
        if check_ok(coin, True, weighings) or check_ok(coin, False, weighings):
            candidates.append(coin)
    return candidates[0] if len(candidates) == 1 else 0


def main():
    lines = sys.stdin.read().split('\n')
    nonempty = (line.strip() for line in lines if line.strip())
    it = iter(nonempty)

    M = int(next(it))
    results = []

    for _ in range(M):
        n, k = map(int, next(it).split())
        weighings = []
        for _ in range(k):
            nums = list(map(int, next(it).split()))
            p = nums[0]
            left  = set(nums[1:      p + 1])
            right = set(nums[p + 1: 2*p + 1])
            symbol = next(it)
            weighings.append((left, right, symbol))
        results.append(str(find_fake(n, weighings)))

    print('\n\n'.join(results))


if __name__ == '__main__':
    main()
