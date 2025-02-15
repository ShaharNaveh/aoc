import pathlib


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    trans = str.maketrans({"F": "0", "B": "1", "L": "0", "R": "1"})
    yield from map(lambda raw: int(raw.translate(trans), 2), inp.splitlines())


def p1(puzzle_file):
    return max(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    ids = sorted(iter_puzzle(puzzle_file))
    for a, b in zip(ids, ids[1:]):
        if b - a != 1:
            return a + 1


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
