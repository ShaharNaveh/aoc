import pathlib


def parse_puzzle(puzzle_file) -> tuple[dict[complex, str], complex]:
    inp = puzzle_file.read_text().strip()
    lines = inp.splitlines()
    bounds = complex(*map(len, (lines[0], lines)))
    grid = {
        complex(x, y): char
        for y, row in enumerate(lines)
        for x, char in enumerate(row)
        if char != "."
    }
    return grid, bounds


def step(f: callable, typ: str, grid: dict[complex, str]) -> dict[complex, str]:
    return {
        npos if (((npos := f(pos)) not in grid) and (char == typ)) else pos: char
        for pos, char in grid.items()
    }


def solve(grid: dict[complex, str], bounds: complex) -> int:
    before, after = None, grid
    steps = 0
    while True:
        steps += 1

        before = after.copy()
        after = step(
            lambda pos: complex((pos.real + 1) % bounds.real, pos.imag), ">", after
        )
        after = step(
            lambda pos: complex(pos.real, (pos.imag + 1) % bounds.imag), "v", after
        )
        if before == after:
            return steps


def p1(puzzle_file):
    return solve(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
