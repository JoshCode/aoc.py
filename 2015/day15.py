import re
from dataclasses import dataclass
from itertools import combinations_with_replacement
from typing import Any


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def part1(input: list[str]) -> Any:
    result: int = 0

    ingredients = parse(input)
    combinations = combinations_with_replacement(ingredients, 100)
    scores: list[int] = []

    for combination in combinations:
        scores.append(calculate_score(combination))

    result = max(scores)

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    ingredients = parse(input)
    combinations = combinations_with_replacement(ingredients, 100)
    scores: list[int] = []

    for combination in combinations:
        scores.append(calculate_score(combination, part2=True))

    result = max(scores)

    return result


def calculate_score(combination: tuple[Ingredient, ...], part2: bool = False) -> int:
    total_capacity = total_durability = total_flavor = total_texture = (
        total_calories
    ) = 0

    for ingredient in combination:
        total_capacity += ingredient.capacity
        total_durability += ingredient.durability
        total_flavor += ingredient.flavor
        total_texture += ingredient.texture
        total_calories += ingredient.calories

    if part2 and total_calories != 500:
        return 0

    total_capacity = max(total_capacity, 0)
    total_durability = max(total_durability, 0)
    total_flavor = max(total_flavor, 0)
    total_texture = max(total_texture, 0)

    result = total_capacity * total_durability * total_flavor * total_texture

    return result


def parse(input: list[str]) -> list[Ingredient]:
    parse_re = re.compile(
        r"^(?P<name>\w+): "
        r"capacity (?P<capacity>-?\d+), "
        r"durability (?P<durability>-?\d+), "
        r"flavor (?P<flavor>-?\d+), "
        r"texture (?P<texture>-?\d+), "
        r"calories (?P<calories>-?\d+)$"
    )
    print(parse_re.pattern)

    result: list[Ingredient] = []

    for line in input:
        match = parse_re.match(line)
        if not match:
            continue
        name, capacity, durability, flavor, texture, calories = match.groups()
        ingredient = Ingredient(
            name,
            int(capacity),
            int(durability),
            int(flavor),
            int(texture),
            int(calories),
        )
        result.append(ingredient)

    return result


# region Input file handling
def main():
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

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
                out1_e = part1(example_lines)
            if run_part1[1]:
                print("   > Input")
                out1_i = part1(input_lines)

        if any(run_part2):
            print("-> Running part 2")
            if run_part2[0]:
                print("   > Example")
                out2_e = part2(example_lines)
            if run_part2[1]:
                print("   > Input")
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
