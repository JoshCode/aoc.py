import heapq
import re
from dataclasses import InitVar, dataclass, field
from typing import Any


def part1(input: list[str]) -> Any:
    result: int = 0

    substitutions, molecule = parse(input)

    # Compute possible strings
    possibilities: set[str] = all_substitutions(molecule, substitutions)

    result = len(possibilities)
    return result


# Needed help for the following insight:
# Every target group can only be produced by one source group.
# So, target molecule can only be deconstructed in one way.
def part2(input: list[str]) -> Any:
    result: int = 0

    source_groups, target_molecule = parse(input)
    target_groups: dict[str, str] = {}

    # Reverse the substitutions. Source -> Targets becomes Target -> Source.
    # Every Target only has one Source.
    for s, ts in source_groups.items():
        for t in ts:
            assert t not in target_groups
            target_groups[t] = s

    synthesis_stack: list[tuple[int, str]] = []
    current_molecule = target_molecule

    molecule_modified = True
    while molecule_modified:
        molecule_modified = False

        for tgt_grp, src_grp in target_groups.items():
            if src_grp == "e":
                continue

            # count how many matches of target first
            substitutions = current_molecule.count(tgt_grp)

            # then replace them all
            if substitutions > 0:
                current_molecule = current_molecule.replace(tgt_grp, src_grp)
                molecule_modified = True
                synthesis_stack.append((substitutions, current_molecule))

    pass

    # Last pass: find the target group that has source 'e' and replace it.
    for tgt_grp, src_grp in target_groups.items():
        if src_grp != "e":
            continue

        # count how many matches of target first
        substitutions = current_molecule.count(tgt_grp)

        # then replace them all
        if substitutions > 0:
            current_molecule = current_molecule.replace(tgt_grp, src_grp)
            molecule_modified = True
            synthesis_stack.append((substitutions, current_molecule))
            break

    result = sum(subs for subs, _ in synthesis_stack)

    return result


def all_substitutions(target_str: str, substitutions: dict[str, set[str]]) -> set[str]:
    result: set[str] = set()

    for sub in substitutions:
        regex = re.compile(f"{sub}")
        for match in regex.finditer(target_str):
            for replacement in substitutions[sub]:
                replaced_str: str = (
                    target_str[0 : match.start()]
                    + replacement
                    + target_str[match.end() :]
                )
                result.add(replaced_str)

    return result


def parse(input: list[str]) -> tuple[dict[str, set[str]], str]:
    substitutions: dict[str, set[str]] = {}
    molecule: str = ""

    for line in input:
        line_split = line.split(" => ")

        if len(line_split) > 1:
            left, right = line_split
            if left not in substitutions:
                substitutions[left] = set()

            substitutions[left].add(right)

        else:
            if len(line_split[0].strip()) == 0:
                continue
            molecule = line_split[0]

    return substitutions, molecule


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


# endregion


# region Madness
# +----+----+----+----+----+----+----+----+----+----+----+
# | DANGER: Below this line lies madness                 |
# +----+----+----+----+----+----+----+----+----+----+----+
@dataclass
class Atom:
    v: str

    def __hash__(self) -> int:
        return hash(self.v)

    def __str__(self) -> str:
        return self.v


@dataclass
class Molecule:
    v: tuple[Atom, ...]

    def replace_index(self, index: int, new: "Molecule") -> "Molecule":
        new_molecule = list(self.v)
        new_molecule = new_molecule[0:index] + list(new.v) + new_molecule[index + 1 :]
        return Molecule(tuple(new_molecule))

    def replace(self, old: Atom, new: "Molecule") -> "Molecule":
        new_molecule = list(self.v)
        for i, atom in enumerate(new_molecule):
            if atom == old:
                new_molecule = new_molecule[0:i] + list(new.v) + new_molecule[i + 1 :]
                return Molecule(tuple(new_molecule))

        return self

    def finditer_index(self, atom: Atom):
        for i, a in enumerate(self.v):
            if a == atom:
                yield i

    def __getitem__(self, key: int):
        return self.v[key]

    def __len__(self) -> int:
        return len(self.v)

    def __iter__(self):
        return iter(self.v)

    def __hash__(self) -> int:
        return hash(self.v)

    def __str__(self) -> str:
        return "".join(str(atom) for atom in self.v)

    def __repr__(self) -> str:
        return f"Molecule({str(self)})"


@dataclass(order=True)
class PriorityMolecule:
    priority: int = field(init=False)
    item: Molecule = field(compare=False)
    target: InitVar[Molecule]

    def __post_init__(self, target: Molecule):
        similarity = 0

        # Only calculate if we are the same length or shorter than target
        # Otherwise: similarity is 0
        if len(self.item) <= len(target):
            for i in range(len(target)):
                if i >= len(self.item):
                    break
                if self.item[i] == target[i]:
                    similarity += 1
                else:
                    break

        self.priority = similarity


def str_to_molecule(molecule_str: str) -> Molecule:
    current_atom = ""
    molecule_atoms: list[Atom] = []

    for char in molecule_str:
        if char.lower() == char:
            current_atom += char
            molecule_atoms.append(Atom(current_atom))
            current_atom = ""
        else:
            if len(current_atom) > 0:
                molecule_atoms.append(Atom(current_atom))
                current_atom = ""
            current_atom = char

    if len(current_atom) > 0:
        molecule_atoms.append(Atom(current_atom))
        current_atom = ""

    return Molecule(tuple(molecule_atoms))


def part1_old(input: list[str]) -> Any:
    result: int = 0

    substitutions, molecule = parse_molecule(input)

    # Compute possible strings
    possibilities: set[Molecule] = all_substitutions_molecule(molecule, substitutions)

    result = len(possibilities)
    return result


# Observations:
# - Substitutions can never make the molecule shorter
def part2_old2(input: list[str]) -> Any:
    result: int = 0

    substitutions, target_molecule = parse_molecule(input)
    distances: dict[Molecule, int] = {}

    start = str_to_molecule("e")
    search_space: set[Molecule] = {start}
    search_space_pq: list[PriorityMolecule] = []
    heapq.heappush_max(search_space_pq, PriorityMolecule(start, target_molecule))
    distances[start] = 0

    while True:
        current_molecule = heapq.heappop_max(search_space_pq)
        molecule = current_molecule.item
        # print(len(molecule))
        search_space.remove(molecule)

        new_molecules = all_substitutions_molecule(molecule, substitutions)
        for new_molecule in new_molecules:
            if new_molecule == target_molecule:
                return distances[molecule] + 1
            if len(new_molecule) > len(target_molecule):
                continue

            # Check if we have seen this before
            if new_molecule in distances:
                if distances[molecule] + 1 < distances[new_molecule]:
                    distances[new_molecule] = distances[molecule] + 1
                    if new_molecule not in search_space:
                        search_space.add(new_molecule)
                        heapq.heappush_max(
                            search_space_pq,
                            PriorityMolecule(new_molecule, target_molecule),
                        )
            else:
                distances[new_molecule] = distances[molecule] + 1
                if new_molecule not in search_space:
                    search_space.add(new_molecule)
                    heapq.heappush_max(
                        search_space_pq, PriorityMolecule(new_molecule, target_molecule)
                    )

    # Breadth-First
    # while True:
    #     new_search_space: set[Molecule] = set()

    #     for molecule in search_space:
    #         new_molecules = all_substitutions(molecule, substitutions)
    #         for new_molecule in new_molecules:
    #             if new_molecule == target_molecule:
    #                 return distances[molecule] + 1
    #             if len(new_molecule) > len(target_molecule):
    #                 continue

    #             # Check if we have seen this before
    #             if new_molecule in distances:
    #                 if distances[molecule] + 1 < distances[new_molecule]:
    #                     distances[new_molecule] = distances[molecule] + 1
    #                     new_search_space.add(new_molecule)
    #             else:
    #                 distances[new_molecule] = distances[molecule] + 1
    #                 new_search_space.add(new_molecule)

    #     search_space = new_search_space
    #     print(len(search_space))

    return result


def all_substitutions_molecule(
    target: Molecule, substitutions: dict[Atom, set[Molecule]]
) -> set[Molecule]:
    result: set[Molecule] = set()

    for sub in substitutions:
        for i in target.finditer_index(sub):
            for replacement in substitutions[sub]:
                new_molecule = target.replace_index(i, replacement)
                result.add(new_molecule)

    return result


def parse_molecule(input: list[str]) -> tuple[dict[Atom, set[Molecule]], Molecule]:
    substitutions: dict[Atom, set[Molecule]] = {}
    molecule: Molecule | None = None

    for line in input:
        line_split = line.split(" => ")

        if len(line_split) > 1:
            left, right = line_split
            left, right = Atom(left.strip()), str_to_molecule(right.strip())
            if left not in substitutions:
                substitutions[left] = set()

            substitutions[left].add(right)

        else:
            if len(line_split[0].strip()) == 0:
                continue
            molecule = str_to_molecule(line_split[0])

    if molecule is None:
        raise ValueError("No molecule found in input")

    return substitutions, molecule


# This algorithm should be turned around
# Do not find the target string from 'e', but explore the space back from target to 'e', trying to reduce as fast as possible
def part2_old(input: list[str]) -> Any:
    result: int = 0

    substitutions, molecule = parse(input)
    inverse_substitutions: dict[str, set[str]] = {}
    for k, v in substitutions.items():
        for item in v:
            if item not in inverse_substitutions:
                inverse_substitutions[item] = set()

            inverse_substitutions[item].add(k)

    substitutions = inverse_substitutions

    search_space: set[str] = set()
    distances: dict[str, int] = {}
    search_space.add(molecule)
    distances[molecule] = 0

    while True:
        if "e" in search_space:
            result = distances["e"]
            break

        new_distances: dict[str, int] = {}
        new_search_space: set[str] = set()
        first = True
        for s in search_space:
            # if first:
            #     print(s)
            #     print(len(s))
            #     first = False
            s_distance = distances[s]
            new_strs = all_substitutions_molecule(s, substitutions)
            for new_str in new_strs:
                if new_str not in new_search_space:
                    new_distances[new_str] = s_distance + 1
                    new_search_space.add(new_str)
                else:
                    new_distances[new_str] = min(new_distances[new_str], s_distance + 1)

        search_space = new_search_space
        distances = new_distances
        print(len(search_space))
        pass

    return result


if __name__ == "__main__":
    main()
# endregion
