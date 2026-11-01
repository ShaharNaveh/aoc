import collections
import enum
import functools
import itertools
import unittest

from utils import Day, run

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


class Day18(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {
            complex(x, y): Acre(tile)
            for y, row in enumerate(inp.splitlines())
            for x, tile in enumerate(row)
        }

    def part1(self, parsed):
        return calc_resource_value(
            next(
                grid for minute, grid in enumerate(simulate(parsed), 1) if minute == 10
            )
        )

    def part2(self, parsed):
        seen, prev = {}, None
        for minute, grid in enumerate(simulate(parsed), 1):
            resources_value = calc_resource_value(grid)
            cycle = minute - seen.get(resources_value, 0)
            if (cycle == prev) and ((1_000_000_000 % cycle) == (minute % cycle)):
                return resources_value
            seen[resources_value] = minute
            prev = cycle


TEST_PUZZLE = """\
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day18()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 1147)


if __name__ == "__main__":
    run(Day18)
