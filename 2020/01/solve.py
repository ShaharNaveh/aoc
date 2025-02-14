import itertools
import math
import pathlib


def solve(nums, size: int = 2) -> int:
    return next(
        math.prod(pair)
        for pair in itertools.combinations(nums, size)
        if sum(pair) == 2020
    )


def iter_puzzle(puzzle_file) -> tuple[dict[complex, str], complex]:
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return solve(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return solve(iter_puzzle(puzzle_file), 3)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
