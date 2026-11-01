import functools

from utils import Day, aoc_main


@functools.cache
def simulate(timer: int, days: int = 80) -> int:
    if 0 >= days - timer:
        return 1

    ndays = days - 1
    ntimer = timer - 1

    if ntimer >= 0:
        return simulate(ntimer, ndays)
    else:
        return simulate(6, ndays) + simulate(8, ndays)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.split(","))


class Day06(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return sum(map(simulate, parsed))

    def part2(self, parsed):
        return sum(simulate(timer, 256) for timer in parsed)


if __name__ == "__main__":
    aoc_main(Day06)
