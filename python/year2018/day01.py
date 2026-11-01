import itertools

from utils import Day, aoc_main


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day01(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return sum(parsed)

    def part2(self, parsed):
        seen = set()
        return next(
            freq
            for freq in itertools.accumulate(itertools.cycle(parsed))
            if (freq in seen) or seen.add(freq)
        )


if __name__ == "__main__":
    aoc_main(Day01)
