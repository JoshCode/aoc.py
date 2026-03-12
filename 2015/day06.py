from typing import Any, Literal, Optional
import math
import re


def part1(input: list[str]) -> Any:
    result: int = 0

    light_grid = [[0 for _ in range(1000)] for _ in range(1000)]

    parse_pattern = re.compile(r"(?P<instr>turn off|turn on|toggle)\s(?P<c1>\d+,\d+)\sthrough\s(?P<c2>\d+,\d+)")

    for line in input:
        match = parse_pattern.match(line)
        if not match:
            continue
        values = match.groupdict()
        instr = values["instr"]
        c1 = values["c1"].split(",")
        c2 = values["c2"].split(",")
        c1 = (int(c1[0]), int(c1[1]))
        c2 = (int(c2[0]), int(c2[1]))
        

        match instr:
            case "turn on":
                part1_operate_light_grid(light_grid, c1, c2, value=1)
            case "turn off":
                part1_operate_light_grid(light_grid, c1, c2, value=0)
            case "toggle":
                part1_operate_light_grid(light_grid, c1, c2, value="toggle")
            case _:
                raise ValueError(f"Invalid instruction: {instr}")
            
        del instr, c1, c2

    for row in light_grid:
        for cell in row:
            result += cell

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    light_grid = [[0 for _ in range(1000)] for _ in range(1000)]

    parse_pattern = re.compile(r"(?P<instr>turn off|turn on|toggle)\s(?P<c1>\d+,\d+)\sthrough\s(?P<c2>\d+,\d+)")

    for line in input:
        match = parse_pattern.match(line)
        if not match:
            continue
        values = match.groupdict()
        instr = values["instr"]
        c1 = values["c1"].split(",")
        c2 = values["c2"].split(",")
        c1 = (int(c1[0]), int(c1[1]))
        c2 = (int(c2[0]), int(c2[1]))
        

        match instr:
            case "turn on":
                part2_operate_light_grid(light_grid, c1, c2, value=1)
            case "turn off":
                part2_operate_light_grid(light_grid, c1, c2, value=-1)
            case "toggle":
                part2_operate_light_grid(light_grid, c1, c2, value=2)
            case _:
                raise ValueError(f"Invalid instruction: {instr}")
            
        del instr, c1, c2

    for row in light_grid:
        for cell in row:
            result += cell

    return result


def part1_operate_light_grid(grid: list[list[int]],
                             c1: tuple[int, int],
                             c2: tuple[int, int],
                             value: int | Literal["toggle"]):
    for i in range(c1[0], c2[0] + 1):
        for j in range(c1[1], c2[1] + 1):
            match value:
                case "toggle":
                    grid[i][j] = (grid[i][j] + 1)%2
                case x:
                    grid[i][j] = x

def part2_operate_light_grid(grid: list[list[int]],
                             c1: tuple[int, int],
                             c2: tuple[int, int],
                             value: int):
    for i in range(c1[0], c2[0] + 1):
        for j in range(c1[1], c2[1] + 1):
            grid[i][j] = clamp(grid[i][j] + value, min=0)

def clamp(value: int, min: Optional[int] = None, max: Optional[int] = None) -> int:
    if min is not None and value < min:
        return min
    elif max is not None and value > max:
        return max
    else:
        return value


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
