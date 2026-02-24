from typing import Any

def part1(input: list[str]) -> Any:
    result: int = 0
    
    for line in input:
        pos = [0, 0]
        deliveries: set[tuple[int, int]] = set()
        deliveries.add((pos[0], pos[1]))

        for dir in line:
            match dir:
                case ">":
                    pos[0] += 1
                case "<":
                    pos[0] -= 1
                case "^":
                    pos[1] += 1
                case "v":
                    pos[1] -= 1
                case _:
                    raise ValueError(f"Malformed input. Direction {dir} not valid.")
            
            deliveries.add((pos[0], pos[1]))
            # print(deliveries)
        
        num_deliveries = len(deliveries)
        result = num_deliveries
        # print(num_deliveries)
    


    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    for line in input:
        # print()
        santa_pos = [0, 0]
        robo_pos = [0, 0]
        deliveries: set[tuple[int, int]] = set()
        deliveries.add((0, 0))

        for i, dir in enumerate(line):
            pos: list[int]
            if i % 2 == 0:
                pos = santa_pos
            else:
                pos = robo_pos

            match dir:
                case ">":
                    pos[0] += 1
                case "<":
                    pos[0] -= 1
                case "^":
                    pos[1] += 1
                case "v":
                    pos[1] -= 1
                case _:
                    raise ValueError(f"Malformed input. Direction {dir} not valid.")
            
            # print(pos)
            deliveries.add((pos[0], pos[1]))
            if i % 2 == 0:
                santa_pos = pos
            else:
                robo_pos = pos
            # print(deliveries)
        
        num_deliveries = len(deliveries)
        result = num_deliveries
        # print(num_deliveries)
    


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
        open(input_path / "data/day03-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day03-input.txt", "r", encoding="utf-8") as input,
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
