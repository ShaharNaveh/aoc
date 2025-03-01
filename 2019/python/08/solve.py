import itertools
import pathlib


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, list(inp))


def p1(puzzle_file):
    image = tuple(itertools.batched(iter_puzzle(puzzle_file), 25 * 6))
    layer = min(image, key=lambda layer: layer.count(0))
    return layer.count(1) * layer.count(2)


def p2(puzzle_file):
    raw_image = [
        next(str(digit) for digit in layer if digit != 2)
        for layer in zip(*itertools.batched(iter_puzzle(puzzle_file), 25 * 6))
    ]

    trans = str.maketrans({"0": " ", "1": "#"})

    return "\n".join(
        " ".join(row).translate(trans) for row in itertools.batched(raw_image, 25)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
