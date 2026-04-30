import re
from typing import Any


def part1(input: list[str]) -> Any:
    result: int = 0

    substitutions, molecule = parse(input)

    # Compute possible strings
    possibilities: set[str] = all_substitutions(molecule, substitutions)

    result = len(possibilities)
    return result


# This algorithm should be turned around
# Do not find the target string from 'e', but explore the space back from target to 'e', trying to reduce as fast as possible
def part2(input: list[str]) -> Any:
    result: int = 0

    substitutions, molecule = parse(input)

    search_space: set[str] = set()
    distances: dict[str, int] = {}
    search_space.add("e")
    distances["e"] = 0

    while True:
        if molecule in search_space:
            result = distances[molecule]
            break

        new_distances: dict[str, int] = {}
        new_search_space: set[str] = set()
        first = True
        for s in search_space:
            if first:
                print(s)
                print(len(s))
                first = False
            s_distance = distances[s]
            new_strs = all_substitutions(s, substitutions)
            for new_str in new_strs:
                if new_str not in new_search_space:
                    new_distances[new_str] = s_distance + 1
                    new_search_space.add(new_str)
                else:
                    new_distances[new_str] = min(new_distances[new_str], s_distance + 1)

        search_space = new_search_space
        distances = new_distances
        pass

    return result


def all_substitutions(target_str: str, substitutions: dict[str, set[str]]) -> set[str]:
    result: set[str] = set()

    for sub in substitutions:
        regex = re.compile(f"{sub}")
        for match in regex.finditer(target_str):
            for replacement in substitutions[sub]:
                replaced_str: str = (
                    target_str[0 : match.start()]
                    + replacement
                    + target_str[match.end() :]
                )
                result.add(replaced_str)

    return result


def parse(input: list[str]) -> tuple[dict[str, set[str]], str]:
    substitutions: dict[str, set[str]] = {}
    molecule = ""

    for line in input:
        line_split = line.split(" => ")

        if len(line_split) > 1:
            left, right = line_split
            if left not in substitutions:
                substitutions[left] = set()

            substitutions[left].add(right)

        else:
            if len(line_split[0].strip()) == 0:
                continue
            molecule = line_split[0]

    return substitutions, molecule


# region Input file handling
def main():
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

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
