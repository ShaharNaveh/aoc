import pathlib


def calc_fuel(mass: int) -> int:
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    return fuel + calc_fuel(fuel)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.splitlines())


def p1(puzzle_file):
    return sum((mass // 3) - 2 for mass in iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return sum(map(calc_fuel, iter_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
