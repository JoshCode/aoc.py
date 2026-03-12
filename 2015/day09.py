from typing import Any
from itertools import permutations
import re

def part1(input: list[str]) -> Any:
    parse_regex = re.compile(r"^(?P<n1>\w+) to (?P<n2>\w+) = (?P<dist>\d+)$")
    locations: set[str] = set()
    distances: dict[str, dict[str, int]] = {}

    for line in input:
        match = parse_regex.match(line)
        if match:
            groups = match.groups()
            # print(f"{line=}, {groups=}")
            n1, n2, dist = groups
            locations.add(n1)
            locations.add(n2)
            if n1 not in distances:
                distances[n1] = {}
            if n2 not in distances:
                distances[n2] = {}
            distances[n1][n2] = int(dist)
            distances[n2][n1] = int(dist)
    
    shortest_distance: int | float = float("inf")

    for path in permutations(locations):
        dist = 0
        for i in range(len(path)-1):
            dist += distances[path[i]][path[i+1]]
        shortest_distance = min(shortest_distance, dist)

    return shortest_distance


def part2(input: list[str]) -> Any:
    parse_regex = re.compile(r"^(?P<n1>\w+) to (?P<n2>\w+) = (?P<dist>\d+)$")
    locations: set[str] = set()
    distances: dict[str, dict[str, int]] = {}

    for line in input:
        match = parse_regex.match(line)
        if match:
            groups = match.groups()
            # print(f"{line=}, {groups=}")
            n1, n2, dist = groups
            locations.add(n1)
            locations.add(n2)
            if n1 not in distances:
                distances[n1] = {}
            if n2 not in distances:
                distances[n2] = {}
            distances[n1][n2] = int(dist)
            distances[n2][n1] = int(dist)
    
    longest_distance: int | float = float("-inf")

    for path in permutations(locations):
        dist = 0
        for i in range(len(path)-1):
            dist += distances[path[i]][path[i+1]]
        longest_distance = max(longest_distance, dist)

    return longest_distance


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
