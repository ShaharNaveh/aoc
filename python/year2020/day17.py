import collections
import itertools
import operator
import unittest

from utils import Day, main


def find_neighs(cube: tuple[int, ...]):
    return {
        tuple(itertools.starmap(operator.add, zip(cube, offset)))
        for offset in itertools.product(range(-1, 2), repeat=len(cube))
        if any(offset)
    }


def simulate(cubes: set[tuple[int, ...]]) -> int:
    for _ in range(6):
        neighs = collections.Counter(
            ncube for cube in cubes for ncube in find_neighs(cube)
        )
        cubes = {
            cube
            for cube, neigh_count in neighs.items()
            if (neigh_count == 3) or ((neigh_count == 2) and (cube in cubes))
        }
    return len(cubes)


def parse_puzzle(puzzle, dims: int = 3):
    inp = puzzle.strip()
    return {
        (x, y) + (0,) * (dims - 2)
        for y, row in enumerate(inp.splitlines())
        for x, char in enumerate(row)
        if char == "#"
    }


class Day17(Day):
    def parse(self, inp: str) -> str:
        return inp

    def part1(self, puzzle):
        return simulate(parse_puzzle(puzzle))

    def part2(self, puzzle):
        return simulate(parse_puzzle(puzzle, 4))


TEST_PUZZLE = """\
.#.
..#
###"""


class Tests(unittest.TestCase):
    DAY = Day17()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 112)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 848)


if __name__ == "__main__":
    main(Day17)
