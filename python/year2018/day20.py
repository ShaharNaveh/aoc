import collections
import unittest

from utils import Day, main

OFFSETS = {"N": -1j, "W": -1, "S": 1j, "E": 1}


def find_distances(instructions: str) -> tuple[int, ...]:
    pos = ppos = 0
    locs = []
    distances = collections.defaultdict(int)
    for char in instructions:
        match char:
            case "(":
                locs.append(pos)
            case ")":
                pos = locs.pop()
            case "|":
                pos = locs[-1]
            case _:
                pos += OFFSETS[char]
                dist, pdist = distances[pos], distances[ppos] + 1
                distances[pos] = pdist if dist == 0 else min(dist, pdist)
        ppos = pos

    return tuple(distances.values())


class Day20(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return inp[1:-1]

    def part1(self, parsed):
        return max(find_distances(parsed))

    def part2(self, parsed):
        return sum(dist >= 1000 for dist in find_distances(parsed))


TEST_PUZZLE = """\
^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day20()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 31)

    def test_part2_test_puzzle(self):
        d = Day20()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 0)


if __name__ == "__main__":
    main(Day20)
