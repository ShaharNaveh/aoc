import itertools
import pathlib
import re

def calc_dead_space(
        sensor: tuple[complex, complex], beacon: tuple[complex, complex], y: int
    ) -> range | None:
    dist = manhattan(sensor, beacon)
    sx, sy = int(sensor.real), int(sensor.imag)
    y_dist = abs(y - sy)
    print(f"Y={y}\t{sensor=}\t{beacon=}\t{dist=}\t{y_dist=}")

    if y_dist > dist:
        return None
    return range(sx - dist + y_dist, sx + dist - y_dist + 1)
    #return range(sx - y_dist + dist, sx - y_dist + dist + 1)
    '''
    for d in range(dist + 1):
        start = sx - dist + d
        stop = sx + dist - d + 1
        yield from (complex(nx, sy + d) for nx in range(start, stop))
        yield from (complex(nx, sy - d) for nx in range(start, stop))
    '''
def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    pattern = re.compile(r"=(-?\d*)")
    for nums in map(pattern.findall, inp.splitlines()):
        sx, sy, bx, by = map(int, nums)
        sensor, beacon = complex(sx, sy), complex(bx, by)
        yield sensor, beacon

def p1(puzzle_file):
    sensor = 8 + 7j
    beacon = 2 + 10j
    print(calc_dead_space(sensor, beacon, 16))
    print(calc_dead_space(sensor, beacon, 15))
    print(calc_dead_space(sensor, beacon, -1))
    return

    Y = 2_000_000
    coords = set(iter_puzzle(puzzle_file))
    beacons = {beacon for _, beacon in coords}
    '''
    dead_pos = {
        pos for pos 
        in itertools.chain.from_iterable(iter_dead_spaces(*pair) for pair in coords)
        if pos.imag == Y
    }
    return len(dead_pos - beacons)
    '''

def p2(puzzle_file):
    return

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
