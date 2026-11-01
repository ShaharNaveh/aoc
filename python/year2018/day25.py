import itertools
import unittest

from utils import Day, main

type Point = tuple[int, int, int, int]


def manhattan(p1: Point, p2: Point) -> int:
    return sum(abs(b - a) for a, b in zip(p1, p2))


def find_constellations(constellations, point: Point):
    npoint = constellations[point]
    if point != npoint:
        constellations[point] = find_constellations(constellations, npoint)
    return constellations[point]


class Day25(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {tuple(map(int, line.split(","))) for line in inp.splitlines()}

    def part1(self, points):
        constellations = {point: point for point in points}
        for (i, p1), (j, p2) in itertools.product(enumerate(points), repeat=2):
            if i >= j:
                continue
            if find_constellations(constellations, p1) == find_constellations(
                constellations, p2
            ):
                continue

            if manhattan(p1, p2) > 3:
                continue
            constellations[constellations[p1]] = constellations[p2]

        for point in points:
            find_constellations(constellations, point)

        return len(set(constellations.values()))


TEST_PUZZLE = """\
-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""


class Tests(unittest.TestCase):
    DAY = Day25()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 4)


if __name__ == "__main__":
    main(Day25)
