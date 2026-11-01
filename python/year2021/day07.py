import functools

from utils import Day, aoc_main


@functools.cache
def range_sum(num: int) -> int:
    return num * (num + 1) // 2


def fuel_cost(crabs: tuple[int, ...], n: int) -> int:
    return sum(abs(crab - n) for crab in crabs)


def fuel_cost_p2(crabs: tuple[int, ...], n: int) -> int:
    return sum(range_sum(abs(crab - n)) for crab in crabs)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.split(","))


class Day07(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        crabs = tuple(parsed)
        return min(fuel_cost(crabs, n) for n in range(0, max(crabs) + 1))

    def part2(self, parsed):
        crabs = tuple(parsed)
        return min(fuel_cost_p2(crabs, n) for n in range(0, max(crabs) + 1))


if __name__ == "__main__":
    aoc_main(Day07)
