import pathlib
import itertools
import operator


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return sum(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    seen = set()
    return next(
        freq
        for freq in itertools.accumulate(itertools.cycle(iter_puzzle(puzzle_file)))
        if (freq in seen) or seen.add(freq)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
