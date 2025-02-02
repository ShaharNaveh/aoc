import functools
import itertools
import pathlib


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def empty_spaces(universe: list[list[str]]) -> tuple[frozenset[int], frozenset[int]]:
    empty_xs = frozenset({idx for idx, row in enumerate(universe) if "#" not in row})
    empty_ys = frozenset(
        {idx for idx, col in enumerate(zip(*universe)) if "#" not in col}
    )
    return empty_xs, empty_ys


def offseted_galaxy(
    pos: complex, offset: int, empty_xs: frozenset[int], empty_ys: frozenset[int]
) -> complex:
    x_offset = sum(offset - 1 for _ in filter(lambda idx: pos.real > idx, empty_ys))
    y_offset = sum(offset - 1 for _ in filter(lambda idx: pos.imag > idx, empty_xs))
    return complex(int(pos.real) + x_offset, int(pos.imag) + y_offset)


def iter_galaxies(universe: list[list[str]]):
    yield from (
        complex(x, y)
        for y, row in enumerate(universe)
        for x, char in enumerate(row)
        if char == "#"
    )


def parse_puzzle(puzzle_file) -> list[list[str]]:
    inp = puzzle_file.read_text().strip()
    universe = [list(row) for row in inp.splitlines()]
    return universe


def p1(puzzle_file):
    universe = parse_puzzle(puzzle_file)
    empty_xs, empty_ys = empty_spaces(universe)
    func = functools.partial(
        offseted_galaxy, offset=2, empty_xs=empty_xs, empty_ys=empty_ys
    )
    return sum(
        manhattan(*pair)
        for pair in itertools.combinations(map(func, iter_galaxies(universe)), 2)
    )


def p2(puzzle_file):
    universe = parse_puzzle(puzzle_file)
    empty_xs, empty_ys = empty_spaces(universe)
    func = functools.partial(
        offseted_galaxy, offset=1_000_000, empty_xs=empty_xs, empty_ys=empty_ys
    )
    return sum(
        manhattan(*pair)
        for pair in itertools.combinations(map(func, iter_galaxies(universe)), 2)
    )
    return


puzzle_file = pathlib.Path(__file__).parent / "input.txt"
# puzzle_file = puzzle_file.with_stem("test_input")

print(p1(puzzle_file))
print(p2(puzzle_file))
