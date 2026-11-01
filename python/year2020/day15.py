import unittest

from utils import Day, aoc_main, slow


def simulate(nums: tuple[int, ...], steps: int = 2020) -> int:
    last = nums[-1]
    turns = {num: turn for turn, num in enumerate(nums)}
    for turn in range(len(nums) - 1, steps - 1):
        turns[last], last = turn, turn - turns.get(last, turn)

    return last


class Day15(Day):
    def parse(self, input: str):
        inp = input.strip()
        return tuple(map(int, inp.split(",")))

    def part1(self, parsed):
        return simulate(parsed)

    def part2(self, parsed):
        return simulate(parsed, 30_000_000)


TEST_PUZZLE = """\
0,3,6"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day15()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 436)

    @slow
    def test_part2_test_puzzle(self):
        d = Day15()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 175594)


if __name__ == "__main__":
    aoc_main(Day15)
