import collections
import functools
import math
import operator
import unittest

from utils import Day, main


def move(pos: complex, v: complex, bounds: complex):
    npos = pos + v
    return complex(npos.real % bounds.real, npos.imag % bounds.imag)


def simulate(robots, seconds: int, bounds: complex):
    lst = robots.copy()
    for _ in range(seconds):
        for idx, robot in enumerate(lst):
            lst[idx] = robot | {"pos": move(**robot, bounds=bounds)}
    return lst


def parse_puzzle(inp: str):
    for line in inp.splitlines():
        pos_block, v_block = line.split()

        entry = {"pos": pos_block, "v": v_block}
        for key, block in entry.items():
            entry[key] = complex(*map(int, block.split("=")[-1].split(",")))
        yield entry


def calc_safety(robots, bounds):
    x_mid = bounds.real // 2
    y_mid = bounds.imag // 2
    quadrants = collections.defaultdict(int)
    for pos in map(operator.itemgetter("pos"), robots):
        x, y = pos.real, pos.imag
        if (x == x_mid) or (y == y_mid):
            continue

        if (x < x_mid) and (y < y_mid):
            key = 0
        elif (x > x_mid) and (y < y_mid):
            key = 1
        elif (x < x_mid) and (y > y_mid):
            key = 2
        else:
            key = 3
        quadrants[key] += 1

    return functools.reduce(operator.mul, quadrants.values())


def calc_entropy(positions):
    counter = collections.Counter(positions)
    total = sum(counter.values())
    entropy = -sum(
        (count / total) * math.log2(count / total) for count in counter.values()
    )
    return entropy


class Day14(Day):
    def __init__(self, bounds: complex = 101 + 103j):
        self.bounds = bounds

    def parse(self, inp: str) -> list[dict[str, complex]]:
        return list(parse_puzzle(inp.strip()))

    def part1(self, robots: list[dict[str, complex]]) -> int:
        simulated = simulate(robots, seconds=100, bounds=self.bounds)
        return calc_safety(simulated, bounds=self.bounds)

    def part2(self, robots: list[dict[str, complex]]) -> int:
        lst = [list(map(operator.itemgetter("pos"), robots))]
        for _ in range(1, 100_000):
            robots = simulate(robots, seconds=1, bounds=self.bounds)
            lst.append(list(map(operator.itemgetter("pos"), robots)))

        return max(
            ((calc_entropy(positions), idx) for idx, positions in enumerate(lst)),
            key=operator.itemgetter(0),
        )[1]


EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day14(bounds=11 + 7j)
        self.assertEqual(d.part1(d.parse(EXAMPLE)), 12)


if __name__ == "__main__":
    main(Day14)
