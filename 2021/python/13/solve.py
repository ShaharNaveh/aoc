import pathlib
import re


def do_fold(coords: set[complex], fold: complex) -> set[complex]:
    if fold.imag:
        bottom = {pos for pos in coords if pos.imag > fold.imag}
        coords -= bottom
        coords |= {complex(pos.real, (fold.imag * 2) - pos.imag) for pos in bottom}
    else:
        right = {pos for pos in coords if pos.real > fold.real}
        coords -= right
        coords |= {complex((fold.real * 2) - pos.real, pos.imag) for pos in right}

    return coords


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_coords, raw_folds = inp.split("\n" * 2)
    coords = {complex(*map(int, line.split(","))) for line in raw_coords.splitlines()}

    folds = [
        int(val) * {"x": 1, "y": 1j}[axis]
        for axis, val in re.findall(r"(\w)=(\d+)", raw_folds, re.MULTILINE)
    ]
    return coords, folds


def p1(puzzle_file):
    coords, folds = parse_puzzle(puzzle_file)
    return len(do_fold(coords, folds[0]))


def p2(puzzle_file):
    coords, folds = parse_puzzle(puzzle_file)
    for fold in folds:
        coords = do_fold(coords, fold)

    xs = {int(pos.real) for pos in coords}
    ys = {int(pos.imag) for pos in coords}

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    for y in range(min_y, max_y + 1):
        print(
            " ".join(
                "#" if complex(x, y) in coords else "." for x in range(min_x, max_x + 1)
            )
        )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
