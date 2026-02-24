from typing import Any

def part1(input: list[str]) -> Any:
    result: int = 0

    for line in input:
        line_split = line.split("x")
        l, w, h = int(line_split[0]), int(line_split[1]), int(line_split[2])
        areas = surface_areas(l, w, h)
        wrapping_paper_area = min(areas) + sum(areas * 2)

        # print(wrapping_paper_area)
        result += wrapping_paper_area

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    for line in input:
        line_split = line.split("x")
        l, w, h = int(line_split[0]), int(line_split[1]), int(line_split[2])
        circs = circumferences(l, w, h)
        ribbon_length = min(circs) + (l * w * h)

        # print(ribbon_length)
        result += ribbon_length

    return result

def surface_areas(l: int, w: int, h: int) -> tuple[int, int, int]:
    return (l*w, w*h, h*l)


def circumferences(l: int, w: int, h: int) -> tuple[int, int, int]:
    return (2*(l+w), 2*(w+h), 2*(h+l))


# region Input file handling
def main():
    import io
    from pathlib import Path
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)
    input_path = Path(__file__).parent

    with (
        open(input_path / "data/day02-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day02-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines: list[str] = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines: list[str] = []
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
