import pathlib
import re


def calc_next_pos_dir(
    pos: complex, direction: complex, *, bsize: int = 50
) -> tuple[complex, complex]:
    posx, posy = int(pos.real), int(pos.imag)
    bsize2 = bsize * 2
    bsize3 = bsize * 3
    bsize4 = bsize * 4
    match direction, posx // bsize, posy // bsize:
        case 1, _, 0:
            return complex(bsize2 - 1, bsize3 - 1 - posy), -1
        case 1, _, 1:
            return complex(posy + bsize, bsize - 1), -1j
        case 1, _, 2:
            return complex(bsize3 - 1, bsize3 - 1 - posy), -1
        case 1, _, 3:
            return complex(posy - bsize2, bsize3 - 1), -1j

        case -1, _, 0:
            return complex(0, bsize3 - 1 - posy), 1
        case -1, _, 1:
            return complex(posy - bsize, bsize2), 1j
        case -1, _, 2:
            return complex(bsize, bsize3 - 1 - posy), 1
        case -1, _, 3:
            return complex(posy - bsize2, 0), 1j

        case 1j, 0, _:
            return complex(posx + bsize2, 0), 1j
        case 1j, 1, _:
            return complex(bsize - 1, bsize2 + posx), -1
        case 1j, 2, _:
            return complex(bsize2 - 1, -bsize + posx), -1

        case -1j, 0, _:
            return complex(bsize, bsize + posx), 1
        case -1j, 1, _:
            return complex(0, bsize2 + posx), 1
        case -1j, 2, _:
            return complex(posx - bsize2, bsize4 - 1), -1j


def walk_p2(start_pos, grid, instructions):
    bsize = int((sum(c in "#." for c in grid.values()) / 6) ** 0.5)

    pos = start_pos
    direction = 1

    for ins in instructions:
        match ins:
            case "L":
                direction *= -1j
            case "R":
                direction *= 1j
            case _:
                for _ in range(ins):
                    npos = pos + direction
                    ntile = grid.get(npos)
                    ndirection = direction

                    if grid.get(npos) is None:
                        npos, ndirection = calc_next_pos_dir(
                            npos, direction, bsize=bsize
                        )
                    if grid.get(npos) == ".":
                        pos, direction = npos, ndirection

    return pos, direction


def walk(start_pos, grid, instructions):
    pos = start_pos
    direction = 1
    for ins in instructions:
        match ins:
            case "L":
                direction *= -1j
            case "R":
                direction *= 1j
            case _:
                for _ in range(ins):
                    pos += direction
                    tile = grid.get(pos)
                    if tile == ".":
                        continue

                    if tile == "#":
                        pos -= direction
                        break

                    odirection = direction * -1
                    npos = pos + odirection
                    while grid.get(npos):
                        npos += odirection

                    npos -= odirection
                    if grid[npos] == "#":
                        pos -= direction
                        break
                    pos = npos

    return pos, direction


def calc_password(pos: complex, direction: complex) -> int:
    row = int(pos.imag) + 1
    column = int(pos.real) + 1
    d = {1: 0, 1j: 1, -1: 2, -1j: 3}[direction]
    return (row * 1000) + (column * 4) + d


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().rstrip()
    raw_grid, raw_instructions = inp.split("\n" * 2)

    start_pos = raw_grid.index(".")
    grid = {
        complex(x, y): tile
        for y, row in enumerate(raw_grid.splitlines())
        for x, tile in enumerate(row)
        if tile != " "
    }

    instructions = tuple(
        int(ins) if ins.isdigit() else ins
        for ins in re.findall(r"\d+|\w", raw_instructions)
    )

    return start_pos, grid, instructions


def p1(puzzle_file):
    start_pos, grid, instructions = parse_puzzle(puzzle_file)
    return calc_password(*walk(start_pos, grid, instructions))


def p2(puzzle_file):
    start_pos, grid, instructions = parse_puzzle(puzzle_file)
    return calc_password(*walk_p2(start_pos, grid, instructions))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
