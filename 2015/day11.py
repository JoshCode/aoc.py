from typing import Any


def part1(input: list[str]) -> Any:
    password = input[0]

    while not check_password(password):
        password = increment_password(password)
        # print(password)

    return password


def part2(input: list[str]) -> Any:
    password = input[0]

    while not check_password(password):
        password = increment_password(password)
        # print(password)
    password = increment_password(password)
    while not check_password(password):
        password = increment_password(password)

    return password


def check_password(password: str) -> bool:
    # Check for straight
    contains_straight = False

    for i in range(0, len(password) - 2):
        if (
            ord(password[i + 1]) == ord(password[i]) + 1
            and ord(password[i + 2]) == ord(password[i + 1]) + 1
        ):
            contains_straight = True
            break

    if not contains_straight:
        return False

    # Check for invalid chars
    only_valid_chars = True

    for char in password:
        if char == "i" or char == "o" or char == "l":
            only_valid_chars = False
            break

    if not only_valid_chars:
        return False

    # Check for pairs
    has_two_pairs = False

    pair_coordinates: set[int] = set()
    valid_pairs: list[tuple[str, int]] = []
    for i in range(0, len(password) - 1):
        if password[i] == password[i + 1] and i not in pair_coordinates:
            pair_coordinates = pair_coordinates.union([i, i + 1])
            pair = (password[i : i + 2], i)
            valid_pairs.append(pair)

    if len(valid_pairs) > 1:
        has_two_pairs = True

    if not has_two_pairs:
        return False

    return True


def increment_password(password: str) -> str:
    password_b = bytearray(password, encoding="ascii")
    password_b[-1] += 1

    # Handle overflow
    for i in range(len(password_b) - 1, 0, -1):
        if password_b[i] > ord("z"):
            password_b[i] = ord("a")
            password_b[i - 1] += 1
    if password_b[0] > ord("z"):
        raise OverflowError("Password has overflowed")

    return password_b.decode("ascii")


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
