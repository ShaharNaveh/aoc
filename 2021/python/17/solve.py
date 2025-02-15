import itertools
import pathlib
import re


def triangular(n: int) -> int:
    return n * (n + 1) // 2


def inv_triangular(n: int) -> int:
    return int((n * 2) ** 0.5)


def iter_pos(x_bounds: tuple[int, int], y_bounds: tuple[int, int]):
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    for px, py in itertools.product(
        range(inv_triangular(x_min), x_max + 1), range(y_min, -y_min)
    ):
        x = y = 0
        vx, vy = px, py
        while (x <= x_max) and (y >= y_min):
            if (x >= x_min) and (y <= y_max):
                yield x, y
                break

            x += vx
            y += vy

            vy -= 1

            if vx > 0:
                vx -= 1


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(tuple(map(int, t)) for t in re.findall(r"(-?\d+)..(-?\d+)", inp))


def p1(puzzle_file):
    _, y_bounds = parse_puzzle(puzzle_file)
    return triangular(y_bounds[0])


def p2(puzzle_file):
    return sum(1 for _ in iter_pos(*parse_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
