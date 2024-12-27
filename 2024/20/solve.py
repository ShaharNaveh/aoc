import itertools
import pathlib


def path_dist(grid, cheat_len):
    start = next(pos for pos, char in grid.items() if char == "S")
    end = next(pos for pos, char in grid.items() if char == "E")

    pos = start
    distances = {start: 0}
    while pos != end:
        for direction in (1, -1, 1j, -1j):
            npos = pos + direction
            if npos not in grid:
                continue
            if npos in distances:
                continue
            distances[npos] = distances[pos] + 1
            pos = npos
            break

    res = 0
    for (pos1, pos_d1), (pos2, pos_d2) in itertools.combinations(distances.items(), 2):
        diff = pos1 - pos2
        pos_distance = abs(diff.imag) + abs(diff.real)
        if pos_distance > cheat_len:
            continue
        if abs(pos_d2 - pos_d1) - pos_distance < 100:
            continue
        res += 1
    return res

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        x + (y * 1j): char
        for y, line in enumerate(inp.splitlines())
        for x, char in enumerate(line)
        if char != "#"
    }

def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return path_dist(grid, 2)

def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return path_dist(grid, 20)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
