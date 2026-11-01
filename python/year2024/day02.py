import unittest

from utils import Day, aoc_main


def is_safe(level):
    slevel = sorted(level)
    if not ((level == slevel) or (level == sorted(level, reverse=True))):
        return False

    for n1, n2 in zip(slevel, slevel[1:]):
        if n1 == n2:
            return False

        diff = abs(n1 - n2)
        if diff > 3:
            return False
    return True


def iter_dampened_safe(levels):
    for level in levels:
        for idx in range(len(level)):
            lvl = level[:idx] + level[idx + 1 :]
            if is_safe(lvl):
                yield 1
                break


class Day02(Day[list[list[int]]]):
    def parse(self, input: str) -> list[list[int]]:
        return [list(map(int, line.split(" "))) for line in input.splitlines()]

    def part1(self, levels: list[list[int]]) -> int:
        return sum(map(is_safe, levels))

    def part2(self, levels: list[list[int]]) -> int:
        return sum(iter_dampened_safe(levels))


EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day02()
        self.assertEqual(d.part1(d.parse(EXAMPLE)), 2)

    def test_part2(self):
        d = Day02()
        self.assertEqual(d.part2(d.parse(EXAMPLE)), 4)


if __name__ == "__main__":
    aoc_main(Day02)
