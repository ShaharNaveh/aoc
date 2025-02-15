import pathlib


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for line in inp.splitlines():
        direction, count = line.split()
        offset = {"forward": 1, "up": -1j, "down": 1j}[direction]
        yield int(count) * offset


def p1(puzzle_file):
    pos = sum(iter_puzzle(puzzle_file))
    return int(pos.real * pos.imag)


def p2(puzzle_file):
    pos = aim = 0
    for offset in iter_puzzle(puzzle_file):
        aim += offset.imag
        pos += offset.real + (offset.real * aim * 1j)

    return int(pos.real * pos.imag)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
