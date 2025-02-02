import enum
import pathlib


@enum.unique
class Direction(complex, enum.Enum):
    North = (0, -1)
    South = (0, 1)
    West = (-1, 0)
    East = (1, 0)


def count_energized(
    grid: dict[complex, str],
    start_pos: complex = 0,
    start_direction: Direction = Direction.East,
) -> int:
    queue = [(start_pos, start_direction)]
    seen = set()
    while queue:
        state = queue.pop()
        if state in seen:
            continue

        pos, direction = state
        if not (tile := grid.get(pos)):
            continue

        seen.add(state)

        if (
            (tile == ".")
            or ((tile == "|") and (direction in (Direction.North, Direction.South)))
            or ((tile == "-") and (direction in (Direction.West, Direction.East)))
        ):
            next_states = [(pos + direction, direction)]
        elif tile == "|":
            next_states = [
                (pos + Direction.North, Direction.North),
                (pos + Direction.South, Direction.South),
            ]
        elif tile == "-":
            next_states = [
                (pos + Direction.West, Direction.West),
                (pos + Direction.East, Direction.East),
            ]

        elif tile == "/":
            match direction:
                case Direction.North:
                    next_states = [(pos + Direction.East, Direction.East)]
                case Direction.South:
                    next_states = [(pos + Direction.West, Direction.West)]
                case Direction.East:
                    next_states = [(pos + Direction.North, Direction.North)]
                case Direction.West:
                    next_states = [(pos + Direction.South, Direction.South)]
        elif tile == "\\":
            match direction:
                case Direction.North:
                    next_states = [(pos + Direction.West, Direction.West)]
                case Direction.South:
                    next_states = [(pos + Direction.East, Direction.East)]
                case Direction.East:
                    next_states = [(pos + Direction.South, Direction.South)]
                case Direction.West:
                    next_states = [(pos + Direction.North, Direction.North)]

        queue.extend(next_states)

    unique_pos = {pos for pos, _ in seen}
    return len(unique_pos)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): tile
        for y, line in enumerate(inp.splitlines())
        for x, tile in enumerate(line)
    }


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return count_energized(grid)


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    max_x = int(max(pos.real for pos in grid))
    max_y = int(max(pos.imag for pos in grid))

    todo = set()
    for y in range(max_y + 1):
        todo.add((complex(0, y), Direction.East))
        todo.add((complex(max_x, y), Direction.West))

    for x in range(max_x + 1):
        todo.add((complex(x, 0), Direction.South))
        todo.add((complex(x, max_y), Direction.North))

    return max(count_energized(grid, *state) for state in todo)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
