import itertools
import re
import unittest

from utils import Day, main


def triangular(n: int) -> int:
    return n * (n + 1) // 2


def inv_triangular(n: int) -> int:
    return int((n * 2) ** 0.5)


def iter_pos(x_bounds: tuple[int, int], y_bounds: tuple[int, int]):
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    for px, py in itertools.product(
        range(inv_triangular(x_min), x_max + 1), range(y_min, -y_min)
    ):
        x = y = 0
        vx, vy = px, py
        while (x <= x_max) and (y >= y_min):
            if (x >= x_min) and (y <= y_max):
                yield x, y
                break

            x += vx
            y += vy

            vy -= 1

            if vx > 0:
                vx -= 1


class Day17(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return tuple(tuple(map(int, t)) for t in re.findall(r"(-?\d+)..(-?\d+)", inp))

    def part1(self, parsed):
        _, y_bounds = parsed
        return triangular(y_bounds[0])

    def part2(self, parsed):
        return sum(1 for _ in iter_pos(*parsed))


TEST_PUZZLE = """\
target area: x=20..30, y=-10..-5"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day17()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 45)

    def test_part2_test_puzzle(self):
        d = Day17()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 112)


if __name__ == "__main__":
    main(Day17)
