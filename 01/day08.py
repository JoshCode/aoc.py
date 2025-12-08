import io
from dataclasses import dataclass, field
from heapq import heappush, heappop
from math import pow, sqrt, prod

@dataclass(order=True)
class Distance:
    d: int
    node1: 'Node'=field(compare=False)
    node2: 'Node'=field(compare=False)

    def __repr__(self):
        return f"{self.d}: {self.node1.id} - {self.node2.id}"

@dataclass
class Node:
    id: int
    x: int
    y: int
    z: int
    parent_graph: 'Graph'

    def __eq__(self, value):
        return self.id == value.id

    def __hash__(self):
        return hash(self.id)

@dataclass
class Edge:
    f: Node
    t: Node

@dataclass
class Graph:
    id: int
    nodes: list[Node]
    root: Node

    def __eq__(self, value):
        return self.id == value.id

def part1(input: list[str]) -> int:
    result: int = 0
    nodes: list[Node] = []
    
    for i, line in enumerate(input):
        line = line.split(",")
        nodes.append(Node(i, int(line[0]), int(line[1]), int(line[2]), None))
    
    graph_id: list[int] = [x for x in range(len(nodes))]
    nodes_in_graph = [[x.id] for x in nodes]
    distances: list[Distance] = []

    # Calculate distances
    for i, from_node in enumerate(nodes):
        # From a node to all nodes after it (prevent double distance calculations)
        for to_node in nodes[i+1:]:
            d = distance(from_node, to_node)
            heappush(distances, Distance(d, from_node, to_node))
    
    connection_attempts = 0
    max_connection_attempts = 0
    if len(nodes) == 20:
        max_connection_attempts = 10
    else:
        max_connection_attempts = 1000

    # Connect graphs
    while connection_attempts < max_connection_attempts and len(distances) > 0:
        d = heappop(distances)

        if graph_id[d.node1.id] != graph_id[d.node2.id]:
            root1 = graph_id[d.node1.id]
            root2 = graph_id[d.node2.id]
            
            for node in nodes_in_graph[root2]:
                nodes_in_graph[root1].append(node)
                graph_id[node] = root1
            
            nodes_in_graph[root2] = []


        connection_attempts += 1

    counts = {}
    for id in graph_id:
        if id in counts:
            counts[id] += 1
        else:
            counts[id] = 1
    
    # print(counts)
    result = sorted(list(counts.values()), reverse=True)[0:3]
    # print(result)
    result = prod(result)
    # print(result)
    return result

def part2(input: list[str]) -> int:
    result: int = 0
    nodes: list[Node] = []
    
    for i, line in enumerate(input):
        line = line.split(",")
        nodes.append(Node(i, int(line[0]), int(line[1]), int(line[2]), None))
    
    graph_id: list[int] = [x for x in range(len(nodes))]
    nodes_in_graph = [[x.id] for x in nodes]
    distances: list[Distance] = []

    # Calculate distances
    for i, from_node in enumerate(nodes):
        # From a node to all nodes after it (prevent double distance calculations)
        for to_node in nodes[i+1:]:
            d = distance(from_node, to_node)
            heappush(distances, Distance(d, from_node, to_node))

    # Connect graphs
    while len(distances) > 0:
        d = heappop(distances)

        if graph_id[d.node1.id] != graph_id[d.node2.id]:
            root1 = graph_id[d.node1.id]
            root2 = graph_id[d.node2.id]
            
            for node in nodes_in_graph[root2]:
                nodes_in_graph[root1].append(node)
                graph_id[node] = root1
            
            nodes_in_graph[root2] = []

            if len(nodes_in_graph[root1]) == len(nodes):
                print(d.node1)
                print(d.node2)
                result = d.node1.x * d.node2.x

    # counts = {}
    # for id in graph_id:
    #     if id in counts:
    #         counts[id] += 1
    #     else:
    #         counts[id] = 1
    
    # print(counts)
    # result = sorted(list(counts.values()), reverse=True)[0:3]
    # print(result)
    # result = prod(result)
    # print(result)
    return result


def distance(f: Node, t: Node) -> float:
    return sqrt(pow(f.x-t.x, 2) + pow(f.y-t.y, 2) + pow(f.z-t.z, 2))


# Shameful overcomplications
# def part1_2(input: list[str]) -> int:
#     # The problem asks us to connect points in 3D space, until 1000 points are connected.
#     # What is the size of the three largest graphs?
#     # I expect part2 to be something like MST + k-cut,
#     # so I will program in a way that will make that easy

#     result: int = 0
#     nodes: list[Node] = []
#     graphs: list[Graph] = []

#     for i, line in enumerate(input):
#         line = line.split(",")
#         nodes.append(Node(i, int(line[0]), int(line[1]), int(line[2]), None))

#     for i, node in enumerate(nodes):
#         graph = Graph(i, [node], node)

#         node.parent_graph = graph

#         graphs.append(graph)

#     print(len(graphs))
#     print(len(input))

#     connection_attempts = 0

#     distances: list[Distance] = []
#     heapify(distances)

#     # Calculate distances
#     for i, from_node in enumerate(nodes):
#         # From a node to all nodes after it (prevent double distance calculations)
#         for to_node in nodes[i+1:]:
#             d = distance(from_node, to_node)
#             heappush(distances, Distance(d, from_node, to_node))

#     print(f"{len(distances)=}")
#     max_connection_attempts = 0
#     if len(nodes) == 20:
#         max_connection_attempts = 10
#     else:
#         max_connection_attempts = 1000

#     # Connect graphs
#     while connection_attempts < max_connection_attempts and len(distances) > 0:
#         shortest = heappop(distances)

#         node1 = shortest.node1
#         node2 = shortest.node2

#         root1 = node1.parent_graph.root
#         root2 = node2.parent_graph.root

#         # Only connect if they are not already in the same graph
#         if root1 is not root2:
#             # for from_node in node2.parent_graph.edges:
#                 # for edge in node2.parent_graph.edges[from_node]:
#                     # node1.parent_graph.edges[from_node].append(edge)

#             root1.parent_graph.nodes.extend(root2.parent_graph.nodes)
#             root2.parent_graph.nodes = []
#             root2.parent_graph.root = root1.parent_graph.root

#         connection_attempts += 1

    
#     print(f"{connection_attempts=}")

#     # Find three biggest graphs
#     graphs_node_count = list(map(lambda x: (x.id, len(x.nodes)), graphs))
#     graphs_node_count = sorted(graphs_node_count, key=lambda x: x[1], reverse=True)
#     # print(graphs_node_count)
#     # print(f"Sanity sum: {sum(graphs_node_count)}")
#     result = graphs_node_count[0][1]
#     for x in graphs_node_count[1:3]:
#         result *= x[1]

#     return result


# def part1_1(input: list[str]) -> int:
#     # The problem asks us to connect points in 3D space, until 1000 points are connected.
#     # What is the size of the three largest graphs?
#     # I expect part2 to be something like MST + k-cut,
#     # so I will program in a way that will make that easy

#     result: int = 0
#     nodes: list[Node] = []
#     graphs: list[Graph] = []

#     for i, line in enumerate(input):
#         line = line.split(",")
#         nodes.append(Node(i, int(line[0]), int(line[1]), int(line[2]), None))

#     for i, node in enumerate(nodes):
#         graph = Graph(i)
#         node.parent_graph = graph

#         graph.edges[node] = []
#         graphs.append(graph)
    
#     nodes_in_graph = [1 for _ in range(len(graphs))]

#     print(len(graphs))
#     print(len(input))

#     connection_attempts = 0

#     distances: list[Distance] = []
#     heapify(distances)

#     # Calculate distances
#     for i, from_node in enumerate(nodes):
#         # From a node to all nodes after it (prevent double distance calculations)
#         for to_node in nodes[i+1:]:
#             d = distance(from_node, to_node)
#             heappush(distances, Distance(d, from_node, to_node))

#     print(len(distances))

#     # Connect graphs
#     while connection_attempts < 1000 and len(distances) > 0:
#         shortest = heappop(distances)

#         node1 = shortest.node1
#         node2 = shortest.node2

#         # Only connect if they are not already in the same graph
#         if node1.parent_graph.id is not node2.parent_graph.id:
#             # for from_node in node2.parent_graph.edges:
#                 # for edge in node2.parent_graph.edges[from_node]:
#                     # node1.parent_graph.edges[from_node].append(edge)
            
#             nodes_in_graph[node1.parent_graph.id] += nodes_in_graph[node2.parent_graph.id]
#             nodes_in_graph[node2.parent_graph.id] = 0
#             node2.parent_graph = node1.parent_graph
#         connection_attempts += 1

    
#     print(f"{connection_attempts=}")

#     # Find three biggest graphs
#     nodes_in_graph = sorted(nodes_in_graph, reverse=True)
#     print(nodes_in_graph)
#     print(f"Sanity sum: {sum(nodes_in_graph)}")
#     result = nodes_in_graph[0]
#     for x in nodes_in_graph[1:3]:
#         result *= x

#     return result


# region Input file handling
def main():
    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (True, True, True)
    run_part2 = (True, True, True)

    with (
        open("./data/day08-example.txt", "r", encoding="utf-8") as example,
        open("./data/day08-input.txt", "r", encoding="utf-8") as input,
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
