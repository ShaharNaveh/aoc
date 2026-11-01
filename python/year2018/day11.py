import functools
import itertools
import unittest

from utils import Day, aoc_main, slow

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
    return (
        find_prefix_sum(pos + complex(grid_size, grid_size), serial_number)
        - find_prefix_sum(pos + (grid_size * 1j), serial_number)
        - find_prefix_sum(pos + grid_size, serial_number)
        + find_prefix_sum(pos, serial_number)
    )


class Day11(Day):
    def parse(self, input: str):
        inp = input.strip()
        return int(inp)

    def part1(self, serial_number):
        grid_size = 3
        pos = max(
            itertools.starmap(
                complex,
                itertools.product(
                    range(MIN_GRID_SIZE, MAX_GRID_SIZE - grid_size + 1), repeat=2
                ),
            ),
            key=lambda pos: find_grid_power_level(pos, grid_size, serial_number),
        )
        return ",".join(map(str, map(int, (pos.real, pos.imag))))

    def part2(self, serial_number):
        pos, grid_size = max(
            (
                (pos, grid_size)
                for grid_size in range(MIN_GRID_SIZE, MAX_GRID_SIZE)
                for pos in itertools.starmap(
                    complex,
                    itertools.product(
                        range(MIN_GRID_SIZE, MAX_GRID_SIZE - grid_size + 1), repeat=2
                    ),
                )
            ),
            key=lambda tup: find_grid_power_level(*tup, serial_number),
        )
        return ",".join(map(str, map(int, (pos.real + 1, pos.imag + 1, grid_size))))


TEST_PUZZLE = """\
42"""


class Tests(unittest.TestCase):
    @slow
    def test_part2_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), "232,251,12")


if __name__ == "__main__":
    aoc_main(Day11)
