from typing import Any
from re import match

def part1(input: list[str]) -> Any:
    result: int = 0

    wires: dict[str, int] = {}
    operations: list[tuple[str, str | int, str | int | None, str]] = parse(input)
    
    wires = interp(operations, wires)

    # Dump the wires to the console
    # for key, value in wires.items():
    #     print(f"{key}: {value}")

    if "a" in wires:
        result = wires["a"]

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    wires: dict[str, int] = {}
    operations: list[tuple[str, str | int, str | int | None, str]] = parse(input)
    
    wires = interp(operations, wires)

    a = 0
    if "a" in wires:
        a = wires["a"]
    wires = {"b": a}
    operations = [op for op in operations if op[3] != "b"]

    wires = interp(operations, wires)

    # Dump the wires to the console
    # for key, value in wires.items():
    #     print(f"{key}: {value}")
    
    if "a" in wires:
        result = wires["a"]

    return result


def parse(input: list[str]) -> list[tuple[str, str | int, str | int | None, str]]:
    re_NUMBER = r"^\d+$"
    re_WIRE = r"^[a-z]+$"
    re_AND = r"^(?P<in1>\w+)\sAND\s(?P<in2>\w+)$"
    re_OR = r"^(?P<in1>\w+)\sOR\s(?P<in2>\w+)$"
    re_LSHIFT = r"^(?P<in1>\w+)\sLSHIFT\s(?P<in2>\d+)$"
    re_RSHIFT = r"^(?P<in1>\w+)\sRSHIFT\s(?P<in2>\d+)$"
    re_NOT = r"^NOT\s(?P<in1>\w+)$"

    operations: list[tuple[str, str | int, str | int | None, str]] = []

    for line in input:
        left, right = line.split(" -> ")
        m = None
        if m := match(re_NUMBER, left):
            operations.append(("SET", int(m.group(0)), None, right))
        elif m := match(re_WIRE, left):
            operations.append(("SET", m.group(0), None, right))
        elif m := match(re_AND, left):
            in1 = m.group("in1")
            in2 = m.group("in2")
            in1 = int(in1) if in1.isdigit() else in1
            in2 = int(in2) if in2.isdigit() else in2
            operations.append(("AND", in1, in2, right))
        elif m := match(re_OR, left):
            in1 = m.group("in1")
            in2 = m.group("in2")
            in1 = int(in1) if in1.isdigit() else in1
            in2 = int(in2) if in2.isdigit() else in2
            operations.append(("OR", in1, in2, right))
        elif m := match(re_LSHIFT, left):
            in1 = m.group("in1")
            in2 = m.group("in2")
            in1 = int(in1) if in1.isdigit() else in1
            in2 = int(in2) if in2.isdigit() else in2
            operations.append(("LSHIFT", in1, in2, right))
        elif m := match(re_RSHIFT, left):
            in1 = m.group("in1")
            in2 = m.group("in2")
            in1 = int(in1) if in1.isdigit() else in1
            in2 = int(in2) if in2.isdigit() else in2
            operations.append(("RSHIFT", in1, in2, right))
        elif m := match(re_NOT, left):
            in1 = m.group("in1")
            in1 = int(in1) if in1.isdigit() else in1
            operations.append(("NOT", in1, None, right))
        else:
            raise ValueError(f"Invalid instruction: {line}")
    
    return operations


def interp(operations: list[tuple[str, str | int, str | int | None, str]], wires: dict[str, int]) -> dict[str, int]:
    operation_stack = operations.copy()
    
    while operation_stack:
        op, in1, in2, out = operation_stack.pop(0)

        if isinstance(in1, str):
            if in1 not in wires:
                operation_stack.append((op, in1, in2, out))
                continue
            else:
                in1 = wires[in1]
        
        if isinstance(in2, str):
            if in2 not in wires:
                operation_stack.append((op, in1, in2, out))
                continue
            else:
                in2 = wires[in2]

        match op:
            case "SET":
                wires[out] = in1
            case "AND":
                wires[out] = in1 & in2
            case "OR":
                wires[out] = in1 | in2
            case "LSHIFT":
                wires[out] = (in1 << in2) % 65536
            case "RSHIFT":
                wires[out] = (in1 >> in2) % 65536
            case "NOT":
                wires[out] = in1 ^ 0b1111_1111_1111_1111
            case _:
                raise ValueError(f"Invalid operation: {op}")
    
    return wires


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
