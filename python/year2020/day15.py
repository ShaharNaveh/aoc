import unittest

from utils import Day, main


def simulate(nums: tuple[int, ...], steps: int = 2020) -> int:
    last = nums[-1]
    turns = {num: turn for turn, num in enumerate(nums)}
    for turn in range(len(nums) - 1, steps - 1):
        turns[last], last = turn, turn - turns.get(last, turn)

    return last


class Day15(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return tuple(map(int, inp.split(",")))

    def part1(self, parsed):
        return simulate(parsed)

    def part2(self, parsed):
        return simulate(parsed, 30_000_000)


TEST_PUZZLE = "0,3,6"


class Tests(unittest.TestCase):
    DAY = Day15()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 436)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 175594)


if __name__ == "__main__":
    main(Day15)
