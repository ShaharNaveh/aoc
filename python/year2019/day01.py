from utils import Day, run


def calc_fuel(mass: int) -> int:
    fuel = (mass // 3) - 2
    if fuel <= 0:
        return 0
    return fuel + calc_fuel(fuel)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(int, inp.splitlines())


class Day01(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum((mass // 3) - 2 for mass in parsed)

    def part2(self, parsed):
        return sum(map(calc_fuel, parsed))


if __name__ == "__main__":
    run(Day01)
