import functools
import pathlib

def detect_cycle(grid: tuple[str, ...], checks: int = 10_000) -> list[int]:
    seq = []
    seen = {}
    for idx in range(checks):
        grid = tilt_cycle(grid)
        load = calc_load(grid)

        if load in seen:
            start = seen[load]
            potential_cycle = seq[start:]
            if potential_cycle == seq[start + len(potential_cycle):start + 2 * len(potential_cycle)]:
                return seq[:start], seq[start:]
        seq.append(load)
        seen[load] = idx

@functools.cache
def tilt_cycle(grid: tuple[str, ...]) -> tuple[str, ...]:
    n_grid = tuple(
        "".join(row)
        for row in zip(*(tilt_row_west(col) for col in zip(*grid)))
    )
    w_grid = tuple(tilt_row_west(row) for row in n_grid)
    s_grid = tuple(
        "".join(row)
        for row in zip(*(tilt_row_west(col)[::-1] for col in zip(*reversed(w_grid))))
    )
    e_grid = tuple(tilt_row_west(row[::-1])[::-1] for row in s_grid)
    return e_grid

@functools.cache
def tilt_row_west(row: str) -> str:
    def inner(_row: str):
        buf = []
        for char in _row:
            match char:
                case "O":
                    buf.insert(0, char)
                case ".":
                    buf.append(char)
                case "#":
                    yield from buf
                    yield char
                    buf.clear()
        yield from buf
    return "".join(inner(row))

def calc_load(grid: tuple[str, ...]) -> int:
    return sum(row.count("O") * i for i, row in enumerate(reversed(grid), start=1))

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(inp.splitlines())

def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    grid = tuple(
        "".join(row)
        for row in zip(*(tilt_row_west(col) for col in zip(*grid)))
    )
    return calc_load(grid)




def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)

    pref, cy = detect_cycle(grid)
    if len(pref):
        print(len(pref))
    return
#    idx = (1_000_000_000 - 1) % len(loads)
   # res = loads[idx]
    return res


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
