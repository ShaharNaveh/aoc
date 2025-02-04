import collections
import enum
import pathlib


@enum.unique
class Direction(complex, enum.Enum):
    North = -1j
    East = 1
    West = -1
    South = 1j
    NorthWest = -1 - 1j
    NorthEast = 1 - 1j
    SouthWest = -1 + 1j
    SouthEast = 1 + 1j


def iter_neigh(pos: complex):
    yield from (pos + direction for direction in Direction)


def simulate(elfs: set[complex]):
    directions = collections.deque(
        [
            (
                Direction.North,
                {Direction.North, Direction.NorthEast, Direction.NorthWest},
            ),
            (
                Direction.South,
                {Direction.South, Direction.SouthEast, Direction.SouthWest},
            ),
            (
                Direction.West,
                {Direction.West, Direction.NorthWest, Direction.SouthWest},
            ),
            (
                Direction.East,
                {Direction.East, Direction.NorthEast, Direction.SouthEast},
            ),
        ]
    )
    while True:
        proposals = collections.defaultdict(set)
        for elf in elfs:
            if all(neigh not in elfs for neigh in iter_neigh(elf)):
                continue
            for direction, offsets in directions:
                if all(elf + offset not in elfs for offset in offsets):
                    proposals[elf + direction].add(elf)
                    break
        directions.rotate(-1)

        for npos, proposers in proposals.items():
            if len(proposers) == 1:
                elfs -= proposers
                elfs.add(npos)

        yield elfs


def calc_empty(elfs: set[complex]) -> int:
    xs = {int(elf.real) for elf in elfs}
    ys = {int(elf.imag) for elf in elfs}

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    area = (abs(max_x - min_x) + 1) * (abs(max_y - min_y) + 1)
    return area - len(elfs)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y)
        for y, row in enumerate(inp.splitlines())
        for x, tile in enumerate(row)
        if tile == "#"
    }


def p1(puzzle_file):
    return calc_empty(
        next(
            elfs
            for i, elfs in enumerate(simulate(parse_puzzle(puzzle_file)), 1)
            if i == 10
        )
    )


def p2(puzzle_file):
    cur = {0}
    prev = {1}
    for i, elfs in enumerate(simulate(parse_puzzle(puzzle_file))):
        if prev == cur:
            return i
        cur, prev = elfs.copy(), cur.copy()


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
