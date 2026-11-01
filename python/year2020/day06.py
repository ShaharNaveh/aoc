import functools

from utils import Day, run


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from (
        frozenset(frozenset(answer) for answer in group.splitlines())
        for group in inp.split("\n" * 2)
    )


class Day06(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(len(functools.reduce(frozenset.union, group)) for group in parsed)

    def part2(self, parsed):
        return sum(
            len(functools.reduce(frozenset.intersection, group)) for group in parsed
        )


if __name__ == "__main__":
    run(Day06)
