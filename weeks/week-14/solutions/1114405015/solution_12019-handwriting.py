from datetime import date

names = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

t = int(input().strip())
for _ in range(t):
    m, d = map(int, input().split())
    print(names[date(2012, m, d).weekday()])
