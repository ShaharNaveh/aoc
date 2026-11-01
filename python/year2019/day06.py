import collections
import unittest

from utils import Day, main


def orbit_count(orbit: str, orbits: dict[str, str]) -> int:
    if (norbit := orbits.get(orbit)) is None:
        return 0
    return 1 + orbit_count(norbit, orbits)


class Day06(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {k: v for v, k in map(lambda x: x.split(")"), inp.splitlines())}

    def part1(self, orbits):
        return sum(orbit_count(orbit, orbits) for orbit in orbits)

    def part2(self, parsed):
        orbits = collections.defaultdict(set)
        for a, b in parsed.items():
            orbits[a].add(b)
            orbits[b].add(a)

        todo, seen, steps = {"YOU"}, set(), 0
        while "SAN" not in todo:
            steps += 1
            ntodo = set()
            for orbit in todo:
                if orbit in seen:
                    continue
                ntodo |= orbits[orbit]
            seen |= todo
            todo = ntodo

        return steps - 2


TEST_PUZZLE = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""


class Tests(unittest.TestCase):
    DAY = Day06()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 54)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 4)


if __name__ == "__main__":
    main(Day06)
