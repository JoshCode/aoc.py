from typing import Any
from functools import reduce

def part1(input: list[str]) -> Any:
    result: int = 0
    line = input[0]

    def f(acc: int, x: str) -> int:
        match x:
            case "(":
                return acc + 1
            case ")":
                return acc - 1
            case _:
                raise ValueError(f"Malformed input. Character '{x}' not allowed")

    result = reduce(f, line, 0)

    return result


def part2(input: list[str]) -> Any:
    result: int = 0
    line = input[0]

    def f(acc: int, x: str) -> int:
        match x:
            case "(":
                return acc + 1
            case ")":
                return acc - 1
            case _:
                raise ValueError(f"Malformed input. Character '{x}' not allowed")

    acc = 0
    for i, x in enumerate(line):
        acc = f(acc, x)
        print(acc)
        if acc < 0:
            result = i + 1
            break
        
    return result


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
        open(input_path / "data/day01-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day01-input.txt", "r", encoding="utf-8") as input,
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
