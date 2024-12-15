import enum
import pathlib

@enum.unique
class Direction(complex, enum.Enum):
    North = (0, -1)
    East = (1, 0)
    South = (0, 1)
    West = (-1, 0)

    @classmethod
    def from_string(cls, char):
        return {
            "^": cls.North,
            ">": cls.East,
            "<": cls.West,
            "v": cls.South,
        }[char]

@enum.unique
class Tile(enum.StrEnum):
    Box = "O"
    Box_E = "]"
    Box_S = "["
    Floor = "."
    Robot = "@"
    Wall = "#"


def simulate(_grid, moves):
    grid = _grid.copy()
    robot = next(pos for pos, tile in grid.items() if tile == Tile.Robot)

    for move in moves:
        movable = []
        locs = [robot]
        while locs:
            loc = locs.pop()
            tile = grid[loc]

            if tile == Tile.Wall:
                break
            elif tile != Tile.Floor:
                movable.append(loc)

                nloc = loc + move
                locs.append(nloc)
                if move.real:
                    continue

                ntile = grid[nloc]
                offset = None
                match ntile:
                    case Tile.Box_S:
                        offset = Direction.East
                    case Tile.Box_E:
                        offset = Direction.West
                if not offset:
                    continue

                locs.append(nloc + offset)
        else:
            seen = set()
            for box in reversed(movable):
                if box in seen:
                    continue
                seen.add(box)
                nbox = box + move
                grid[box], grid[nbox] = grid[nbox], grid[box]

            robot += move

    return grid

def calc_gps(grid):
    for pos, tile in grid.items():
        if tile not in (Tile.Box, Tile.Box_S):
            continue

        yield int(pos.real + (pos.imag * 100))

def parse_puzzle(path, *, is_p2: bool = False):
    inp = path.read_text().strip()
    grid_block, moves_block = inp.split("\n" * 2)

    if is_p2:
        grid_block = grid_block.replace(
            "O", "[]"
        ).replace(".", "..").replace("#", "##").replace("@", "@.")

    grid = {
        x + (y * 1j): Tile(char)
        for y, row in enumerate(grid_block.splitlines())
        for x, char in enumerate(row)
    }

    moves = map(Direction.from_string, moves_block.replace("\n", ""))
    return grid, moves


def p1(path):
    grid, moves = parse_puzzle(path)
    simulated = simulate(grid, moves)
    res = calc_gps(simulated)
    return sum(res)

def p2(path):
    grid, moves = parse_puzzle(path, is_p2=True)
    simulated = simulate(grid, moves)
    res = calc_gps(simulated)
    return sum(res)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
