import itertools
import math

from utils import Day, aoc_main


def solve(nums, size: int = 2) -> int:
    return next(
        math.prod(pair)
        for pair in itertools.combinations(nums, size)
        if sum(pair) == 2020
    )


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day01(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return solve(parsed)

    def part2(self, parsed):
        return solve(parsed, 3)


if __name__ == "__main__":
    aoc_main(Day01)
