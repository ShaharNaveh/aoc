import collections
import pathlib

OFFSETS = {"N": -1j, "W": -1, "S": 1j, "E": 1}


def find_distances(instructions: str) -> tuple[int, ...]:
    pos = ppos = 0
    locs = []
    distances = collections.defaultdict(int)
    for char in instructions:
        match char:
            case "(":
                locs.append(pos)
            case ")":
                pos = locs.pop()
            case "|":
                pos = locs[-1]
            case _:
                pos += OFFSETS[char]
                dist, pdist = distances[pos], distances[ppos] + 1
                distances[pos] = pdist if dist == 0 else min(dist, pdist)
        ppos = pos

    return tuple(distances.values())


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return inp[1:-1]


def p1(puzzle_file):
    return max(find_distances(parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    return sum(dist >= 1000 for dist in find_distances(parse_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
