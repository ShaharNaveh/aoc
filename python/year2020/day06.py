import functools

from utils import Day, aoc_main


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from (
        frozenset(frozenset(answer) for answer in group.splitlines())
        for group in inp.split("\n" * 2)
    )


class Day06(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return sum(len(functools.reduce(frozenset.union, group)) for group in parsed)

    def part2(self, parsed):
        return sum(
            len(functools.reduce(frozenset.intersection, group)) for group in parsed
        )


if __name__ == "__main__":
    aoc_main(Day06)
