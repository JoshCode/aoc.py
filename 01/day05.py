import io
from dataclasses import dataclass
import copy


@dataclass
class Range:
    lower: int
    upper: int


def part1(input: list[str]) -> int:
    result: int = 0

    in_ranges = True
    ranges: list[Range] = []
    products: list[int] = []

    # Input parsing
    for line in input:
        if line == "":
            in_ranges = False
            continue
        if in_ranges:
            line_parsed = list(map(int, line.split("-")))
            ranges.append(Range(line_parsed[0], line_parsed[1]))
        else:
            products.append(int(line))

    ranges = sorted(ranges, key=lambda r: r.lower)
    ranges_merged: list[Range] = [copy.copy(ranges[0])]

    # Merge ranges
    for r in ranges[1:]:
        if ranges_merged[-1].upper >= r.lower:
            ranges_merged[-1].upper = max(ranges_merged[-1].upper, r.upper)
        else:
            ranges_merged.append(copy.copy(r))

    ranges = ranges_merged

    for product in products:
        for r in ranges:
            if r.lower <= product <= r.upper:
                result += 1
                break

    return result


# Yay, got a part2 for free today!
# I was already merging ranges :)
def part2(input: list[str]) -> int:
    result: int = 0

    in_ranges = True
    ranges: list[Range] = []
    products: list[int] = []

    # Input parsing
    for line in input:
        if line == "":
            in_ranges = False
            continue
        if in_ranges:
            line_parsed = list(map(int, line.split("-")))
            ranges.append(Range(line_parsed[0], line_parsed[1]))
        else:
            products.append(int(line))

    ranges = sorted(ranges, key=lambda r: r.lower)
    ranges_merged: list[Range] = [copy.copy(ranges[0])]

    # Merge ranges
    for r in ranges[1:]:
        if ranges_merged[-1].upper >= r.lower:
            ranges_merged[-1].upper = max(ranges_merged[-1].upper, r.upper)
        else:
            ranges_merged.append(copy.copy(r))

    ranges = ranges_merged

    for r in ranges:
        result += r.upper - r.lower + 1

    return result


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

    with (
        open("./data/day05-example.txt", "r", encoding="utf-8") as example,
        open("./data/day05-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines = []
        for row in input.readlines():
            input_lines.append(row.replace("\n", ""))

        if run_part1[0]:
            print("-> Running part 1")
            print("   > Example")
            out1_e = part1(example_lines)
            if run_part1[1]:
                print("   > Input")
                out1_i = part1(input_lines)

        if run_part2[0]:
            example.seek(0, io.SEEK_SET)
            input.seek(0, io.SEEK_SET)

            print("-> Running part 2")
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
