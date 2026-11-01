import collections
import itertools

from utils import Day, aoc_main


class Day08(Day):
    def parse(self, input: str):
        inp = input.strip().replace("#", ".")
        puzzle = collections.defaultdict(set)
        for row_idx, row in enumerate(inp.splitlines()):
            for col_idx, char in enumerate(row):
                puzzle[char].add(row_idx + col_idx * 1j)

        return dict(puzzle)

    def part1(self, puzzle):
        all_pos = {pos for pos in itertools.chain.from_iterable(puzzle.values())}
        del puzzle["."]

        anti = set()
        for char, cords in puzzle.items():
            for a, b in itertools.combinations(cords, 2):
                diff = a - b
                if (a := a + diff) in all_pos:
                    anti.add(a)
                if (b := b - diff) in all_pos:
                    anti.add(b)
        return len(anti)

    def part2(self, puzzle):
        all_pos = {pos for pos in itertools.chain.from_iterable(puzzle.values())}
        del puzzle["."]

        anti = set()
        for char, cords in puzzle.items():
            for a, b in itertools.combinations(cords, 2):
                diff = a - b
                while (a := a - diff) in all_pos:
                    anti.add(a)
                while (b := b + diff) in all_pos:
                    anti.add(b)
        return len(anti)


if __name__ == "__main__":
    aoc_main(Day08)
