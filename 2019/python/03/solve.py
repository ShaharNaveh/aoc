import pathlib


def iter_pos(offsets: tuple[tuple[complex, int]]):
    pos = 0
    for offset, amount in offsets:
        for _ in range(amount):
            pos += offset
            yield pos


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    return tuple(
        tuple(
            ({"L": -1, "D": 1j, "R": 1, "U": -1j}[offset[0]], int(offset[1:]))
            for offset in offsets.split(",")
        )
        for offsets in inp.splitlines()
    )


def p1(puzzle_file):
    wires = parse_puzzle(puzzle_file)
    wire1, wire2 = (set(iter_pos(offsets)) for offsets in parse_puzzle(puzzle_file))
    return int(min(abs(pos.real) + abs(pos.imag) for pos in (wire1 & wire2)))


def p2(puzzle_file):
    wires = parse_puzzle(puzzle_file)
    wire1, wire2 = (list(iter_pos(offsets)) for offsets in parse_puzzle(puzzle_file))
    intersection = set(wire1) & set(wire2)
    return min(wire1.index(pos) + wire2.index(pos) for pos in intersection) + 2


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
