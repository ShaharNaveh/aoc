import math
import pathlib

OFFSETS = (1, -1, 1j, -1j)

def scenic_score(pos: complex, grid: dict[complex, int], bounds: complex) -> int:
    if is_edge(pos, bounds):
        return 0

    tree = grid[pos]
    scores = {}
    for offset in OFFSETS:
        score = 0
        for npos in iter_until_edge(pos, offset, bounds):
            score += 1
            if grid[npos] >= tree:
                break
        if score == 0:
            return 0
        scores[offset] = score

    return math.prod(scores.values())

def iter_until_edge(start: complex, offset: complex, bounds: complex):
    pos = start + offset
    while (
        (0 <= pos.real <= bounds.real) and (0 <= pos.imag <= bounds.imag)
    ):
        yield pos
        pos += offset

def is_edge(pos: complex, bounds: complex) -> bool:
    return (pos.real in (0, bounds.real)) or (pos.imag in (0, bounds.imag))

def is_tree_visible(pos: complex, grid: dict[complex, int], bounds: complex) -> bool:
    if is_edge(pos, bounds):
        return True

    tree = grid[pos]
    return any(
        all(tree > grid[npos] for npos in iter_until_edge(pos, offset, bounds))
        for offset in OFFSETS
    )


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): int(tree)
        for y, line in enumerate(inp.splitlines())
        for x, tree in enumerate(line)
    }


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    bounds = [*grid][-1]
    return sum(is_tree_visible(pos, grid, bounds) for pos in grid)

def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    bounds = [*grid][-1]
    return max(scenic_score(pos, grid, bounds) for pos in grid)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
