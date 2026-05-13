def solve(n_str: str) -> str:
    odd_sum = 0
    even_sum = 0
    
    for position, digit_char in enumerate(reversed(n_str)):
        digit = int(digit_char)
        if position % 2 == 0:
            odd_sum += digit
        else:
            even_sum += digit
    
    diff = odd_sum - even_sum
    
    if diff % 11 == 0:
        return f"{n_str} is a multiple of 11."
    else:
        return f"{n_str} is not a multiple of 11."


if __name__ == "__main__":
    while True:
        line = input().strip()
        if line == "0":
            break
        print(solve(line))
