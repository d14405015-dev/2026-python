import sys


# 七段顯示器 bitmask（a~g 共 7 段）
SEG = {
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
REV = {v: k for k, v in SEG.items()}


def build_maps():
    """建立三種轉換表：拿走一根、增加一根、同位內搬一根。"""
    rem = {d: set() for d in range(10)}
    add = {d: set() for d in range(10)}
    move = {d: set() for d in range(10)}

    for d in range(10):
        m = SEG[d]
        for b in range(7):
            bit = 1 << b
            if m & bit:
                nm = m ^ bit
                if nm in REV:
                    rem[d].add(REV[nm])
            else:
                nm = m | bit
                if nm in REV:
                    add[d].add(REV[nm])

        for rb in range(7):
            rbit = 1 << rb
            if not (m & rbit):
                continue
            for ab in range(7):
                abit = 1 << ab
                if m & abit:
                    continue
                nm = (m ^ rbit) | abit
                if nm in REV:
                    move[d].add(REV[nm])

    return (
        {k: sorted(v) for k, v in rem.items()},
        {k: sorted(v) for k, v in add.items()},
        {k: sorted(v) for k, v in move.items()},
    )


REM, ADD, MOVE = build_maps()


def parse_equation(expr):
    """把等式轉為 base_sum 與每個數字位置的影響係數。

    如果把等式看成：左邊 - 右邊 = 0
    那麼每個數字改變時，對整體只會造成線性增量，
    可以 O(1) 檢查成立與否。
    """
    eq = expr.index("=")

    def parse_side(st, ed, side_sign):
        i = st
        out = []
        while i < ed:
            sign = 1
            if expr[i] == "+":
                i += 1
            elif expr[i] == "-":
                sign = -1
                i += 1

            s = i
            while i < ed and expr[i].isdigit():
                i += 1
            e = i
            val = int(expr[s:e])
            out.append((s, e, val, side_sign * sign))
        return out

    tokens = parse_side(0, eq, 1) + parse_side(eq + 1, len(expr), -1)
    base = 0
    info = {}
    for s, e, val, c in tokens:
        base += c * val
        for pos in range(s, e):
            place = 10 ** (e - 1 - pos)
            old = int(expr[pos])
            info[pos] = (c * place, old)

    return base, info


def solve(data):
    """輸入一條以 # 結尾的式子，輸出修正後式子或 No。"""
    h = data.find("#")
    if h == -1:
        return "No\n"

    expr = data[:h]
    chars = list(expr)
    positions = [i for i, ch in enumerate(chars) if ch.isdigit()]

    if not positions:
        return "No\n"

    base, info = parse_equation(expr)

    for src in positions:
        src_digit = int(chars[src])
        src_factor, src_old = info[src]

        for dst in positions:
            dst_digit = int(chars[dst])

            # 同一數字內搬一根
            if src == dst:
                for nd in MOVE[src_digit]:
                    if base + src_factor * (nd - src_old) == 0:
                        ans = chars[:]
                        ans[src] = str(nd)
                        return "".join(ans) + "#\n"
                continue

            # 跨兩個數字搬一根
            dst_factor, dst_old = info[dst]
            for ns in REM[src_digit]:
                delta_s = src_factor * (ns - src_old)
                for nd in ADD[dst_digit]:
                    delta_d = dst_factor * (nd - dst_old)
                    if base + delta_s + delta_d == 0:
                        ans = chars[:]
                        ans[src] = str(ns)
                        ans[dst] = str(nd)
                        return "".join(ans) + "#\n"

    return "No\n"


def main():
    sys.stdout.write(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()