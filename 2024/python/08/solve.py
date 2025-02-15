import collections
import itertools
import pathlib


def parse_puzzle(path):
    inp = path.read_text().strip().replace("#", ".")
    puzzle = collections.defaultdict(set)
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, char in enumerate(row):
            puzzle[char].add(row_idx + col_idx * 1j)

    return dict(puzzle)


def p1(path):
    puzzle = parse_puzzle(path)
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
    print(len(anti))


def p2(path):
    puzzle = parse_puzzle(path)
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
    print(len(anti))


puzzle_file = pathlib.Path(__file__).parent / "input.txt"
# puzzle_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(puzzle_file)
p2(puzzle_file)
