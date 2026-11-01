import collections
import itertools
import math

from utils import Day, aoc_main


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.splitlines()


class Day02(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return math.prod(
            collections.Counter(
                count
                for counter in map(collections.Counter, parsed)
                for count in (2, 3)
                if count in counter.values()
            ).values()
        )

    def part2(self, parsed):
        return next(
            res
            for a, b in itertools.combinations(parsed, r=2)
            if len(a) - len((res := "".join(x for x, y in zip(a, b) if x == y))) == 1
        )


if __name__ == "__main__":
    aoc_main(Day02)
