import collections
import itertools
import pathlib

def antinodes_pos(cords):
    for pos1, pos2 in itertools.combinations(cords, 2):
        yield pos1 + pos1 - pos2
        yield pos2 + pos2 - pos1

def parse_puzzle(path):
    inp = path.read_text().strip()
    grid = {}
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, char in enumerate(row):
            pos = complex(col_idx, row_idx)
            grid[pos] = char
    return grid

def groupby_char(grid):
    result = collections.defaultdict(set)
    for pos, char in grid.items():
        result[char] |= {pos}

    return result


def p1(path):
    grid = parse_puzzle(path)
    inverted_grid = groupby_char(grid)

    seen = set()
    for char, cords in inverted_grid.items():
        if char == ".":
            continue
        for antinode_pos in antinodes_pos(cords):
            if not grid.get(antinode_pos):
                continue
            seen.add(antinode_pos)

    print(len(seen))

puzzle_file = pathlib.Path(__file__).parent / "input.txt"
puzzle_file = pathlib.Path(__file__).parent / "test_input.txt"

p1(puzzle_file)
