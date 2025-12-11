import io
from dataclasses import dataclass, field
from copy import copy


@dataclass
class Node:
    id: str
    edges: set["Node"]

    def __hash__(self):
        return hash(str)
    
    def __repr__(self):
        return self.id
    
    def __eq__(self, value):
        return self.id == value.id


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=lambda: dict())
    start: Node = None
    end: Node = None


@dataclass
class Path:
    nodes: list[Node]
    visited: set[Node]


def part1(input: list[str]) -> int:
    result: int = 0

    graph = Graph()
    nodes: dict[str, Node] = {}

    nodes["out"] = Node("out", set())
    graph.end = nodes["out"]

    for line in input:
        line = line.split(":")
        id = line[0]
        nodes[id] = Node(id, set())
        if id == "you":
            graph.start = nodes[id]

    for line in input:
        line = line.split(":")
        id = line[0]
        for edge in line[1].split():
            nodes[id].edges.add(nodes[edge])

    graph.nodes = set(nodes.values())
    del line, id, edge

    # Search the graph
    paths: list[Path] = [Path(nodes=[graph.start], visited=set([graph.start]))]
    full_paths: list[Path] = []
    
    
    while len(paths) > 0:
        new_paths: list[Path] = []
        print(len(paths))
        for path in paths:
            # print(path.nodes)
            possible_nodes = path.nodes[-1].edges
            for node in possible_nodes:
                if node not in path.visited:
                    new_path = Path(copy(path.nodes), copy(path.visited))
                    new_path.nodes.append(node)
                    new_path.visited.add(node)
                    if node == graph.end:
                        result += 1
                        full_paths.append(new_path)
                    else:
                        new_paths.append(new_path)
        paths = new_paths
    
    if len(nodes) > 20:
        for path in full_paths:
            if nodes['svr'] in path.nodes:
                print("Yes")

    return result


def part2(input: list[str]) -> int:
    result: int = 0

    graph = Graph()
    nodes: dict[str, Node] = {}

    nodes["out"] = Node("out", set())
    graph.end = nodes["out"]

    for line in input:
        line = line.split(":")
        id = line[0]
        nodes[id] = Node(id, set())
        if id == "svr":
            graph.start = nodes[id]

    for line in input:
        line = line.split(":")
        id = line[0]
        for edge in line[1].split():
            nodes[id].edges.add(nodes[edge])

    graph.nodes = set(nodes.values())
    del line, id, edge

    # Search the graph
    paths: list[Path] = [Path(nodes=[graph.start], visited=set([graph.start.id]))]
    full_paths: list[Path] = []
    
    
    while len(paths) > 0:
        new_paths: list[Path] = []
        for path in paths:
            # print(path.nodes)
            possible_nodes = path.nodes[-1].edges
            for node in possible_nodes:
                if node.id == "svr":
                    print("svr")
                if node.id not in path.visited:
                    new_path = Path(copy(path.nodes), copy(path.visited))
                    new_path.nodes.append(node)
                    new_path.visited.add(node.id)
                    if node == graph.end:
                        result += 1
                        full_paths.append(new_path)
                    else:
                        new_paths.append(new_path)
        paths = new_paths
        print(f"Exploring: {len(paths)}, found: {len(full_paths)}")

    valid_paths = []
    for path in full_paths:
        if nodes["fft"] in path.nodes and nodes["dac"] in path.nodes:
            valid_paths.append(path)
    result = len(valid_paths)

    return result


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (False, True, True)
    run_part2 = (True, False, True)

    with (
        open("./data/day11-example.txt", "r", encoding="utf-8") as example,
        open("./data/day11-example_2.txt", "r", encoding="utf-8") as example2,
        open("./data/day11-input.txt", "r", encoding="utf-8") as input,
    ):
        example_lines = []
        for row in example.readlines():
            example_lines.append(row.replace("\n", ""))
        
        example_lines_2 = []
        for row in example2.readlines():
            example_lines_2.append(row.replace("\n", ""))

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
                out2_e = part2(example_lines_2)
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
