import itertools
import pathlib


type Point = tuple[int, int, int, int]
type Constellations = frozenset[frozenset[Point]]


def manhattan(a: Point, b: Point) -> int:
    return sum(abs(r - l) for l, r in zip(a, b))


def find_constellations(constellations: Constellations) -> Constellations:
    while True:
        print(len(constellations))
        for l, r in itertools.combinations(constellations, r=2):
            if any(manhattan(a, b) <= 3 for a in l for b in r):
                constellations -= {l, r}
                constellations |= frozenset({l | r})
                break
        else:
            return constellations


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return frozenset(
        frozenset({tuple(map(int, line.split(",")))}) for line in inp.splitlines()
    )


def p1(puzzle_file):
    return len(find_constellations(parse_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
