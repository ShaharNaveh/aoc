import unittest

from utils import Day, aoc_main


def available_trails(puzzle):
    trails = [[pos] for pos, height in puzzle.items() if height == 0]
    for height in range(1, 10):
        for trail in trails.copy():
            last_pos = trail[-1]
            direction = -1
            for _ in range(4):
                next_pos = last_pos + direction
                if puzzle.get(next_pos) == height:
                    new_trail = trail + [next_pos]
                    trails.append(new_trail)
                direction *= -1j

        # Trails GC
        trails = [trail for trail in trails if len(trail) >= height + 1]
    return trails


class Day10(Day):
    def parse(self, input: str):
        inp = input.strip().replace(".", "0")
        puzzle = {}
        for row_idx, row in enumerate(inp.splitlines()):
            for col_idx, num in enumerate(row):
                puzzle[complex(row_idx, col_idx)] = int(num)
        return puzzle

    def part1(self, puzzle):
        trails = available_trails(puzzle)
        res = len({(trail[0], trail[-1]) for trail in trails})
        return res

    def part2(self, puzzle):
        trails = available_trails(puzzle)
        res = len(trails)
        return res


TEST_PUZZLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day10()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 36)

    def test_part2_test_puzzle(self):
        d = Day10()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 81)


if __name__ == "__main__":
    aoc_main(Day10)
