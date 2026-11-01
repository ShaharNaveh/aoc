import collections
import itertools
import operator
import unittest

from utils import Day, aoc_main


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


class Day17(Day[str]):
    def parse(self, input: str) -> str:
        return input

    def part1(self, puzzle):
        return simulate(parse_puzzle(puzzle))

    def part2(self, puzzle):
        return simulate(parse_puzzle(puzzle, 4))


TEST_PUZZLE = """\
.#.
..#
###"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day17()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 112)

    def test_part2_test_puzzle(self):
        d = Day17()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 848)


if __name__ == "__main__":
    aoc_main(Day17)
