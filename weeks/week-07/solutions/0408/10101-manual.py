import sys


DIGIT_MASKS = {
    0: 0b1111110,
    1: 0b0110000,
    2: 0b1101101,
    3: 0b1111001,
    4: 0b0110011,
    5: 0b1011011,
    6: 0b1011111,
    7: 0b1110000,
    8: 0b1111111,
    9: 0b1111011,
}

MASK_TO_DIGIT = {mask: digit for digit, mask in DIGIT_MASKS.items()}


def build_maps():
    remove_map = {d: [] for d in range(10)}
    add_map = {d: [] for d in range(10)}
    move_map = {d: [] for d in range(10)}

    for d in range(10):
        m = DIGIT_MASKS[d]

        for b in range(7):
            bit = 1 << b
            if m & bit:
                nm = m ^ bit
                if nm in MASK_TO_DIGIT:
                    remove_map[d].append(MASK_TO_DIGIT[nm])
            else:
                nm = m | bit
                if nm in MASK_TO_DIGIT:
                    add_map[d].append(MASK_TO_DIGIT[nm])

        for rb in range(7):
            rbit = 1 << rb
            if not (m & rbit):
                continue
            for ab in range(7):
                abit = 1 << ab
                if m & abit:
                    continue
                nm = (m ^ rbit) | abit
                if nm in MASK_TO_DIGIT:
                    move_map[d].append(MASK_TO_DIGIT[nm])

        remove_map[d] = sorted(set(remove_map[d]))
        add_map[d] = sorted(set(add_map[d]))
        move_map[d] = sorted(set(move_map[d]))

    return remove_map, add_map, move_map


REMOVE_MAP, ADD_MAP, MOVE_MAP = build_maps()


def parse_equation(expr):
    eq = expr.index("=")

    def parse_side(start, end, side_sign):
        i = start
        out = []
        while i < end:
            sign = 1
            if expr[i] == "+":
                i += 1
            elif expr[i] == "-":
                sign = -1
                i += 1

            s = i
            while i < end and expr[i].isdigit():
                i += 1
            e = i

            value = int(expr[s:e])
            out.append((s, e, value, side_sign * sign))
        return out

    tokens = parse_side(0, eq, 1) + parse_side(eq + 1, len(expr), -1)

    base_sum = 0
    info = {}
    for s, e, value, coeff in tokens:
        base_sum += coeff * value
        for pos in range(s, e):
            place = 10 ** (e - 1 - pos)
            old_digit = int(expr[pos])
            info[pos] = (coeff * place, old_digit)

    return base_sum, info


def solve(data):
    h = data.find("#")
    if h == -1:
        return "No\n"

    expr = data[:h]
    chars = list(expr)
    positions = [i for i, ch in enumerate(chars) if ch.isdigit()]
    if not positions:
        return "No\n"

    base_sum, info = parse_equation(expr)

    for src in positions:
        src_digit = int(chars[src])
        src_factor, src_old = info[src]

        for dst in positions:
            dst_digit = int(chars[dst])

            if src == dst:
                for nd in MOVE_MAP[src_digit]:
                    if base_sum + src_factor * (nd - src_old) == 0:
                        ans = chars[:]
                        ans[src] = str(nd)
                        return "".join(ans) + "#\n"
                continue

            dst_factor, dst_old = info[dst]

            for ns in REMOVE_MAP[src_digit]:
                delta_s = src_factor * (ns - src_old)
                for nd in ADD_MAP[dst_digit]:
                    delta_d = dst_factor * (nd - dst_old)
                    if base_sum + delta_s + delta_d == 0:
                        ans = chars[:]
                        ans[src] = str(ns)
                        ans[dst] = str(nd)
                        return "".join(ans) + "#\n"

    return "No\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
