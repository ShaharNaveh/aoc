import math
import pathlib


def basin_from_low_point(low_pos: complex, grid: dict[complex, int]) -> int:
    basin = set()
    seen = set()
    todo = {low_pos}

    while todo:
        pos = todo.pop()

        basin.add(pos)
        seen.add(pos)

        for neigh in iter_neigh(pos):
            if neigh in seen:
                continue
            if grid.get(neigh, 9) == 9:
                seen.add(neigh)
                continue
            todo.add(neigh)

    return len(basin)


def iter_neigh(pos: complex):
    yield from (pos + offset for offset in (1, -1, 1j, -1j))


def iter_low_points(grid: dict[complex, int]):
    for pos, height in grid.items():
        if height == 9:
            continue
        if any(height >= grid.get(neigh, float("inf")) for neigh in iter_neigh(pos)):
            continue
        yield pos, height + 1


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): int(val)
        for y, row in enumerate(inp.splitlines())
        for x, val in enumerate(row)
    }


def p1(puzzle_file):
    return sum(
        risk_level for _, risk_level in iter_low_points(parse_puzzle(puzzle_file))
    )


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    sizes = tuple(basin_from_low_point(pos, grid) for pos, _ in iter_low_points(grid))
    return math.prod(sorted(sizes, reverse=True)[:3])


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
