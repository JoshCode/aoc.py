import io
from dataclasses import dataclass


@dataclass
class Unit:
    value: int = 0

@dataclass
class Start:
    value: int = 0

@dataclass
class Splitter:
    value: int = 0


Cell = Start | Splitter | Unit


def part1(input: list[str]) -> int:
    result: int = 0

    grid: list[list[Cell]] = []

    # Parse input
    for line in input:
        grid_row: list[Cell] = []
        for char in line:
            match char:
                case ".":
                    grid_row.append(Unit())
                case "^":
                    grid_row.append(Splitter())
                case "S":
                    grid_row.append(Start())
        grid.append(grid_row)

    # Find start, start beam below
    for i, cell in enumerate(grid[0]):
        if type(cell) is Start:
            grid[1][i].value = 1
            break

    for i, row in enumerate(grid[1:]):
        # Don't run for the last line (avoid OoB)
        if i == len(grid) - 1:
            break

        for j, cell in enumerate(grid[i]):
            # If beam is present
            if cell.value > 0:
                cell_below = grid[i + 1][j]
                # If cell below is empty, pass on the beam
                if type(cell_below) is Unit:
                    cell_below.value += cell.value
                # If cell below is splitter, split the beam
                if type(cell_below) is Splitter:
                    cell_below_left = grid[i + 1][j - 1]
                    cell_below_right = grid[i + 1][j + 1]
                    cell_below_left.value += cell.value
                    cell_below_right.value += cell.value
                    result += 1

    print(render_grid(grid))

    return result


def part2(input: list[str]) -> int:
    result: int = 0

    grid: list[list[Cell]] = []

    # Parse input
    for line in input:
        grid_row: list[Cell] = []
        for char in line:
            match char:
                case ".":
                    grid_row.append(Unit())
                case "^":
                    grid_row.append(Splitter())
                case "S":
                    grid_row.append(Start())
        grid.append(grid_row)

    # Find start, start beam below
    for i, cell in enumerate(grid[0]):
        if type(cell) is Start:
            grid[1][i].value = 1
            break

    for i, row in enumerate(grid[1:]):
        # Don't run for the last line (avoid OoB)
        if i == len(grid) - 1:
            break

        for j, cell in enumerate(grid[i]):
            # If beam is present
            if cell.value > 0:
                cell_below = grid[i + 1][j]
                # If cell below is empty, pass on the beam
                if type(cell_below) is Unit:
                    cell_below.value += cell.value
                # If cell below is splitter, split the beam
                if type(cell_below) is Splitter:
                    cell_below_left = grid[i + 1][j - 1]
                    cell_below_right = grid[i + 1][j + 1]
                    cell_below_left.value += cell.value
                    cell_below_right.value += cell.value

    for cell in grid[-1]:
        result += cell.value

    print(render_grid(grid))

    return result


def render_grid(grid: list[list[Cell]]) -> str:
    result_str: str = ""
    for row in grid:
        for cell in row:
            match cell:
                case Unit(value):
                    if value > 0:
                        result_str += "|"
                    else:
                        result_str += "."
                case Splitter():
                    result_str += "^"
                case Start():
                    result_str += "S"

        result_str += "\n"
    return result_str


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

    with (
        open("./data/day07-example.txt", "r", encoding="utf-8") as example,
        open("./data/day07-input.txt", "r", encoding="utf-8") as input,
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
