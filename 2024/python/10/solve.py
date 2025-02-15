import pathlib


def available_trails(puzzle):
    trails = [[pos] for pos, height in puzzle.items() if height == 0]
    for height in range(1, 10):
        for trail in trails.copy():
            last_pos = trail[-1]
            direction = -1
            for _ in range(4):
                next_pos = last_pos + direction
                if puzzle.get(next_pos) == height:
                    new_trail = trail + [next_pos]
                    trails.append(new_trail)
                direction *= -1j

        # Trails GC
        trails = [trail for trail in trails if len(trail) >= height + 1]
    return trails


def p1(path):
    puzzle = parse_puzzle(path)
    trails = available_trails(puzzle)
    res = len({(trail[0], trail[-1]) for trail in trails})
    print(res)


def p2(path):
    puzzle = parse_puzzle(path)
    trails = available_trails(puzzle)
    res = len(trails)
    print(res)


def parse_puzzle(path):
    inp = path.read_text().strip().replace(".", "0")
    puzzle = {}
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, num in enumerate(row):
            puzzle[complex(row_idx, col_idx)] = int(num)
    return puzzle


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
