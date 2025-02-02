import itertools
import pathlib


def pour_sand(
    rocks: set[complex],
    min_x: int,
    max_x: int,
    max_y: int,
    *,
    pos: complex = 500,
) -> complex | None:
    if (max_x < pos.real < min_x) or (pos.imag > max_y):
        return None

    for offset in (1j, -1 + 1j, 1 + 1j):
        npos = pos + offset
        if npos not in rocks:
            return pour_sand(rocks, pos=npos, min_x=min_x, max_x=max_x, max_y=max_y)
    return pos


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for line in inp.splitlines():
        paths = [complex(*map(int, path.split(","))) for path in line.split(" -> ")]
        yield from paths
        for a, b in itertools.pairwise(paths):
            dist = b - a
            if dist.real:
                offset = dist.real / abs(dist.real)
            else:
                offset = (dist.imag / abs(dist.imag)) * 1j

            for pos in itertools.count(a, offset):
                if pos == b:
                    break
                yield pos


def p1(puzzle_file):
    rocks = set(iter_puzzle(puzzle_file))
    rocks_len = len(rocks)
    xs = set(rock.real for rock in rocks)
    min_x, max_x = min(xs), max(xs)
    max_y = max(rock.imag for rock in rocks)

    while (sand := pour_sand(rocks, min_x=min_x, max_x=max_x, max_y=max_y)) is not None:
        rocks.add(sand)

    return len(rocks) - rocks_len


def p2(puzzle_file):
    rocks = set(iter_puzzle(puzzle_file))
    max_y = max(int(rock.imag) for rock in rocks) + 2

    xs = set(int(rock.real) for rock in rocks)
    min_x, max_x = min(xs), max(xs)

    min_x *= -max_y
    max_x *= max_y + 1

    for x in range(min_x, max_x):
        rocks.add(complex(x, max_y))

    for i in itertools.count(1):
        sand = pour_sand(rocks, min_x=-float("inf"), max_x=float("inf"), max_y=max_y)
        if sand == 500:
            return i
        rocks.add(sand)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
