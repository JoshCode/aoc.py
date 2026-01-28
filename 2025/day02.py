import re


def main():
    import io
    from pathlib import Path
    input_path = Path.relative_to = Path(__file__).parent
    with (
        open(input_path / "data/day02-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day02-input.txt", "r", encoding="utf-8") as input,
    ):
        print("-> Running part 1")
        print("   > Example")
        out1_e = part1(example.readlines())
        print("   > Input")
        out1_i = part1(input.readlines())

        example.seek(0, io.SEEK_SET)
        input.seek(0, io.SEEK_SET)

        print("-> Running part 2")
        print("   > Example")
        out2_e = part2(example.readlines())
        print("   > Input")
        out2_i = part2(input.readlines())

        print("")
        print(f"{out1_e=}")
        print(f"{out1_i=}")
        print(f"{out2_e=}")
        print(f"{out2_i=}")


def part1(input: list[str]) -> int:
    input: str = input[0]
    result_list = []
    result: int = 0

    ranges = input.split(",")
    ranges = list(map(lambda x: x.split("-"), ranges))
    ranges = list(map(lambda x: [int(x[0]), int(x[1])], ranges))
    # input = list(map(lambda x: {'lower': x[0], 'upper': x[1]}, input))

    for r in ranges:
        # print(r)
        for i in range(r[0], r[1] + 1):
            i = str(i)
            if (len(i) % 2) == 0:
                i_1 = i[0 : int(len(i) / 2)]
                i_2 = i[int(len(i) / 2) :]
                if i_1 == i_2:
                    result_list.append(int(i))
                    result += int(i)

    return result


def part2(input: list[str]) -> int:
    input: str = input[0]
    result_list = []
    result: int = 0

    ranges = input.split(",")
    ranges = list(map(lambda x: x.split("-"), ranges))
    ranges = list(map(lambda x: [int(x[0]), int(x[1])], ranges))

    for r in ranges:
        # print(r)
        for i in range(r[0], r[1] + 1):
            i = str(i)

            for j in range(1, int(len(i) / 2) + 1):
                pattern = i[0:j]
                regex = re.compile(f"({pattern}){{2,}}")
                if regex.fullmatch(i) is not None:
                    print(i)
                    result_list.append(int(i))
                    result += int(i)
                    break

    return result


if __name__ == "__main__":
    main()
