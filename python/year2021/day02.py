from utils import Day, run


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        direction, count = line.split()
        offset = {"forward": 1, "up": -1j, "down": 1j}[direction]
        yield int(count) * offset


class Day02(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        pos = sum(parsed)
        return int(pos.real * pos.imag)

    def part2(self, parsed):
        pos = aim = 0
        for offset in parsed:
            aim += offset.imag
            pos += offset.real + (offset.real * aim * 1j)

        return int(pos.real * pos.imag)


if __name__ == "__main__":
    run(Day02)
