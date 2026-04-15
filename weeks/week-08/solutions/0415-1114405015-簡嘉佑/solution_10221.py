import math


def solve(input_data: str) -> str:
    """
    UVA 10221 - Satellites

    題目要對每一筆輸入 (s, a, unit) 計算：
    1) 弧長 arc
    2) 弦長 chord

    幾何關係：
    - 地球半徑固定為 6440
    - 衛星軌道半徑 r = 6440 + s
    - 若角度超過 180 度，需改用較小圓心角：angle = 360 - angle
    - 弧長 arc = r * theta
    - 弦長 chord = 2 * r * sin(theta / 2)
      其中 theta 是弧度（radian）

    輸出格式：每筆輸出一行，arc 與 chord 皆保留小數點後六位。
    """
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    outputs = []

    for line in lines:
        parts = line.split()
        s = float(parts[0])
        a = float(parts[1])
        unit = parts[2]

        # 軌道半徑 = 地球半徑 + 衛星高度
        r = 6440.0 + s

        # 若角度是分（arcminute），先轉成度（degree）
        if unit == "min":
            a /= 60.0

        # 本題要取較短弧，因此角度大於 180 度時取補角
        if a > 180.0:
            a = 360.0 - a

        # 度轉弧度
        theta = math.radians(a)

        arc = r * theta
        chord = 2.0 * r * math.sin(theta / 2.0)

        outputs.append(f"{arc:.6f} {chord:.6f}")

    return "\n".join(outputs)


def main() -> None:
    import sys

    print(solve(sys.stdin.read()))


if __name__ == "__main__":
    main()
