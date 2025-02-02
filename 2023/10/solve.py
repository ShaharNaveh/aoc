import collections
import enum
import operator
import pathlib


@enum.unique
class Direction(complex, enum.Enum):
    South = (0, 1)
    North = (0, -1)
    East = (1, 0)
    West = (-1, 0)
    Southeast = (1, 1)  # Part 2 only

    def __invert__(self):
        return {
            Direction.South: Direction.North,
            Direction.North: Direction.South,
            Direction.East: Direction.West,
            Direction.West: Direction.East,
        }[self]


PIPE_DIRECTION = {
    "|": {Direction.North, Direction.South},
    "-": {Direction.East, Direction.West},
    "L": {Direction.North, Direction.East},
    "J": {Direction.North, Direction.West},
    "7": {Direction.South, Direction.West},
    "F": {Direction.South, Direction.East},
    "S": {Direction.South, Direction.North, Direction.East, Direction.West},
    ".": set(),
}


def is_pos_inside(pos: complex, mloop, grid, bounds: complex) -> bool:
    npos = pos + Direction.Southeast
    inside = False
    while (bounds.real >= npos.real) and (bounds.imag >= npos.imag):
        if (npos in mloop) and (grid[npos] not in ("L", "7")):
            inside = not inside

        npos += Direction.Southeast
    return inside


def find_main_loop(grid):
    start = next(pos for pos, tile in grid.items() if tile == "S")
    main_loop = collections.defaultdict(lambda: float("inf"))
    todo = {(start, direction, 0) for direction in PIPE_DIRECTION["S"]}
    while todo:
        pos, direction, steps = todo.pop()
        main_loop[pos] = min(steps, main_loop[pos])

        ctile = grid[pos]
        pipe_directions = PIPE_DIRECTION[ctile] - {~direction}
        for ndirection in pipe_directions:
            npos = pos + ndirection
            if steps > main_loop[npos]:
                continue

            ntile = grid.get(npos, ".")
            if ~ndirection not in PIPE_DIRECTION[ntile]:
                continue

            main_loop[npos] = (nsteps := steps + 1)
            todo |= {(npos, ndirection, nsteps)}
    return {k: v for k, v in main_loop.items() if v != float("inf")}


def parse_puzzle(puzzle_file):
    return {
        x + (y * 1j): tile
        for y, line in enumerate(puzzle_file.read_text().strip().splitlines())
        for x, tile in enumerate(line)
    }


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    main_loop = find_main_loop(grid)
    return max(main_loop.values())


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    mloop = set(find_main_loop(grid))

    xs = map(lambda n: int(n.real), mloop)
    ys = map(lambda n: int(n.imag), mloop)
    max_x, max_y = max(xs), max(ys)
    bounds = complex(max_x, max_y)

    poses = set(grid) - mloop
    return sum(is_pos_inside(pos, mloop, grid, bounds) for pos in poses)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")


print(p1(puzzle_file))
print(p2(puzzle_file))
