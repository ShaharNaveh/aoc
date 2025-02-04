import collections
import pathlib
import re


def calc_next_pos_dir(
    pos: complex, direction: complex, *, bsize: int = 50
) -> tuple[complex, complex]:
    posx, posy = int(pos.real), int(pos.imag)
    bsize2 = bsize * 2
    bsize3 = bsize * 3
    bsize4 = bsize * 4

    #print(f"Got: {pos=} {direction=}")

    #posx , posy = posy, posx
    match direction, posx // bsize, posy // bsize:
        # Right
        case 1, _, 0:
            return complex(bsize2 - 1, bsize3 - 1 - posy), -1
        case 1, _, 1:
            return complex(posy + bsize, bsize - 1), -1j
        case 1, _, 2:
            return complex(bsize3 - 1, bsize3 -1 - posy), -1
        case 1, _, 3:
            return complex(posy - bsize2, bsize3 - 1), -1j

        # Left
        case -1, _, 0:
            #return complex(bsize3 - 1- posy, 0), 1
            return complex(0, bsize3 - 1- posy), 1
        case -1, _, 1:
            #return complex(posx - bsize, bsize2), 1j
            return complex(posy - bsize, bsize2), 1j
            return complex(bsize2, posx - bsize), 1j
            return complex(bsize2, posy - bsize), 1j
            return complex(posy - bsize, bsize2), 1j
        case -1, _, 2:
            #return complex(bsize3 - 1 - posy, bsize), 1
            return complex(bsize, bsize3 - 1 - posy), 1
        case -1, _, 3:
            #return complex(0, posy - bsize2), 1j
            return complex(posy - bsize2, 0), 1j
            #return complex(posx - bsize2, 0), 1j

        # Down
        case 1j, 0, _:
            #print("Down 0")
            #return complex(0, posx + bsize2), 1j
            return complex(posx + bsize2, 0), 1j
        case 1j, 1, _:
            #print("Down 1")
            #return complex(bsize2 + posx, bsize - 1 ), -1
            return complex(bsize - 1, bsize2 + posx), -1
        case 1j, 2, _:
            #print("Down 2")
            #return complex(-bsize + posx, bsize2 - 1), -1
            return complex(bsize2 - 1, -bsize + posx), -1

        # Up
        case -1j, 0, _:
            #print("Up 0")
            #return complex( bsize + posx, bsize), 1
            return complex(bsize, bsize + posx), 1
        case -1j, 1, _:
            #print("Up 1")
            #return complex( bsize2 + posx, 0), 1
            return complex(0, bsize2 + posx), 1
            return complex(0, bsize2 + posx), 1
            return complex(0, bsize2 + posx), 1
        case -1j, 2, _:
            #print("Up 2")
            #return complex(bsize4 - 1, posx - bsize2), -1j
            return complex(posx - bsize2, bsize4 - 1), -1j

        case _:
            raise ValueError((pos, direction))


def walk_p2(start_pos, grid, instructions):
    bsize = int((sum(c in "#." for c in grid.values()) / 6) ** 0.5)

    pos = start_pos
    direction = 1


    l = int(open("a").read())
    i = 0
    for ins in instructions:
        if (False and (i % 100 == 0) ) or(l - 5 <= i <= l + 5):
            print(i, pos, direction)
            print()
        i += 1
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


ROOT_DIR = pathlib.Path(__file__).parent

puzzle_file = ROOT_DIR / "puzzle.txt"
test_puzzle_file = ROOT_DIR / "test_puzzle.txt"

assert (res := p1(test_puzzle_file)) == (expected := 6032), f"{res=} {expected=}"
print(p1(puzzle_file))

#assert (res := p2(test_puzzle_file)) == (expected := 5031), f"{res=} {expected=}"
print(p2(puzzle_file))
