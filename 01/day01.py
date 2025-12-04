import math
import io


def main():
    with (
        open("./data/day01-example.txt", "r", encoding="utf-8") as example,
        open("./data/day01-input.txt", "r", encoding="utf-8") as input,
    ):
        print("-> Running part 1")
        out1_e = part1(example.readlines())
        out1_i = part1(input.readlines())

        example.seek(0, io.SEEK_SET)
        input.seek(0, io.SEEK_SET)

        print("-> Running part 2")
        out2_e = part2(example.readlines())
        out2_i = part2(input.readlines())

        example.seek(0, io.SEEK_SET)
        input.seek(0, io.SEEK_SET)

        print("-> Running part 2 alternate")
        out2a_e = part2_alt(example.readlines())
        out2a_i = part2_alt(input.readlines())

        print("")
        print(f"{out1_e=}")
        print(f"{out1_i=}")
        print(f"{out2_e=}")
        print(f"{out2_i=}")
        print(f"{out2a_e=}")
        print(f"{out2a_i=}")


def part1(input: list[str]) -> int:
    position: int = 50
    password: int = 0

    for line in input:
        direction: int = 0
        match line[0]:
            case "L":
                direction = -1
            case "R":
                direction = 1

        amount: int = int(line[1:])
        position += amount * direction

        while position < 0 or position > 99:
            if position > 99:
                position -= 100
            if position < 0:
                position += 100

        if position == 0:
            password += 1

    return password


def part2(input: list[str]) -> int:
    position: int = 50
    password: int = 0

    for line in input:
        old_position = position
        direction: int = 0
        match line[0]:
            case "L":
                direction = -1
            case "R":
                direction = 1

        amount: int = int(line[1:])
        position += amount * direction
        factor = math.floor(position / 100)
        position = position + (-1 * factor * 100)
        password += abs(factor)

        if old_position == 0 and abs(factor) > 0:
            password -= 1

        if position == 0 and factor == 0:
            password += 1

    return password


def part2_alt(input: list[str]) -> int:
    # TODO: This is mega dirty and I am very unhappy with it
    # This should be do-able without the second loop and with a formula, right?
    position: int = 50
    password: int = 0
    total = 0

    for line in input:
        old_position = position
        direction: int = 0
        match line[0]:
            case "L":
                direction = -1
            case "R":
                direction = 1

        amount: int = int(line[1:])
        total += abs(amount)

        while amount > 0:
            position += direction
            amount -= 1

            if position < 0:
                position = 99
            elif position > 99:
                position = 0

            if position == 0:
                password += 1

    print(f"totaal = {total}")

    return password


if __name__ == "__main__":
    main()
