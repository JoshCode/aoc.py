from dataclasses import dataclass

@dataclass
class Point2D:
    x: int
    y: int

@dataclass
class Edge:
    x1: int
    y1: int
    x2: int
    y2: int

def part1(input: list[str]) -> int:
    result: int = 0

    points: list[Point2D] = []

    for line in input:
        coords = list(map(lambda x: int(x), line.split(",")))
        point = Point2D(coords[0], coords[1])
        points.append(point)

    areas: list[tuple[Point2D, Point2D, int]] = []

    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points[i+1:]):
            areas.append((p1, p2, area(p1, p2)))
    
    areas = sorted(areas, key=lambda x: x[2], reverse=True)
    print(areas[0])
    result = areas[0][2]

    return result

def part2(input: list[str]) -> int:
    result: int = 0

    points: list[Point2D] = []
    edges: list[Edge] = []

    # Parse input to 2D points
    for line in input:
        coords = list(map(lambda x: int(x), line.split(",")))
        point = Point2D(coords[0], coords[1])
        points.append(point)
    
    # Create edges
    for i, from_point in enumerate(points[:-1]):
        to_point = points[i+1]
        edge = Edge(from_point.x, from_point.y, to_point.x, to_point.y)
        edges.append(edge)
    
    # Close the shape
    from_point = points[-1]
    to_point = points[0]
    edge = Edge(from_point.x, from_point.y, to_point.x, to_point.y)
    edges.append(edge)

    # Delete objects for easier debugging
    del line, i, coords, point, from_point, to_point, edge

    # The coordinate system is points from top left 0,0
    def intersects(p1: Point2D, p2: Point2D) -> bool:
        rect_minX = min(p1.x, p2.x)
        rect_maxX = max(p1.x, p2.x)
        rect_minY = min(p1.y, p2.y)
        rect_maxY = max(p1.y, p2.y)

        for edge in edges:
            edge_minX = min(edge.x1, edge.x2)
            edge_maxX = max(edge.x1, edge.x2)
            edge_minY = min(edge.y1, edge.y2)
            edge_maxY = max(edge.y1, edge.y2)
            # Using <= and >=, because we're using edges that have line width (1 cell), so overlap with rectangle edge on an edge is okay
            rectLeftOfEdge = rect_maxX <= edge_minX
            rectRightOfEdge = rect_minX >= edge_maxX
            rectAboveEdge = rect_maxY <= edge_minY
            rectBelowEdge = rect_minY >= edge_maxY

            if not (rectLeftOfEdge or rectRightOfEdge or rectAboveEdge or rectBelowEdge):
                return True
        return False

    areas: list[tuple[Point2D, Point2D, int]] = []

    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points[i+1:]):
            areas.append((p1, p2, area(p1, p2)))
    
    areas = sorted(areas, key=lambda x: x[2], reverse=True)

    # Old line:
    # filtered_areas = list(filter(lambda x: not intersects(x[0], x[1]), areas))
    # result = filtered_areas[0][2]
    # This is a bit more optimised
    # Find the first area that clears the intersect check: this is the largest valid area, since areas is sorted
    for a in areas:
        if not intersects(a[0], a[1]):
            result = a[2]
            break
    
    return result


def area(p1: Point2D, p2: Point2D) -> int:
    return (abs(p1.x - p2.x) + 1) * (abs(p1.y - p2.y) + 1)

# region Input file handling
def main():
    import io
    from pathlib import Path

    # Define the following tuples to easily switch what runs
    # First argument: If this part runs
    # Second argument: Given True on first, if the puzzle input runs on this part
    run_part1 = (False, True, True)
    run_part2 = (True, True, True)
    input_path = Path.relative_to = Path(__file__).parent

    with (
        open(input_path / "data/day09-example.txt", "r", encoding="utf-8") as example,
        open(input_path / "data/day09-input.txt", "r", encoding="utf-8") as input,
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
