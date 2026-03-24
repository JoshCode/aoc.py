from typing import Any
import re
import math


def part1(input: list[str]) -> Any:
    result: int = 0

    parse_re = re.compile(
        r"^(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<fly_time>\d+) seconds"
        r", but then must rest for (?P<rest_time>\d+) seconds.$"
    )

    reindeer_stats: dict[str, dict[str, int]] = {}

    for line in input:
        match = parse_re.match(line)
        if not match:
            continue
        name, speed, fly_time, rest_time = match.groups()

        if name not in reindeer_stats:
            reindeer_stats[name] = {}

        reindeer_stats[name]["speed"] = int(speed)
        reindeer_stats[name]["fly_time"] = int(fly_time)
        reindeer_stats[name]["rest_time"] = int(rest_time)

    RACE_TIME = 2503

    distances: dict[str, int] = {}

    for name in reindeer_stats:
        reindeer = reindeer_stats[name]
        speed, fly_time, rest_time = (
            reindeer["speed"],
            reindeer["fly_time"],
            reindeer["rest_time"],
        )
        completed_intervals = math.floor(RACE_TIME / (fly_time + rest_time))
        current_interval_time = RACE_TIME % (fly_time + rest_time)
        current_interval_flying_time = min(fly_time, current_interval_time)
        distance = (
            completed_intervals * speed * fly_time
            + current_interval_flying_time * speed
        )
        distances[name] = distance

    result = max(distances.values())

    return result


def part2(input: list[str]) -> Any:
    result: int = 0

    parse_re = re.compile(
        r"^(?P<name>\w+) can fly (?P<speed>\d+) km/s for (?P<fly_time>\d+) seconds"
        r", but then must rest for (?P<rest_time>\d+) seconds.$"
    )

    reindeer_stats: dict[str, dict[str, int]] = {}

    for line in input:
        match = parse_re.match(line)
        if not match:
            continue
        name, speed, fly_time, rest_time = match.groups()

        if name not in reindeer_stats:
            reindeer_stats[name] = {}

        reindeer_stats[name]["speed"] = int(speed)
        reindeer_stats[name]["fly_time"] = int(fly_time)
        reindeer_stats[name]["rest_time"] = int(rest_time)

    RACE_TIME = 2503
    distances: dict[str, int] = {}
    points: dict[str, int] = {}

    for name in reindeer_stats:
        distances[name] = 0
        points[name] = 0

    for time in range(1, RACE_TIME + 1):
        # Update distances
        for name in reindeer_stats:
            reindeer = reindeer_stats[name]
            speed, fly_time, rest_time = (
                reindeer["speed"],
                reindeer["fly_time"],
                reindeer["rest_time"],
            )

            current_interval_time = time % (fly_time + rest_time)
            if current_interval_time > 0 and current_interval_time <= fly_time:
                distances[name] += speed

        # print(f"After second {time}")
        # print(distances)
        max_distance = max(distances.values())

        for name in distances:
            if distances[name] == max_distance:
                points[name] += 1

    result = max(points.values())
    return result


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
