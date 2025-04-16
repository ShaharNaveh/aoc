import itertools
import pathlib


type Point = tuple[int, int, int, int]


def manhattan(p1: Point, p2: Point) -> int:
    return sum(abs(b - a) for a, b in zip(p1, p2))


def find_constellations(constellations, point: Point):
    npoint = constellations[point]
    if point != npoint:
        constellations[point] = find_constellations(constellations, npoint)
    return constellations[point]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {tuple(map(int, line.split(","))) for line in inp.splitlines()}


def p1(puzzle_file):
    points = parse_puzzle(puzzle_file)
    constellations = {point: point for point in points}
    for (i, p1), (j, p2) in itertools.product(enumerate(points), repeat=2):
        if i >= j:
            continue
        if find_constellations(constellations, p1) == find_constellations(
            constellations, p2
        ):
            continue

        if manhattan(p1, p2) > 3:
            continue
        constellations[constellations[p1]] = constellations[p2]

    for point in points:
        find_constellations(constellations, point)

    return len(set(constellations.values()))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
