import functools
import pathlib


@functools.cache
def get_neigh(pos: complex) -> frozenset[complex]:
    return frozenset(
        pos + offset for offset in (1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j)
    )


def simulate(grid):
    while True:
        for pos in grid:
            grid[pos] += 1

        flashed = set()
        while max(grid.values()) > 9:
            for pos, val in grid.copy().items():
                if pos in flashed:
                    continue
                if val <= 9:
                    continue

                flashed.add(pos)
                grid[pos] = 0

                for neigh in get_neigh(pos):
                    if neigh not in grid:
                        continue
                    if neigh in flashed:
                        continue
                    grid[neigh] += 1

        yield len(flashed)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): int(val)
        for y, row in enumerate(inp.splitlines())
        for x, val in enumerate(row)
    }


def p1(puzzle_file):
    res = 0
    for step, flashes in enumerate(simulate(parse_puzzle(puzzle_file)), 1):
        if step > 100:
            break
        res += flashes
    return res


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return next(
        step for step, flashes in enumerate(simulate(grid), 1) if flashes == len(grid)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
