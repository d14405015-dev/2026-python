import sys


# 七段顯示器：每個數字對應到哪些段（a~g）。
# 這裡用 bitmask 表示，bit = 1 代表該段有亮。
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


def build_transitions():
    """預先建立「移動一根木棒」可到達的數字轉移。

    回傳三個對照表：
    1. remove_map[d]：把數字 d 移除一根木棒後，可變成哪些數字
    2. add_map[d]：把數字 d 增加一根木棒後，可變成哪些數字
    3. move_inside_map[d]：在同一個數字內把一根木棒搬位置後，可變成哪些數字
    """
    remove_map = {d: [] for d in range(10)}
    add_map = {d: [] for d in range(10)}
    move_inside_map = {d: [] for d in range(10)}

    for digit in range(10):
        mask = DIGIT_MASKS[digit]

        # 移除一根木棒：關掉目前亮著的一個 bit。
        for bit in range(7):
            if mask & (1 << bit):
                new_mask = mask ^ (1 << bit)
                if new_mask in MASK_TO_DIGIT:
                    remove_map[digit].append(MASK_TO_DIGIT[new_mask])

        # 增加一根木棒：把目前沒亮的一個 bit 打開。
        for bit in range(7):
            if not (mask & (1 << bit)):
                new_mask = mask | (1 << bit)
                if new_mask in MASK_TO_DIGIT:
                    add_map[digit].append(MASK_TO_DIGIT[new_mask])

        # 同一數字內搬一根：先關一根，再開另一根。
        for remove_bit in range(7):
            if not (mask & (1 << remove_bit)):
                continue
            for add_bit in range(7):
                if mask & (1 << add_bit):
                    continue
                new_mask = (mask ^ (1 << remove_bit)) | (1 << add_bit)
                if new_mask in MASK_TO_DIGIT:
                    move_inside_map[digit].append(MASK_TO_DIGIT[new_mask])

        # 去重與排序，讓輸出穩定（可重現）。
        remove_map[digit] = sorted(set(remove_map[digit]))
        add_map[digit] = sorted(set(add_map[digit]))
        move_inside_map[digit] = sorted(set(move_inside_map[digit]))

    return remove_map, add_map, move_inside_map


REMOVE_MAP, ADD_MAP, MOVE_INSIDE_MAP = build_transitions()


def parse_tokens_and_digit_info(expression):
    """解析等式，建立快速驗證用資訊。

    我們把整條等式改寫成：
    sum(coeff_i * value_i) = 0

    - 左邊數字的 coeff 由原本正負號決定（+1 或 -1）
    - 右邊數字的 coeff 反向（乘上 -1）

    這樣判斷等式是否成立就變成：總和是否為 0。

    另外建立 digit_info：
    對每一個數字字元位置，記錄：
    - 該位數改變 1 時，總和會變多少（coeff * place_value）
    - 原本數字值
    """
    equal_index = expression.index("=")

    def parse_side(start, end, side_factor):
        index = start
        tokens = []
        while index < end:
            sign = 1
            if expression[index] == "+":
                sign = 1
                index += 1
            elif expression[index] == "-":
                sign = -1
                index += 1

            number_start = index
            while index < end and expression[index].isdigit():
                index += 1
            number_end = index

            number_text = expression[number_start:number_end]
            number_value = int(number_text)
            coeff = side_factor * sign
            tokens.append((number_start, number_end, number_value, coeff))

        return tokens

    left_tokens = parse_side(0, equal_index, 1)
    right_tokens = parse_side(equal_index + 1, len(expression), -1)
    tokens = left_tokens + right_tokens

    base_sum = 0
    digit_info = {}
    for start, end, value, coeff in tokens:
        base_sum += coeff * value
        for position in range(start, end):
            place_value = 10 ** (end - 1 - position)
            old_digit = int(expression[position])
            digit_info[position] = (coeff * place_value, old_digit)

    return base_sum, digit_info


def solve(expression_with_hash):
    """找出移動一根木棒後可成立的等式；若無解回傳 No。"""
    hash_index = expression_with_hash.find("#")
    if hash_index == -1:
        return "No\n"

    expression = expression_with_hash[:hash_index]
    chars = list(expression)

    digit_positions = [i for i, ch in enumerate(chars) if ch.isdigit()]
    if not digit_positions:
        return "No\n"

    base_sum, digit_info = parse_tokens_and_digit_info(expression)

    # 依序枚舉「來源數字位置」與「目的數字位置」。
    # 找到第一個可行解就輸出，確保結果穩定。
    for source_pos in digit_positions:
        source_digit = int(chars[source_pos])
        source_factor, source_old_digit = digit_info[source_pos]

        for target_pos in digit_positions:
            target_digit = int(chars[target_pos])

            # 情況一：在同一個數字內移動（先關一段再開另一段）。
            if source_pos == target_pos:
                for new_digit in MOVE_INSIDE_MAP[source_digit]:
                    delta = source_factor * (new_digit - source_old_digit)
                    if base_sum + delta == 0:
                        candidate = chars[:]
                        candidate[source_pos] = str(new_digit)
                        return "".join(candidate) + "#\n"
                continue

            # 情況二：從 source 拿一根，放到 target。
            target_factor, target_old_digit = digit_info[target_pos]

            for new_source_digit in REMOVE_MAP[source_digit]:
                delta_source = source_factor * (new_source_digit - source_old_digit)
                for new_target_digit in ADD_MAP[target_digit]:
                    delta_target = target_factor * (new_target_digit - target_old_digit)
                    if base_sum + delta_source + delta_target == 0:
                        candidate = chars[:]
                        candidate[source_pos] = str(new_source_digit)
                        candidate[target_pos] = str(new_target_digit)
                        return "".join(candidate) + "#\n"

    return "No\n"


def main():
    input_data = sys.stdin.read()
    sys.stdout.write(solve(input_data))


if __name__ == "__main__":
    main()