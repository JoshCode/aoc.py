import re
from itertools import combinations
from typing import Any


class Item:
    def __init__(self, name: str, cost: int, damage: int, armor: int):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.armor = armor

    def __repr__(self) -> str:
        return f"Item({self.name})"


WEAPONS: list[Item] = [
    Item("Dagger", 8, 4, 0),
    Item("Shortsword", 10, 5, 0),
    Item("Warhammer", 25, 6, 0),
    Item("Longsword", 40, 7, 0),
    Item("Greataxe", 74, 8, 0),
]

ARMOR: list[Item] = [
    Item("Leather", 13, 0, 1),
    Item("Chainmail", 31, 0, 2),
    Item("Splintmail", 53, 0, 3),
    Item("Bandedmail", 75, 0, 4),
    Item("Platemail", 102, 0, 5),
]

RINGS: list[Item] = [
    Item("Damage +1", 25, 1, 0),
    Item("Damage +2", 50, 2, 0),
    Item("Damage +3", 100, 3, 0),
    Item("Defense +1", 20, 0, 1),
    Item("Defense +2", 40, 0, 2),
    Item("Defense +3", 80, 0, 3),
]


def parse(line: str) -> int:
    match = re.search(r"\d+", line)
    assert match, f"No number found in line: {line!r}"
    return int(match.group())


def gear_cost(gear_set: list[Item]):
    return sum(item.cost for item in gear_set)


def part1(input: list[str]) -> Any:
    result: int | None = None
    boss_hitpoints, boss_damage, boss_armor = (parse(line) for line in input[:3])

    gear_sets: list[list[Item]] = []

    for weapon in WEAPONS:
        for ring_count in range(3):
            for rings in combinations(RINGS, ring_count):
                gear_sets.append([weapon, *rings])
                for armor in ARMOR:
                    gear_sets.append([weapon, armor, *rings])

    gear_sets.sort(key=gear_cost)

    player_hitpoints = 100
    for gear_set in gear_sets:
        player_damage = sum(item.damage for item in gear_set)
        player_armor = sum(item.armor for item in gear_set)

        player_effective_damage = max(player_damage - boss_armor, 1)
        boss_effective_damage = max(boss_damage - player_armor, 1)

        boss_current_hitpoints = boss_hitpoints
        player_current_hitpoints = player_hitpoints
        while True:
            boss_current_hitpoints -= player_effective_damage

            if boss_current_hitpoints <= 0:
                result = gear_cost(gear_set)
                break

            player_current_hitpoints -= boss_effective_damage
            if player_current_hitpoints <= 0:
                break

        if result is not None:
            break

    return result


def part2(input: list[str]) -> Any:
    result: int | None = None
    boss_hitpoints, boss_damage, boss_armor = (parse(line) for line in input[:3])

    gear_sets: list[list[Item]] = []

    for weapon in WEAPONS:
        for ring_count in range(3):
            for rings in combinations(RINGS, ring_count):
                gear_sets.append([weapon, *rings])
                for armor in ARMOR:
                    gear_sets.append([weapon, armor, *rings])

    gear_sets.sort(key=gear_cost, reverse=True)

    player_hitpoints = 100
    for gear_set in gear_sets:
        player_damage = sum(item.damage for item in gear_set)
        player_armor = sum(item.armor for item in gear_set)

        player_effective_damage = max(player_damage - boss_armor, 1)
        boss_effective_damage = max(boss_damage - player_armor, 1)

        boss_current_hitpoints = boss_hitpoints
        player_current_hitpoints = player_hitpoints
        win = False
        while True:
            boss_current_hitpoints -= player_effective_damage

            if boss_current_hitpoints <= 0:
                win = True
                break

            player_current_hitpoints -= boss_effective_damage
            if player_current_hitpoints <= 0:
                win = False
                result = gear_cost(gear_set)
                break

        if result is not None and win:
            break

    return result


# region Input file handling
def main():
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, False)
    run_part2 = (True, False)

    global is_example
    is_example = False

    script_file = Path(__file__)
    day_nr = script_file.stem[-2:]

    script_path = script_file.parent

    example_file = script_path / f"data/day{day_nr}-example.txt"
    input_file = script_path / f"data/day{day_nr}-input.txt"

    example_file.touch(exist_ok=True)
    input_file.touch(exist_ok=True)

    with (
        open(example_file, "r", encoding="utf-8") as example,
        open(input_file, "r", encoding="utf-8") as input,
    ):
        example_lines: list[str] = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines: list[str] = []
        for row in input.readlines():
            input_lines.append(row.replace("\n", ""))

        out1_e = out1_i = out2_e = out2_i = None

        if any(run_part1):
            print("-> Running part 1")
            if run_part1[0]:
                print("   > Example")
                is_example = True
                out1_e = part1(example_lines)
            if run_part1[1]:
                print("   > Input")
                is_example = False
                out1_i = part1(input_lines)

        if any(run_part2):
            print("-> Running part 2")
            if run_part2[0]:
                print("   > Example")
                is_example = True
                out2_e = part2(example_lines)
            if run_part2[1]:
                print("   > Input")
                is_example = False
                out2_i = part2(input_lines)

        print("")
        if run_part1[0]:
            print(f"{out1_e=}")
        if run_part1[1]:
            print(f"{out1_i=}")
        if run_part2[0]:
            print(f"{out2_e=}")
        if run_part2[1]:
            print(f"{out2_i=}")


if __name__ == "__main__":
    main()
# endregion
