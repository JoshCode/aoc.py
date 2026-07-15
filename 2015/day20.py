from math import log
from typing import Any


def part1(input: list[str]) -> Any:
    result: int = 0

    presents_target: int = int(input[0])

    primes = gen_primes()
    hcn = gen_hcn(primes)

    max_index = 0
    for index, (id, _, _) in enumerate(hcn):
        presents = 0
        # Optimisation: do not check the entire range.
        # A number is always divisible by itself, and never divisible by any number between (itself/2) + 1 and itself
        # TODO This is very similar to finding primes, consider reading up on sieves
        for elf_id in range(1, int(id / 2) + 1):
            if id % elf_id == 0:
                presents += elf_id * 10
        presents += id * 10
        print(f"House {id} got {presents} presents.")
        if presents >= presents_target:
            max_index = index
            break

    # Slow search between prev_id and id
    lb = hcn[max_index - 1][0]
    ub = hcn[max_index][0]
    # print(f"Slow searching between houses {lb} and {ub}")
    # for id in range(lb, ub + 1, 2):
    #     print(id)
    #     presents = 0
    #     # Optimisation: do not check the entire range.
    #     # A number is always divisible by itself, and never divisible by any number between (itself/2) + 1 and itself
    #     # TODO This is very similar to finding primes, consider reading up on sieves
    #     for elf_id in range(1, int(id / 2) + 1):
    #         if id % elf_id == 0:
    #             presents += elf_id * 10
    #     presents += id * 10

    houses = [0 for _ in range(ub + 1)]
    houses[0] = 0

    print("Delivering presents to houses")

    for i in range(1, ub + 1):
        for j in range(i, ub + 1, i):
            houses[j] += 10 * i

    print("Searching for target house")

    for house_idx, house_presents_total in enumerate(houses):
        if house_presents_total >= presents_target:
            result = house_idx
            break
    pass
    return result


# Generates a list of the first primes (with product > max_n).
def gen_primes(max_n: int = 10**18) -> list[int]:
    primes: list[int] = []
    primes_product = 1
    for n in range(2, 10**10):
        is_prime = True
        for i in range(2, n):
            if n % i == 0:
                is_prime = False
        if is_prime:
            primes.append(n)
            primes_product *= n
            if primes_product > max_n:
                break
    return primes


# Generates a list of the hcn <= max_n.
def gen_hcn(primes: list[int], max_n: int = 10**18) -> list[tuple[int, int, list[int]]]:
    # List of (number, number of divisors, exponents of the factorization)
    hcn: list[tuple[int, int, list[int]]] = [(1, 1, [])]
    for i in range(len(primes)):
        new_hcn: list[tuple[int, int, list[int]]] = []
        for el in hcn:
            new_hcn.append(el)
            if len(el[2]) < i:
                continue
            e_max = el[2][i - 1] if i >= 1 else int(log(max_n, 2))
            n = el[0]
            for e in range(1, e_max + 1):
                n *= primes[i]
                if n > max_n:
                    break
                div = el[1] * (e + 1)
                exponents = el[2] + [e]
                new_hcn.append((n, div, exponents))
        new_hcn.sort()
        hcn = [(1, 1, [])]
        for el in new_hcn:
            if el[1] >= hcn[-1][1]:
                hcn.append(el)
    new_hcn: list[tuple[int, int, list[int]]] = [(1, 1, [])]
    for el in hcn:
        if el[0] != new_hcn[-1][0]:
            new_hcn.append(el)
    hcn = new_hcn
    return hcn


def part2(input: list[str]) -> Any:
    result: int = 0

    presents_target: int = int(input[0])

    primes = gen_primes()
    hcn = gen_hcn(primes)

    # Calculate upper bound
    # This is actually wrong for part 2 (doesn't take into account max houses per elf)
    # But it got the correct answer, so ¯\(°_o)/¯
    # TODO Correct upper bound
    max_index = 0
    for index, (id, _, _) in enumerate(hcn):
        presents = 0
        for elf_id in range(1, int(id / 2) + 1):
            if id % elf_id == 0:
                presents += elf_id * 10
        presents += id * 10
        print(f"House {id} got {presents} presents.")
        if presents >= presents_target:
            max_index = index
            break

    ub = hcn[max_index][0]

    houses = [0 for _ in range(ub + 1)]

    print("Delivering presents to houses")
    house_count = 0
    for i in range(1, ub + 1):
        house_count = 0
        for j in range(i, ub + 1, i):
            houses[j] += 11 * i
            house_count += 1
            if house_count == 50:
                break

    print("Searching for target house")

    for house_idx, house_presents_total in enumerate(houses):
        if house_presents_total >= presents_target:
            result = house_idx
            break
    pass
    return result


# region Input file handling
def main():
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True)
    run_part2 = (True, True)

    global is_example
    is_example = False

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
                is_example = True
                out1_e = part1(example_lines)
            if run_part1[1]:
                print("   > Input")
                is_example = False
                out1_i = part1(input_lines)

        if any(run_part2):
            print("-> Running part 2")
            if run_part2[0]:
                print("   > Example")
                is_example = True
                out2_e = part2(example_lines)
            if run_part2[1]:
                print("   > Input")
                is_example = False
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
