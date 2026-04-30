from typing import Any


def part1(input: list[str]) -> Any:
    result: int = 0

    grid: list[list[str]] = []

    for row in input:
        grid.append(list(row))

    # print("Initial state:")
    # print(count_cells(grid))
    # print(grid_to_str(grid))
    # print()

    for step in range(100):
        old_grid = [row.copy() for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] = update_cell(old_grid, j, i)
        # print(f"After {step + 1} steps:")
        # print(count_cells(grid))
        # print(grid_to_str(grid))
        # print()

    result = count_cells(grid)
    return result


def count_cells(grid: list[list[str]]) -> int:
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "#":
                result += 1
    return result


def grid_to_str(grid: list[list[str]]) -> str:
    rows: list[str] = []
    for row in grid:
        rows.append("".join(row))
    return "\n".join(rows)


def update_cell(grid: list[list[str]], x: int, y: int) -> str:
    current_state = grid[y][x]

    neighbours = 0

    mods = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for mod in mods:
        x_mod = x + mod[0]
        y_mod = y + mod[1]
        if x_mod >= 0 and x_mod < len(grid) and y_mod >= 0 and y_mod < len(grid[0]):
            if grid[y_mod][x_mod] == "#":
                neighbours += 1

    if current_state == "#" and neighbours in {2, 3}:
        return "#"
    elif current_state == "." and neighbours == 3:
        return "#"
    else:
        return "."


def part2(input: list[str]) -> Any:
    result: int = 0

    grid: list[list[str]] = []

    for row in input:
        grid.append(list(row))

    # Make corners always on
    grid[0][0] = "#"
    grid[0][len(grid[0]) - 1] = "#"
    grid[len(grid) - 1][0] = "#"
    grid[len(grid) - 1][len(grid[0]) - 1] = "#"

    # print("Initial state:")
    # print(count_cells(grid))
    # print(grid_to_str(grid))
    # print()

    for step in range(100):
        old_grid = [row.copy() for row in grid]
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (
                    (i == 0 and j == 0)
                    or (i == 0 and j == len(grid[i]) - 1)
                    or (i == len(grid) - 1 and j == 0)
                    or (i == len(grid) - 1 and j == len(grid[i]) - 1)
                ):
                    pass
                else:
                    grid[i][j] = update_cell(old_grid, j, i)
        # print(f"After {step + 1} steps:")
        # print(count_cells(grid))
        # print(grid_to_str(grid))
        # print()

    result = count_cells(grid)
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
