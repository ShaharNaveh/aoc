import heapq
import re
import typing
import unittest

from utils import Day, aoc_main


class Vec3(typing.NamedTuple):
    x: int
    y: int
    z: int

    def distance_to(self: typing.Self, other) -> float:
        return sum(abs(b - a) for a, b in zip(self, other))


class Nanobot(typing.NamedTuple):
    pos: Vec3
    r: int

    def __and__(self: typing.Self, other) -> bool:
        return self.distance_to(other) <= self.r

    def distance_to(self: typing.Self, other) -> float:
        return self.pos.distance_to(other.pos)

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        *pos, r = map(int, re.findall(r"(-?\d+)", raw))
        return cls(Vec3(*pos), r)


class Day23(Day):
    def parse(self, input: str):
        inp = input.strip()
        return frozenset(map(Nanobot.from_str, inp.splitlines()))

    def part1(self, nanobots):
        nanobot = max(nanobots, key=lambda x: x.r)
        return sum(nanobot & other for other in nanobots)

    def part2(self, parsed):
        pq = []
        for nanobot in parsed:
            dist = sum(map(abs, nanobot.pos))
            heapq.heappush(pq, (max(0, dist - nanobot.r), 1))
            heapq.heappush(pq, (dist + nanobot.r + 1, -1))

        count = max_count = res = 0
        while pq:
            dist, offset = heapq.heappop(pq)
            count += offset
            if count > max_count:
                res = dist
                max_count = count
        return res


TEST_PUZZLE = """\
pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day23()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 6)

    def test_part2_test_puzzle(self):
        d = Day23()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 36)


if __name__ == "__main__":
    aoc_main(Day23)
