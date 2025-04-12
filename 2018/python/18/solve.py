import collections
import enum
import functools
import itertools
import pathlib

type Grid = dict[complex, "Acre"]


@enum.unique
class Acre(enum.StrEnum):
    Open = "."
    Tree = "|"
    Lumberyard = "#"


@functools.cache
def find_neighbors(pos: complex) -> frozenset[complex]:
    return frozenset(
        pos + offset
        for offset in itertools.starmap(
            complex, filter(any, itertools.product(range(-1, 2), repeat=2))
        )
    )


def parse_puzzle(puzzle_file) -> Grid:
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): Acre(tile)
        for y, row in enumerate(inp.splitlines())
        for x, tile in enumerate(row)
    }


def simulate(grid: Grid):
    while True:
        ngrid = {}
        for pos, acre in grid.items():
            counter = collections.Counter(map(grid.get, find_neighbors(pos)))
            if (acre == Acre.Open) and (counter[Acre.Tree] >= 3):
                ngrid[pos] = Acre.Tree
            elif (acre == Acre.Tree) and (counter[Acre.Lumberyard] >= 3):
                ngrid[pos] = Acre.Lumberyard
            elif (acre == Acre.Lumberyard) and (
                not all(counter[x] for x in (Acre.Lumberyard, Acre.Tree))
            ):
                ngrid[pos] = Acre.Open
            else:
                ngrid[pos] = acre

        yield ngrid
        grid = ngrid


def calc_resource_value(grid: Grid) -> int:
    counter = collections.Counter(grid.values())
    return counter[Acre.Tree] * counter[Acre.Lumberyard]


def p1(puzzle_file):
    return calc_resource_value(
        next(
            grid
            for minute, grid in enumerate(simulate(parse_puzzle(puzzle_file)), 1)
            if minute == 10
        )
    )


def p2(puzzle_file):
    seen, prev = {}, None
    for minute, grid in enumerate(simulate(parse_puzzle(puzzle_file)), 1):
        resources_value = calc_resource_value(grid)
        cycle = minute - seen.get(resources_value, 0)
        if (cycle == prev) and ((1_000_000_000 % cycle) == (minute % cycle)):
            return resources_value
        seen[resources_value] = minute
        prev = cycle


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
