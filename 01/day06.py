import io


def part1(input: list[str]) -> int:
    result: int = 0
    symbol_index = 0
    
    # Find row with mathmatical symbols
    for i, line in enumerate(input):
        if line[0] == "*" or line[0] == "+":
            symbol_index = i
    
    symbol_line = input[symbol_index]
    input_parsed = [x.split() for x in input[0:symbol_index]]
    
    for i, char in enumerate(symbol_line.split()):
        if char == " ":
            continue
        
        # Gather integers
        ints = []
        for j in range(len(input_parsed)):
            ints.append(int(input_parsed[j][i]))
        
        print(ints)
        
        # Do calculations
        calc_result = ints[0]
        match char:
            case "*":
                for num in ints[1:]:
                    calc_result *= num
            case "+":
                for num in ints[1:]:
                    calc_result += num
        result += calc_result

    return result


def part2(input: list[str]) -> int:
    result: int = 0
    
    operation = ""
    numbers = []
    
    for i in range(len(input[0]) - 1, -1, -1):
        number = ""
        
        for j in range(0, len(input)):
            char = input[j][i]
            if char == "*" or char == "+":
                operation = char
                break
            else:
                number += char
        
        if len(number.strip()) != 0:
            numbers.append(int(number))
        else:
            continue
        
        match operation:
            case "*":
                operation = ""
                calc = numbers[0]
                for num in numbers[1:]:
                    calc *= num
                result += calc
                numbers = []
            case "+":
                operation = ""
                calc = numbers[0]
                for num in numbers[1:]:
                    calc += num
                result += calc
                numbers = []
            case "":
                pass
            

    return result


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

    with (
        open("./data/day06-example.txt", "r", encoding="utf-8") as example,
        open("./data/day06-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines = []
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
