from collections import Counter, defaultdict, namedtuple
from pathlib import Path

General = namedtuple(
    "General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"]
)


def load_generals(filename="generals.txt"):
    generals = {}
    file_path = Path(__file__).resolve().parent / filename
    with file_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if line == "EOF":
                break
            if not line:
                continue
            faction, name, hp, atk, def_, spd, is_leader = line.split()
            generals[name] = General(
                faction,
                name,
                int(hp),
                int(atk),
                int(def_),
                int(spd),
                is_leader == "True",
            )
    return generals


def simulate_easy_battle(generals):
    damage = Counter()
    losses = defaultdict(int)

    alliance = [g for g in generals.values() if g.faction in {"蜀", "吳"}]
    alliance = sorted(alliance, key=lambda g: g.spd, reverse=True)
    wei = [g for g in generals.values() if g.faction == "魏"]
    wei = sorted(wei, key=lambda g: g.spd, reverse=True)

    for round_no in range(1, 4):
        for i, attacker in enumerate(alliance[: round_no + 2]):
            target = wei[i % len(wei)]
            dealt = max(1, attacker.atk - target.def_)
            damage[attacker.name] += dealt
            losses[target.name] += dealt

    return damage, losses


def main():
    generals = load_generals()
    damage, losses = simulate_easy_battle(generals)

    print("Top Damage (Easy Version)")
    for rank, (name, value) in enumerate(damage.most_common(5), 1):
        print(f"{rank}. {name}: {value}")

    print("\nLosses")
    for name, value in sorted(losses.items(), key=lambda item: item[1], reverse=True):
        print(f"{name}: {value}")


if __name__ == "__main__":
    main()
