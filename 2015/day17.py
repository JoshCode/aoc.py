from itertools import combinations
from typing import Any


def part1(input: list[str]) -> Any:
    result: int = 0

    containers: list[int] = []
    for row in input:
        containers.append(int(row))

    containers.sort(reverse=True)

    FLUID_AMOUNT = 25 if is_example else 150

    solutions: list[tuple[int, ...]] = []

    # TODO There may be a better way to do this, but this works fast enough for the input size.
    # Find out if this following algorithm is faster:
    # Create a stack to hold indices of containers, add containers until sum >= target.
    # If it is equal, it's a solution
    # In both cases, pop the last container and add the next one, if there is one. If not, pop the previous one and add the next one, etc.
    for i in range(1, len(containers) + 1):
        for combination in combinations(containers, i):
            if sum(combination) == FLUID_AMOUNT:
                solutions.append(combination)

    result = len(solutions)
    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    containers: list[int] = []
    for row in input:
        containers.append(int(row))

    containers.sort(reverse=True)

    FLUID_AMOUNT = 25 if is_example else 150

    solutions: list[tuple[int, ...]] = []

    for i in range(1, len(containers) + 1):
        for combination in combinations(containers, i):
            if sum(combination) == FLUID_AMOUNT:
                solutions.append(combination)
        if len(solutions) > 0:
            break

    result = len(solutions)
    return result


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
