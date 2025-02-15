import functools
import pathlib


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from (
        frozenset(frozenset(answer) for answer in group.splitlines())
        for group in inp.split("\n" * 2)
    )


def p1(puzzle_file):
    return sum(
        len(functools.reduce(frozenset.union, group))
        for group in iter_puzzle(puzzle_file)
    )


def p2(puzzle_file):
    return sum(
        len(functools.reduce(frozenset.intersection, group))
        for group in iter_puzzle(puzzle_file)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
