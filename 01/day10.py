import io
from dataclasses import dataclass
from functools import reduce
from copy import copy
from itertools import combinations_with_replacement
import sys


@dataclass
class Button:
    value: set[int]


@dataclass
class JoltageSequence:
    seq: list[Button]
    state: list[int]


@dataclass
class Machine:
    desired_state: str
    button_sets: list[Button]
    desired_joltage: list[int]


def part1(input: list[str]) -> int:
    result: int = 0

    machines: list[Machine] = []

    for line in input:
        line = line.split()
        desired_state = line[0][1:-1]
        # print(desired_state)

        button_sets: list[Button] = []

        for button_str in line[1:-1]:
            button_str = button_str[1:-1]
            button_str = button_str.split(",")
            button_str = list(map(lambda x: int(x), button_str))
            button = Button(button_str)
            button_sets.append(button)

        joltage = (line[-1])[1:-1].split(",")
        joltage = list(map(lambda x: int(x), joltage))
        # print(joltage)

        machine = Machine(desired_state, button_sets, joltage)
        machines.append(machine)
        # print(machine)

    for i, machine in enumerate(machines):
        solution = solve_machine_indicators(machine)
        result += solution
        print(f"{i}/{len(machines)}")

    return result


def solve_machine_indicators(machine: Machine) -> int:
    combos: list[list[Button]] = [[]]
    while True:
        new_combos = []
        for combo in combos:
            for button_set in machine.button_sets:
                # Skip adding the same set if it's already the last set (we don't undo a press)
                if len(combo) > 0 and combo[-1] == button_set:
                    continue
                new_combo = copy(combo)
                new_combo.append(button_set)
                new_combos.append(new_combo)
        combos = new_combos

        for combo in combos:
            state = process_press_indicators(combo, len(machine.desired_state))
            if state == machine.desired_state:
                return len(combo)

        # print(len(combos))
        # if len(combos) > 6:
        #     return


def process_press_indicators(buttons: list[Button], length: int) -> str:
    state = reduce(lambda rest, x: rest + x, ["." for _ in range(length)], "")

    for button_set in buttons:
        button_set = button_set.value
        for button in button_set:
            if state[button] == ".":
                state = state[:button] + "#" + state[button + 1 :]
            else:
                state = state[:button] + "." + state[button + 1 :]

    return state


def process_press_joltage(buttons: list[Button], length: int) -> list[int]:
    state = [0 for _ in range(length)]

    for button_set in buttons:
        button_set = button_set.value
        for button in button_set:
            state[button] += 1

    return state


def part2(input: list[str]) -> int:
    result: int = 0

    machines: list[Machine] = []

    for line in input:
        line = line.split()
        desired_state = line[0][1:-1]
        # print(desired_state)

        button_sets: list[Button] = []

        for button_str in line[1:-1]:
            button_str = button_str[1:-1]
            button_str = button_str.split(",")
            button_str = list(map(lambda x: int(x), button_str))
            button = Button(button_str)
            button_sets.append(button)

        joltage = (line[-1])[1:-1].split(",")
        joltage = list(map(lambda x: int(x), joltage))
        # print(joltage)

        machine = Machine(desired_state, button_sets, joltage)
        machines.append(machine)
        # print(machine)

    for i, machine in enumerate(machines):
        current_state = [0 for _ in machine.desired_joltage]
        solution = solve_machine_joltage(machine.button_sets, [], current_state, machine.desired_joltage, None)
        result += solution
        print(f"{i + 1}/{len(machines)}: {solution}")

    return result


def solve_machine_joltage(button_set: list[Button], current_sequence: list[Button], current_state: list[int], desired_state: list[int], lowest_solution) -> int:
    # Strategy
    # Find lowest joltage counter, find all buttons that affect that counter. Find all combinations of those buttons of length == value of the counter
    # Now we have all combinations that set the lowest counter to the right value
    # Remove all those buttons from consideration: they can never be used again (they would increase a counter we don't want to increase anymore)
    # Calculate for all combinations their state
    # Find the next minimum delta joltage (the counter that needs the least increase in joltage), add all combinations of that delta length, remove buttons, etc.
    delta_state = copy(desired_state)
    for i, x in enumerate(current_state):
        delta_state[i] -= x
    
    # Find minimum (non-zero)
    ldj = max(delta_state) + 1
    ldj_index = None
    for i, x in enumerate(delta_state):
        if x > 0 and x < ldj:
            ldj = x
            ldj_index = i
    
    if ldj_index is None:
        return None
    
    # if len(solved_indices) > 0:
    #     print(f"Solved: {",".join(map(lambda x: str(x), solved_indices))} - solving: {ldj_index}")
    # else:
    #     print(f"Solving: {ldj_index}")
    
    buttons_for_current_index: list[Button] = []
    for button in button_set:
        if ldj_index in button.value:
            buttons_for_current_index.append(button)
    
    if len(buttons_for_current_index) == 0:
        return None
    combos = list(combinations_with_replacement(buttons_for_current_index, ldj))

    new_button_set = copy(button_set)
    for button in buttons_for_current_index:
        new_button_set.remove(button)
    
    # print(f"[{",".join(map(lambda x: str(x), solved_indices))}]-{{{ldj_index}}}: Checking {len(combos)} new combinations")
    for combo in combos:
        new_sequence = copy(current_sequence)
        new_sequence.extend(combo)
        if lowest_solution is not None and len(new_sequence) > lowest_solution:
            continue
        new_state = process_press_joltage(new_sequence, len(current_state))
        # print(new_sequence)
        # print(new_state)
        if new_state == desired_state:
            # print("Found!")
            return len(new_sequence)
        
        result = solve_machine_joltage(new_button_set, new_sequence, new_state, desired_state, lowest_solution)
        if result is not None:
            if lowest_solution is None:
                lowest_solution = result
            elif result < lowest_solution:
                lowest_solution = result


    return lowest_solution


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (False, True, True)
    run_part2 = (True, True, True)

    with (
        open("./data/day10-example.txt", "r", encoding="utf-8") as example,
        open("./data/day10-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))

        input_lines = []
        for row in input.readlines():
            input_lines.append(row.replace("\n", ""))

        if run_part1[0]:
            print("-> Running part 1")
            if run_part1[1]:
                print("   > Example")
                out1_e = part1(example_lines)
            if run_part1[2]:
                print("   > Input")
                out1_i = part1(input_lines)

        if run_part2[0]:
            example.seek(0, io.SEEK_SET)
            input.seek(0, io.SEEK_SET)

            print("-> Running part 2")
            if run_part2[1]:
                print("   > Example")
                out2_e = part2(example_lines)
            if run_part2[2]:
                print("   > Input")
                out2_i = part2(input_lines)

        print("")
        if run_part1[0]:
            if run_part1[1]:
                print(f"{out1_e=}")
            if run_part1[2]:
                print(f"{out1_i=}")
        if run_part2[0]:
            if run_part2[1]:
                print(f"{out2_e=}")
            if run_part2[2]:
                print(f"{out2_i=}")


if __name__ == "__main__":
    main()
# endregion
