from typing import Any
import re
from itertools import permutations


def part1(input: list[str]) -> Any:
    result: int = 0

    edges: dict[str, dict[str, int]] = {}
    parse_re = re.compile(
        r"^(?P<n1>\w+) would (?P<op>\w+) (?P<value>\d+) happiness units by sitting next to (?P<n2>\w+).$"
    )

    for line in input:
        match = parse_re.match(line)
        if not match:
            continue
        n1, op, value, n2 = match.groups()
        value = int(value)

        match op:
            case "gain":
                pass
            case "lose":
                value = -value
            case _:
                raise ValueError(f"Unsupported operation: {op} in line: {line}")

        if n1 not in edges:
            edges[n1] = {}

        edges[n1][n2] = value

    # TODO This is too many seating orders.
    # For example: 1, 2, 3, 4 is the same seating order as 2, 3, 4, 1 as far as cost is concerned
    seating_orders = list(permutations(edges.keys()))
    seating_orders_cost: list[int] = []

    for order in seating_orders:
        seating_orders_cost.append(calculate_seating_cost(order, edges))

    result = max(seating_orders_cost)
    return result


def calculate_seating_cost(
    seating_order: tuple[str, ...], edges: dict[str, dict[str, int]]
) -> int:
    result = 0

    round_seating_order = seating_order + (seating_order[0],)
    pass
    for i, person in enumerate(round_seating_order[:-1]):
        next_person = round_seating_order[i + 1]
        result += edges[person][next_person]
        result += edges[next_person][person]

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    edges: dict[str, dict[str, int]] = {"Me": {}}
    parse_re = re.compile(
        r"^(?P<n1>\w+) would (?P<op>\w+) (?P<value>\d+) happiness units by sitting next to (?P<n2>\w+).$"
    )

    for line in input:
        match = parse_re.match(line)
        if not match:
            continue
        n1, op, value, n2 = match.groups()
        value = int(value)

        match op:
            case "gain":
                pass
            case "lose":
                value = -value
            case _:
                raise ValueError(f"Unsupported operation: {op} in line: {line}")

        if n1 not in edges:
            edges[n1] = {"Me": 0}

        edges[n1][n2] = value
        edges["Me"][n2] = 0

    seating_orders = list(permutations(edges.keys()))
    seating_orders_cost: list[int] = []

    for order in seating_orders:
        seating_orders_cost.append(calculate_seating_cost(order, edges))

    result = max(seating_orders_cost)
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
