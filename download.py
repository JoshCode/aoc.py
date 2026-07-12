import argparse
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(prog="AoC downloader")
    parser.add_argument("--path", required=True)
    parser.add_argument("--year", required=True)

    args = parser.parse_args()

    path = Path(args.path)
    year = args.year

    path.mkdir(parents=True, exist_ok=True)

    days = (
        [i for i in range(1, 26)] if year not in ["2025"] else [i for i in range(1, 13)]
    )

    for day in days:
        input_file = f"day{day:02}-input.txt"
        puzzle_file = f"day{day:02}.puzzle.md"

        input_file = (path / input_file).absolute()
        puzzle_file = (path / puzzle_file).absolute()

        # print(input_file)
        # print(puzzle_file)
        # continue

        if input_file.exists():
            print(f"{input_file} exists")
        else:
            subprocess.run(
                [
                    "aoc",
                    "download",
                    "--year",
                    year,
                    "--day",
                    str(day),
                    "--input-only",
                    "--input-file",
                    input_file,
                ]
            )
        if puzzle_file.exists():
            print(f"{puzzle_file} exists")
        else:
            subprocess.run(
                [
                    "aoc",
                    "download",
                    "--year",
                    year,
                    "--day",
                    str(day),
                    "--puzzle-only",
                    "--puzzle-file",
                    puzzle_file,
                ]
            )


if __name__ == "__main__":
    main()
