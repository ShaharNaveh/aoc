import pathlib


def tilt_cycle(grid: tuple[str, ...]) -> tuple[str, ...]:
    for _ in range(4):
        grid = tilt_north(grid)
        grid = tuple("".join(reversed(row)) for row in zip(*grid))
    return grid


def tilt_north(grid: tuple[str, ...]) -> tuple[str, ...]:
    t_grid = tuple(map("".join, zip(*grid)))

    ngrid = []
    for row in t_grid:
        buf = []
        for part in row.split("#"):
            shifted = sorted(part, reverse=True)
            jshifted = "".join(shifted)
            buf.append(jshifted)
        nrow = "#".join(buf)
        ngrid.append(nrow)
    return tuple(map("".join, zip(*ngrid)))


def calc_load(grid: tuple[str, ...]) -> int:
    return sum(row.count("O") * i for i, row in enumerate(reversed(grid), start=1))


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(inp.splitlines())


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return calc_load(tilt_north(grid))


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)

    NTH = 1_000_000_000

    seen = {grid}
    cycle = [grid]
    for idx in range(NTH):
        grid = tilt_cycle(grid)
        if grid in seen:
            break
        seen.add(grid)
        cycle.append(grid)

    first_idx = cycle.index(grid)
    grid_idx = ((NTH - first_idx) % (idx - first_idx + 1)) + first_idx
    return calc_load(cycle[grid_idx])


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
