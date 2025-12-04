import io
import re


def main():
    with (
        open("./data/day03-example.txt", "r", encoding="utf-8") as example,
        open("./data/day03-input.txt", "r", encoding="utf-8") as input,
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
    result: int = 0

    for bank in input:
        num1 = bank[0]
        num2 = bank[1]
        max_num = int(bank[0] + bank[1])

        for num3 in bank[2:]:
            if int(num2 + num3) > max_num:
                num1 = num2
                num2 = num3
            elif int(num1 + num3) > max_num:
                num2 = num3
            max_num = int(num1+num2)
        
        print(max_num)
        result += max_num

    return result


def part2(input: list[str]) -> int:
    result: int = 0

# TODO: Thinking about implementing this in a way where we consider dropping each digit from the number
# starting leftmost with the new digit added to the back

# TODO: Idea for alternate: just append the new character,
# then iterate through string,
# dropping a digit if it is less than the next digit
# (so the greater digit shifts left)
# Note: if none found, then the new digit is dropped again

    for bank in input:
        num = bank[0:12]
        max_num = int(num)

        for next_digit in bank[12:]:
            for i in range(0, len(num)):
                cur_num = num[0:i] + num[i+1:] + next_digit
                # print(f"{num} : {cur_num}")
                # print(f"{"^":>{i}}")
                if int(cur_num) > max_num:
                    num = cur_num
                    max_num = int(num)
                    # print("Accepted:")
                    break
                # print()
        print(max_num)
        
        result += max_num

        

    return result


if __name__ == "__main__":
    main()
