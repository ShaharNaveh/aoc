import math
import pathlib


def slide(trees: frozenset[complex], bounds: complex, slope: complex = 3 + 1j) -> int:
    count = 0
    pos = 0
    while pos.imag <= bounds.imag:
        count += pos in trees
        pos = complex((pos.real + slope.real) % bounds.real, pos.imag + slope.imag)
    return count


def parse_puzzle(puzzle_file) -> tuple[frozenset[complex], complex]:
    inp = puzzle_file.read_text().strip()
    lines = inp.splitlines()
    bounds = complex(*map(len, (lines[0], lines)))
    trees = frozenset(
        complex(x, y)
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "#"
    )
    return trees, bounds


def p1(puzzle_file):
    return slide(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    trees, bounds = parse_puzzle(puzzle_file)
    return math.prod(
        slide(trees, bounds, slope)
        for slope in (1 + 1j, 3 + 1j, 5 + 1j, 7 + 1j, 1 + 2j)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
