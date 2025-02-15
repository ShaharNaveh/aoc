import functools
import pathlib


@functools.cache
def simulate(timer: int, days: int = 80) -> int:
    if 0 >= days - timer:
        return 1

    ndays = days - 1
    ntimer = timer - 1

    if ntimer >= 0:
        return simulate(ntimer, ndays)
    else:
        return simulate(6, ndays) + simulate(8, ndays)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.split(","))


def p1(puzzle_file):
    return sum(map(simulate, iter_puzzle(puzzle_file)))


def p2(puzzle_file):
    return sum(simulate(timer, 256) for timer in iter_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
