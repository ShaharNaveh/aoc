import collections
import re
import unittest

from utils import Day, main


def play(max_players: int, last_marble: int) -> int:
    scores = collections.defaultdict(int)
    circle = collections.deque([0])
    for marble in range(1, last_marble + 1):
        if (marble % 23) == 0:
            circle.rotate(7)
            scores[marble % max_players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores.values())


class Day09(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return map(int, re.findall(r"(\d+)", inp))

    def part1(self, parsed):
        return play(*parsed)

    def part2(self, parsed):
        max_players, last_marble = parsed
        return play(max_players, last_marble * 100)


TEST_PUZZLE = """\
30 players; last marble is worth 5807 points"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day09()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 37305)


if __name__ == "__main__":
    main(Day09)
