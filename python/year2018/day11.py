import collections
import functools
import itertools
import unittest

from utils import Day, main

MIN_GRID_SIZE, MAX_GRID_SIZE = 1, 300
type PrefixSum = collections.defaultdict[complex, int]


def find_power_level(pos: complex, serial_number: int) -> int:
    x, y = map(int, (pos.real, pos.imag))
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = power_level // 100 % 10
    return power_level - 5


@functools.cache
def find_prefix_sum(pos: complex, serial_number: int) -> int:
    if not all(MAX_GRID_SIZE >= n >= MIN_GRID_SIZE for n in (pos.real, pos.imag)):
        return 0
    return (
        find_power_level(pos, serial_number)
        + find_prefix_sum(pos - 1, serial_number)
        + find_prefix_sum(pos - 1j, serial_number)
        - find_prefix_sum(pos - 1 - 1j, serial_number)
    )


def find_grid_power_level(pos: complex, grid_size: int, serial_number: int) -> int:
    """Total power of the square whose top-left cell is `pos`."""
    corner = pos - 1 - 1j
    return (
        find_prefix_sum(corner + complex(grid_size, grid_size), serial_number)
        - find_prefix_sum(corner + (grid_size * 1j), serial_number)
        - find_prefix_sum(corner + grid_size, serial_number)
        + find_prefix_sum(corner, serial_number)
    )


def iter_top_left(grid_size: int):
    """Every top-left cell of a `grid_size` square that fits in the grid."""
    return itertools.starmap(
        complex,
        itertools.product(
            range(MIN_GRID_SIZE, MAX_GRID_SIZE - grid_size + 2), repeat=2
        ),
    )


class Day11(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return int(inp)

    def part1(self, serial_number):
        grid_size = 3
        pos = max(
            iter_top_left(grid_size),
            key=lambda pos: find_grid_power_level(pos, grid_size, serial_number),
        )
        return ",".join(map(str, map(int, (pos.real, pos.imag))))

    def part2(self, serial_number):
        pos, grid_size = max(
            (
                (pos, grid_size)
                for grid_size in range(MIN_GRID_SIZE, MAX_GRID_SIZE + 1)
                for pos in iter_top_left(grid_size)
            ),
            key=lambda tup: find_grid_power_level(*tup, serial_number),
        )
        return ",".join(map(str, map(int, (pos.real, pos.imag, grid_size))))


TEST_PUZZLE = """\
42"""


class Tests(unittest.TestCase):
    def test_power_level(self):
        for pos, serial_number, expected in [
            (3 + 5j, 8, 4),
            (122 + 79j, 57, -5),
            (217 + 196j, 39, 0),
            (101 + 153j, 71, 4),
        ]:
            with self.subTest(pos=pos, serial_number=serial_number):
                self.assertEqual(find_power_level(pos, serial_number), expected)

    def test_part1_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), "21,61")

    def test_part1_serial_18(self):
        d = Day11()
        self.assertEqual(d.part1(d.parse("18")), "33,45")

    def test_part2_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), "232,251,12")


if __name__ == "__main__":
    main(Day11)
