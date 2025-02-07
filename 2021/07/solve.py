import functools
import pathlib


@functools.cache
def range_sum(num: int) -> int:
    return num * (num + 1) // 2


def fuel_cost(crabs: tuple[int, ...], n: int) -> int:
    return sum(abs(crab - n) for crab in crabs)


def fuel_cost_p2(crabs: tuple[int, ...], n: int) -> int:
    return sum(range_sum(abs(crab - n)) for crab in crabs)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.split(","))


def p1(puzzle_file):
    crabs = tuple(iter_puzzle(puzzle_file))
    return min(fuel_cost(crabs, n) for n in range(0, max(crabs) + 1))


def p2(puzzle_file):
    crabs = tuple(iter_puzzle(puzzle_file))
    return min(fuel_cost_p2(crabs, n) for n in range(0, max(crabs) + 1))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
