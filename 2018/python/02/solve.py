import collections
import itertools
import math
import pathlib


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.splitlines()


def p1(puzzle_file):
    return math.prod(
        collections.Counter(
            count
            for counter in map(collections.Counter, iter_puzzle(puzzle_file))
            for count in (2, 3)
            if count in counter.values()
        ).values()
    )


def p2(puzzle_file):
    return next(
        res
        for a, b in itertools.combinations(iter_puzzle(puzzle_file), r=2)
        if len(a) - len((res := "".join(x for x, y in zip(a, b) if x == y))) == 1
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
