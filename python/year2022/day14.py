import itertools
import unittest

from utils import Day, main


def pour_sand(
    rocks: set[complex],
    min_x: int,
    max_x: int,
    max_y: int,
    *,
    pos: complex = 500,
) -> complex | None:
    if (max_x < pos.real < min_x) or (pos.imag > max_y):
        return None

    for offset in (1j, -1 + 1j, 1 + 1j):
        npos = pos + offset
        if npos not in rocks:
            return pour_sand(rocks, pos=npos, min_x=min_x, max_x=max_x, max_y=max_y)
    return pos


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        paths = [complex(*map(int, path.split(","))) for path in line.split(" -> ")]
        yield from paths
        for a, b in itertools.pairwise(paths):
            dist = b - a
            if dist.real:
                offset = dist.real / abs(dist.real)
            else:
                offset = (dist.imag / abs(dist.imag)) * 1j

            for pos in itertools.count(a, offset):
                if pos == b:
                    break
                yield pos


class Day14(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        rocks = set(parsed)
        rocks_len = len(rocks)
        xs = set(rock.real for rock in rocks)
        min_x, max_x = min(xs), max(xs)
        max_y = max(rock.imag for rock in rocks)

        while (
            sand := pour_sand(rocks, min_x=min_x, max_x=max_x, max_y=max_y)
        ) is not None:
            rocks.add(sand)

        return len(rocks) - rocks_len

    def part2(self, parsed):
        rocks = set(parsed)
        max_y = max(int(rock.imag) for rock in rocks) + 2

        xs = set(int(rock.real) for rock in rocks)
        min_x, max_x = min(xs), max(xs)

        min_x *= -max_y
        max_x *= max_y + 1

        for x in range(min_x, max_x):
            rocks.add(complex(x, max_y))

        for i in itertools.count(1):
            sand = pour_sand(
                rocks, min_x=-float("inf"), max_x=float("inf"), max_y=max_y
            )
            if sand == 500:
                return i
            rocks.add(sand)


TEST_PUZZLE = """\
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


class Tests(unittest.TestCase):
    DAY = Day14()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 24)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 93)


if __name__ == "__main__":
    main(Day14)
