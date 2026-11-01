import functools
import itertools
import string

from utils import Day, aoc_main


def split_str(s: str) -> tuple[set[str], set[str]]:
    middle = len(s) // 2
    return set(s[:middle]), set(s[middle:])


def matching_items(rucksacks):
    yield from functools.reduce(set.intersection, rucksacks)


def iter_puzzle(puzzle, *, is_p2: bool = False):
    inp = puzzle.strip()
    yield from itertools.batched(inp.splitlines(), 3 if is_p2 else 1)


class Day03(Day[str]):
    def parse(self, input: str) -> str:
        return input

    def part1(self, puzzle):
        return sum(
            string.ascii_letters.index(item) + 1
            for rucksacks in map(
                split_str, itertools.chain.from_iterable(iter_puzzle(puzzle))
            )
            for item in matching_items(rucksacks)
        )

    def part2(self, puzzle):
        return sum(
            string.ascii_letters.index(item) + 1
            for rucksacks in iter_puzzle(puzzle, is_p2=True)
            for item in matching_items((set(rucksack) for rucksack in rucksacks))
        )


if __name__ == "__main__":
    aoc_main(Day03)
