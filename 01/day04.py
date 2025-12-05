import io
import itertools


def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (False, True)
    run_part2 = (True, True)

    with (
        open("./data/day04-example.txt", "r", encoding="utf-8") as example,
        open("./data/day04-input.txt", "r", encoding="utf-8") as input,
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
            out1_e = part1(example_lines)[0]
            if run_part1[1]:
                print("   > Input")
                out1_i = part1(input_lines)[0]

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


def part1(input: list[str]) -> tuple[int, list[str]]:
    result: int = 0
    width = len(input[0])
    height = len(input)

    # Init two grids that are 2 wider and higher than the original input
    # This is so we can easily take a 3x3 window over the original input without worrying about out-of-bounds conditions
    input_grid: list[list[int]] = [
        [0 for _ in range(width + 2)] for _ in range(height + 2)
    ]
    output_grid: list[list[int]] = [
        [0 for _ in range(width + 2)] for _ in range(height + 2)
    ]

    # Set all spaces with a paper roll to 0
    # 0 meaning: not a free space
    for i, row in enumerate(input):
        for j, item in enumerate(row):
            if item == "@":
                input_grid[i + 1][j + 1] = 1

    for i, row in enumerate(input_grid):
        if i == 0 or i == len(input_grid) - 1:
            continue
        for j, _ in enumerate(row):
            if j == 0 or j == len(row) - 1:
                continue
            count = 0
            offsets = itertools.product([-1, 0, 1], [-1, 0, 1])
            for offset in offsets:
                if offset[0] == 0 and offset[1] == 0:
                    continue
                i_off = i + offset[0]
                j_off = j + offset[1]
                # Clamp offset indices
                # i_off = max(0, min(i_off, len(input_grid)-1))
                # j_off = max(0, min(j_off, len(row)-1))
                count += input_grid[i_off][j_off]
            output_grid[i][j] = count

    # print(render_grid(input_grid))
    # print(render_grid(output_grid))

    result_grid = []

    for i, row in enumerate(input):
        row_str = ""
        for j, item in enumerate(row):
            if item == "@" and output_grid[i + 1][j + 1] < 4:
                row_str += "x"
                result += 1
            else:
                row_str += item
        result_grid.append(row_str)

    return (result, result_grid)


def part2(input: list[str]) -> int:
    result: int = 0
    removed: int = None

    new_input: list[str] = input
    # print(len(new_input))
    # for row in new_input:
    #     print(row)
    # print(new_input[len(new_input) - 1])
    # print(len(new_input[0]))
    # print(len(new_input[len(new_input) - 1]))
    # return

    while removed != 0:
        (removed, new_input) = part1(new_input)
        result += removed

        # print("Received")
        # print(render_grid(new_input))

        # Clear removed rows from input
        for i in range(len(new_input)):
            new_input[i] = new_input[i].replace("x", ".")

        # print("Processed")
        # print(render_grid(new_input))

        print(f"Removed: {removed} - Result: {result}")

        # if removed == 0:
        # print(render_grid(new_input))

    return result


def render_grid(grid) -> str:
    result = ""
    for row in grid:
        for item in row:
            result += f"{item}"
        result = result[-1:]
        result += "\n"
    return result


if __name__ == "__main__":
    main()
