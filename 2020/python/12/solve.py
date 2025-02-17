import operator
import pathlib
import re
import typing

DIRECTIONS = list("ESWN")
ROTATIONS = {"L": operator.sub, "R": operator.add}


class Pos(typing.NamedTuple):
    x: int = 0
    y: int = 0

    def move(self, direction: str, amount: int) -> "Pos":
        x, y = self
        match direction:
            case "N":
                y += amount
            case "S":
                y -= amount
            case "E":
                x += amount
            case "W":
                x -= amount
        return Pos(x, y)

    @property
    def distance(self) -> int:
        return sum(map(abs, self))


def iter_puzzle(puzzle_file) -> dict[complex, bool]:
    inp = puzzle_file.read_text().strip()
    pattern = re.compile(r"(\w)(\d+)", re.MULTILINE)
    yield from map(lambda ins: (ins[0], int(ins[1])), pattern.findall(inp))


def p1(puzzle_file):
    pos = Pos()
    facing = "E"
    for direction, amount in iter_puzzle(puzzle_file):
        match direction:
            case "F":
                pos = pos.move(facing, amount)
            case "L" | "R":
                op = ROTATIONS[direction]
                cdirection = DIRECTIONS.index(facing)
                idx = op(cdirection, amount // 90) % 4
                facing = DIRECTIONS[idx]
            case _:
                pos = pos.move(direction, amount)
    return pos.distance


def p2(puzzle_file):
    pos = Pos()
    wp = Pos(10, 1)
    for direction, amount in iter_puzzle(puzzle_file):
        match direction:
            case "F":
                nx = pos.x + (wp.x * amount)
                ny = pos.y + (wp.y * amount)
                pos = Pos(nx, ny)
            case "L" | "R":
                amount //= 90
                for _ in range(amount):
                    if direction == "L":
                        wp = Pos(-wp.y, wp.x)
                    else:
                        wp = Pos(wp.y, -wp.x)
            case _:
                wp = wp.move(direction, amount)
    return pos.distance


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
