import functools
import unittest

from utils import Day, main


@functools.cache
def get_neigh(pos: complex) -> frozenset[complex]:
    return frozenset(
        pos + offset for offset in (1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)
    )


def simulate(grid):
    while True:
        for pos in grid:
            grid[pos] += 1

        flashed = set()
        while max(grid.values()) > 9:
            for pos, val in grid.copy().items():
                if pos in flashed:
                    continue
                if val <= 9:
                    continue

                flashed.add(pos)
                grid[pos] = 0

                for neigh in get_neigh(pos):
                    if neigh not in grid:
                        continue
                    if neigh in flashed:
                        continue
                    grid[neigh] += 1

        yield len(flashed)


class Day11(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {
            complex(x, y): int(val)
            for y, row in enumerate(inp.splitlines())
            for x, val in enumerate(row)
        }

    def part1(self, parsed):
        res = 0
        for step, flashes in enumerate(simulate(parsed), 1):
            if step > 100:
                break
            res += flashes
        return res

    def part2(self, grid):
        return next(
            step
            for step, flashes in enumerate(simulate(grid), 1)
            if flashes == len(grid)
        )


TEST_PUZZLE = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 1656)

    def test_part2_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 195)


if __name__ == "__main__":
    main(Day11)
