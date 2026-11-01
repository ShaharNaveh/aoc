import math
import unittest

from utils import Day, aoc_main


def slide(trees: frozenset[complex], bounds: complex, slope: complex = 3 + 1j) -> int:
    count = 0
    pos = 0
    while pos.imag <= bounds.imag:
        count += pos in trees
        pos = complex((pos.real + slope.real) % bounds.real, pos.imag + slope.imag)
    return count


class Day03(Day):
    def parse(self, input: str):
        inp = input.strip()
        lines = inp.splitlines()
        bounds = complex(*map(len, (lines[0], lines)))
        trees = frozenset(
            complex(x, y)
            for y, line in enumerate(lines)
            for x, char in enumerate(line)
            if char == "#"
        )
        return trees, bounds

    def part1(self, parsed):
        return slide(*parsed)

    def part2(self, parsed):
        trees, bounds = parsed
        return math.prod(
            slide(trees, bounds, slope)
            for slope in (1 + 1j, 3 + 1j, 5 + 1j, 7 + 1j, 1 + 2j)
        )


TEST_PUZZLE = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day03()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 7)

    def test_part2_test_puzzle(self):
        d = Day03()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 336)


if __name__ == "__main__":
    aoc_main(Day03)
