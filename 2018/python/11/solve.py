import collections
import itertools
import pathlib


MAX_GRID_SIZE = 300
type PrefixSum = collections.defaultdict[complex, int]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return int(inp)


def find_power_level(pos: complex, serial_number: int) -> int:
    x, y = map(int, (pos.real, pos.imag))
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = power_level // 100 % 10
    return power_level - 5


def build_prefix_sum(serial_number: int, grid_size: int = MAX_GRID_SIZE) -> PrefixSum:
    res = collections.defaultdict(int)
    for pos in itertools.starmap(
        complex, itertools.product(range(1, grid_size + 1), repeat=2)
    ):
        res[pos] = (
            find_power_level(pos, serial_number)
            + res[pos - 1]
            + res[pos - 1j]
            - res[pos - 1 - 1j]
        )
    return res


def find_grid_power_level(pos: complex, grid_size: int, prefix_sum: PrefixSum) -> int:
    return (
        prefix_sum[pos + complex(grid_size, grid_size)]
        - prefix_sum[complex(pos.real, pos.imag + grid_size)]
        - prefix_sum[complex(pos.real + grid_size, pos.imag)]
        + prefix_sum[pos]
    )


def p1(puzzle_file):
    serial_number = parse_puzzle(puzzle_file)
    prefix_sum = build_prefix_sum(serial_number)
    grid_size = 3

    pos = max(
        itertools.starmap(
            complex, itertools.product(range(MAX_GRID_SIZE - grid_size + 1), repeat=2)
        ),
        key=lambda pos: find_grid_power_level(pos, grid_size, prefix_sum),
    )
    return ",".join(map(str, map(int, (pos.real, pos.imag))))


def p2(puzzle_file):
    serial_number = parse_puzzle(puzzle_file)
    prefix_sum = build_prefix_sum(serial_number)
    pos, grid_size = max(
        (
            (pos, grid_size)
            for grid_size in range(1, MAX_GRID_SIZE)
            for pos in itertools.starmap(
                complex,
                itertools.product(range(1, MAX_GRID_SIZE - grid_size + 1), repeat=2),
            )
        ),
        key=lambda tup: find_grid_power_level(*tup, prefix_sum),
    )
    return ",".join(map(str, map(int, (pos.real + 1, pos.imag + 1, grid_size))))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
