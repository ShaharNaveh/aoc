import functools
import itertools
import json
import math
import unittest

from utils import Day, main


def add_left(sf: list | int, n: int | None):
    if n is None:
        return sf

    if isinstance(sf, int):
        return sf + n

    return [add_left(sf[0], n), sf[1]]


def add_right(sf: list | int, n: int | None):
    if n is None:
        return sf

    if isinstance(sf, int):
        return sf + n

    return [sf[0], add_right(sf[1], n)]


def split(sf: list | int):
    if isinstance(sf, int):
        if sf >= 10:
            return True, [sf // 2, math.ceil(sf / 2)]
        return False, sf

    a, b = sf

    change, a = split(a)
    if change:
        return True, [a, b]

    change, b = split(b)
    return change, [a, b]


def explode(sf: list | int, depth: int = 4):
    if isinstance(sf, int):
        return False, None, sf, None

    if depth == 0:
        return True, sf[0], 0, sf[1]

    a, b = sf

    exp, left, a, right = explode(a, depth - 1)
    if exp:
        return True, left, [a, add_left(b, right)], None

    exp, left, b, right = explode(b, depth - 1)
    if exp:
        return True, None, [add_right(a, left), b], right
    return False, None, sf, None


def add(left: list | int, right: list | int) -> list:
    sf = [left, right]
    while True:
        change, _, sf, _ = explode(sf)
        if change:
            continue
        change, sf = split(sf)
        if not change:
            break
    return sf


def magnitude(sf: list | int) -> int:
    if isinstance(sf, int):
        return sf

    return (magnitude(sf[0]) * 3) + (magnitude(sf[1]) * 2)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(json.loads, inp.splitlines())


class Day18(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return magnitude(functools.reduce(add, parsed))

    def part2(self, parsed):
        return max(
            map(
                magnitude,
                itertools.starmap(add, itertools.permutations(parsed, 2)),
            )
        )


TEST_PUZZLE = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""


class Tests(unittest.TestCase):
    DAY = Day18()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 4140)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 3993)


if __name__ == "__main__":
    main(Day18)
