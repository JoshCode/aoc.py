from typing import Any

def part1(input: list[str]) -> Any:
    result: int = 0

    VOWELS = set("aeiou")
    NAUGHTY = set(["ab", "cd", "pq", "xy"])

    for line in input:
        char_window = "__"

        no_naughty_strings = True
        double_character = False
        vowel_count = 0

        for char in line:
            char_window = char_window[-1] + char
            
            if char_window in NAUGHTY:
                no_naughty_strings = False
                break

            if char_window[0] == char_window[1]:
                double_character = True

            if char in VOWELS:
                vowel_count += 1
        
        if vowel_count >= 3 and double_character and no_naughty_strings:
            print(f"'{line}' is nice")
            result += 1

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    for line in input:
        cond_pair = False
        cond_repeated = False

        pairs: dict[str, set[tuple[int, int]]] = {}

        for i in range(len(line)):
            pair = line[i:i+2]
            trio = line[i:i+3]

            if cond_pair and cond_repeated:
                break

            if len(pair) == 2 and not cond_pair:
                if pair in pairs:
                    for pair_location in pairs[pair]:
                        # Check if there is a pair that doesn't overlap with our current pair
                        if pair_location[1] != i:
                            cond_pair = True
                    pairs[pair].add((i, i+1))
                else:
                    pairs[pair] = {(i, i+1)}

            if len(trio) == 3 and not cond_repeated:
                if trio[0] == trio[2]:
                    cond_repeated = True

        if cond_pair and cond_repeated:
            print(f"'{line}' is nice")
            result += 1
    
    return result


# region Input file handling
def main():
    import io
    from pathlib import Path
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (False, True)
    run_part2 = (True, True)
    input_path = Path(__file__).parent

    with (
        open(input_path / "data/day05-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day05-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines: list[str] = []
        for row in example.readlines():
            example_lines.append(row.removesuffix("\n"))

        input_lines: list[str] = []
        for row in input.readlines():
            input_lines.append(row.removesuffix("\n"))

        out1_e = out1_i = out2_e = out2_i = None

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
