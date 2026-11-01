import itertools
import unittest

from utils import Day, run


def iter_puzzle(puzzle):
    yield 1

    inp = puzzle.strip()
    func = lambda x: int(x) if x[-1].isdigit() else 0
    yield from map(func, inp.split())


def simulate(ops):
    yield from enumerate(itertools.accumulate(ops), start=1)


class Day10(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(cycle * x for cycle, x in simulate(parsed) if cycle % 40 == 20)

    def part2(self, parsed):
        return "\n".join(
            "".join(
                "#" if (cycle - 1) % 40 - x in (-1, 0, 1) else " " for cycle, x in batch
            )
            for batch in itertools.batched(simulate(parsed), 40)
        )


TEST_PUZZLE = """\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day10()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 13140)


if __name__ == "__main__":
    run(Day10)
