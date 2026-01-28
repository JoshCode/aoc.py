from dataclasses import dataclass
from functools import reduce
import re
import math

@dataclass
class Shape:
    id: int
    filled_count: int
    shape: list[str]

@dataclass
class Rect:
    dim1: int
    dim2: int
    counts: list[int]

def part1(input: list[str]) -> int:
    result: int = 0

    shapes: list[Shape] = []
    rects: list[Rect] = []

    parsing_shapes = True
    in_shape = False
    
    shape_id: int = None
    shape_str: list[str] = []

    re_shape_id = re.compile(r"^\d+:$")

    for line in input:
        if parsing_shapes:
            if in_shape:
                if len(line) == 0:
                    count = reduce(lambda sum, s: sum + s.count("#"), shape_str, 0)
                    shapes.append(Shape(shape_id, count, shape_str))
                    shape_id = None
                    shape_str = []
                    in_shape = False
                    continue
                else:
                    shape_str.append(line)
                    continue
            else:
                # Check if line is a new shape or the start of rectangles
                if re_shape_id.match(line) is not None:
                    shape_id = int(line[0:-1])
                    in_shape = True
                    continue
                else:
                    parsing_shapes = False
        
        # Not parsing shapes
        parts = line.split(":")
        dims = list(map(lambda x: int(x), parts[0].split("x")))
        counts = list(map(lambda x: int(x), parts[1].split()))
        rects.append(Rect(dims[0], dims[1], counts))

    pass

    for rect in rects:
        size = rect.dim1 * rect.dim2

        shape_filled_total = 0
        shape_count = 0
        for i, shape in enumerate(shapes):
            shape_count += rect.counts[i]
            shape_filled_total += rect.counts[i] * shape.filled_count
        pass

        max_3x3_in_rect = math.floor(rect.dim1 / 3) * math.floor(rect.dim2 / 3)

        if size < shape_filled_total:
            print("Can't fit: not enough squares")
            continue
        elif max_3x3_in_rect > shape_count:
            print("Fits: all in 3x3 areas")
            result += 1
        else:
            print("Ambiguous!")

    return result


def part2(input: list[str]) -> int:
    result: int = 0


    return result


# region Input file handling
def main():
    import io
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True, True)
    run_part2 = (False, False, True)
    input_path = Path.relative_to = Path(__file__).parent

    with (
        open(input_path / "data/day12-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day12-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines = []
        for row in input.readlines():
            input_lines.append(row.replace("\n", ""))

        if run_part1[0]:
            print("-> Running part 1")
            if run_part1[1]:
                print("   > Example")
                out1_e = part1(example_lines)
            if run_part1[2]:
                print("   > Input")
                out1_i = part1(input_lines)

        if run_part2[0]:
            example.seek(0, io.SEEK_SET)
            input.seek(0, io.SEEK_SET)

            print("-> Running part 2")
            if run_part2[1]:
                print("   > Example")
                out2_e = part2(example_lines)
            if run_part2[2]:
                print("   > Input")
                out2_i = part2(input_lines)

        print("")
        if run_part1[0]:
            if run_part1[1]:
                print(f"{out1_e=}")
            if run_part1[2]:
                print(f"{out1_i=}")
        if run_part2[0]:
            if run_part2[1]:
                print(f"{out2_e=}")
            if run_part2[2]:
                print(f"{out2_i=}")


if __name__ == "__main__":
    main()
# endregion
