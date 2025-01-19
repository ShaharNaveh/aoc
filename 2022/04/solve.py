import pathlib

def overlap(s1: set[int], s2: set[int], *, is_p2: bool = False):
    if is_p2:
        return bool(s1 & s2)

    return (s1 >= s2) or (s2 >= s1)

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for line in inp.splitlines():
        buf = []
        for part in line.split(","):
            start, stop = map(int, part.split("-"))
            buf += [set(range(start, stop + 1))]
        yield tuple(buf)


def p1(puzzle_file):
    return sum(overlap(*pair) for pair in iter_puzzle(puzzle_file))

def p2(puzzle_file):
    return sum(overlap(*pair, is_p2=True) for pair in iter_puzzle(puzzle_file))

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
