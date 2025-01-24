import itertools
import pathlib
import re

def iter_dead_spaces(sensor: tuple[complex, complex], beacon: tuple[complex, complex]):
    dist = manhattan(sensor, beacon)
    
    x = int(sensor.real)
    y = int(sensor.imag)

    for d in range(dist + 1):
        start = x - dist + d
        stop = x + dist - d + 1

        yield from (complex(nx, y + d) for nx in range(start, stop))
        yield from (complex(nx, y - d) for nx in range(start, stop))
        continue

        yield y + d, range(start, stop)
        yield y - d, range(start, stop)

def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    pattern = re.compile(r"=(-?\d)*")
    for nums in map(pattern.findall, inp.splitlines()):
        sx, sy, bx, by = map(int, nums)
        sensor, beacon = complex(sx, sy), complex(bx, by)
        yield sensor, beacon

def p1(puzzle_file):
    coords = list(iter_puzzle(puzzle_file))
    xs = set(int(pos.real) for pos in itertools.chain.from_iterable(coords))
    min_x, max_x = min(xs), max(xs)





    d = 9
    wanted = 7, range(0, 17 + 1)

    sensor = complex(8, 7)
    beacon = complex(2, 10)
    for a in sorted(iter_dead_spaces(sensor, beacon), key=lambda t: t[0]):
    #for a in iter_dead_spaces(sensor, beacon):
        s = "." * 40
        b = a[1]

        print(a)


def p2(puzzle_file):
    return

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
