from __future__ import annotations

from collections import Counter, defaultdict, namedtuple
from pathlib import Path
from typing import Dict, List, Tuple

General = namedtuple(
    "General", ["faction", "name", "hp", "atk", "def_", "spd", "is_leader"]
)


class ChibiBattle:
    """Chibi battle simulator with data loading, stats, and ASCII reporting."""

    def __init__(self) -> None:
        self.generals: Dict[str, General] = {}
        self.stats = {
            "damage": Counter(),
            "losses": defaultdict(int),
        }

    def _resolve_path(self, filename: str) -> Path:
        path = Path(filename)
        if path.is_absolute():
            return path
        return Path(__file__).resolve().parent / path

    def load_generals(self, filename: str = "generals.txt") -> None:
        file_path = self._resolve_path(filename)
        with file_path.open("r", encoding="utf-8") as handle:
            for raw_line in handle:
                line = raw_line.strip()
                if line == "EOF":
                    break
                if not line:
                    continue

                faction, name, hp, atk, def_, spd, is_leader = line.split()
                self.generals[name] = General(
                    faction=faction,
                    name=name,
                    hp=int(hp),
                    atk=int(atk),
                    def_=int(def_),
                    spd=int(spd),
                    is_leader=(is_leader == "True"),
                )

    def get_battle_order(self) -> List[General]:
        return sorted(self.generals.values(), key=lambda g: g.spd, reverse=True)

    def calculate_damage(self, attacker_name: str, defender_name: str) -> int:
        attacker = self.generals[attacker_name]
        defender = self.generals[defender_name]

        damage = max(1, attacker.atk - defender.def_)
        self.stats["damage"][attacker_name] += damage
        self.stats["losses"][defender_name] += damage
        return damage

    def _living_generals(self, faction: str) -> List[General]:
        living = []
        for general in self.generals.values():
            if general.faction != faction:
                continue
            remaining = general.hp - self.stats["losses"][general.name]
            if remaining > 0:
                living.append(general)
        return living

    def simulate_wave(self, wave_num: int) -> None:
        if wave_num <= 0:
            return

        alliance = [g for g in self.get_battle_order() if g.faction in {"蜀", "吳"}]
        wei = [g for g in self.get_battle_order() if g.faction == "魏"]

        attack_count = min(wave_num + 2, len(alliance))
        for i, attacker in enumerate(alliance[:attack_count]):
            if not wei:
                break
            target = wei[i % len(wei)]
            self.calculate_damage(attacker.name, target.name)

        retaliation_count = min(max(1, wave_num - 1), len(wei))
        living_alliance = [g for g in self._living_generals("蜀") + self._living_generals("吳")]
        for i, attacker in enumerate(wei[:retaliation_count]):
            if not living_alliance:
                break
            target = living_alliance[i % len(living_alliance)]
            self.calculate_damage(attacker.name, target.name)

    def simulate_battle(self, waves: int = 3) -> None:
        for wave_num in range(1, waves + 1):
            self.simulate_wave(wave_num)

    def get_damage_ranking(self, top_n: int = 5) -> List[Tuple[str, int]]:
        return self.stats["damage"].most_common(top_n)

    def get_faction_stats(self) -> Dict[str, int]:
        faction_damage: Dict[str, int] = defaultdict(int)
        for general_name, damage in self.stats["damage"].items():
            faction = self.generals[general_name].faction
            faction_damage[faction] += damage
        return dict(faction_damage)

    def get_defeated_generals(self) -> List[str]:
        defeated = []
        for name, total_loss in self.stats["losses"].items():
            if total_loss >= self.generals[name].hp:
                defeated.append(name)
        return defeated

    def print_battle_start(self) -> None:
        print("=" * 60)
        print("Chibi Battle: Shu+Wu Alliance vs Wei")
        print("=" * 60)
        for faction in ["蜀", "吳", "魏"]:
            print(f"[{faction}]")
            faction_generals = [g for g in self.get_battle_order() if g.faction == faction]
            for general in faction_generals:
                hp_blocks = max(0, (general.hp - self.stats['losses'][general.name]) // 10)
                bar = "#" * hp_blocks + "." * (12 - min(12, hp_blocks))
                role = " strategist" if general.is_leader else ""
                print(
                    f"  {general.name:<8} HP:{bar} "
                    f"ATK:{general.atk:>2} DEF:{general.def_:>2} SPD:{general.spd:>2}{role}"
                )
            print()

    def print_damage_report(self) -> None:
        print("=" * 60)
        print("Damage Ranking")
        print("=" * 60)
        for idx, (name, damage) in enumerate(self.get_damage_ranking(5), 1):
            bar_len = min(20, damage // 5)
            bar = "#" * bar_len + "." * (20 - bar_len)
            print(f"{idx:>2}. {name:<8} {bar} {damage:>3}")

        print("\nFaction Damage")
        faction_stats = self.get_faction_stats()
        total_damage = sum(faction_stats.values()) or 1
        max_faction_damage = max(faction_stats.values(), default=1)
        for faction in ["蜀", "吳", "魏"]:
            value = faction_stats.get(faction, 0)
            ratio = int((value / max_faction_damage) * 20) if max_faction_damage else 0
            bar = "#" * ratio + "." * (20 - ratio)
            percentage = (value / total_damage) * 100
            print(f"{faction} {bar} {value:>3} ({percentage:>5.1f}%)")

        print("\nDefeated Generals")
        defeated = self.get_defeated_generals()
        if defeated:
            for name in defeated:
                print(f"- {name}")
        else:
            print("- None")

    def run_full_battle(self, generals_file: str = "generals.txt") -> None:
        if not self.generals:
            self.load_generals(generals_file)
        self.print_battle_start()
        self.simulate_battle()
        self.print_damage_report()


if __name__ == "__main__":
    game = ChibiBattle()
    game.run_full_battle("generals.txt")
