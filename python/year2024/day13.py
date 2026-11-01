import re

from utils import Day, aoc_main


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    block_pattern = r"""
        (?P<entity>(Button\s[A-Z]|Prize)):\sX[+=]?(?P<X>\d+),\sY[+=]?(?P<Y>\d+)
""".strip()

    reg = re.compile(block_pattern)

    for block in inp.split("\n" * 2):
        entry = {}
        for hit in reg.finditer(block):
            name = hit.group("entity").removeprefix("Button ").lower()
            entry[name] = complex(*tuple(int(hit.group(axis)) for axis in ("X", "Y")))
        yield entry


def play_machine(a: complex, b: complex, prize: complex, *, offset: int = 0):
    prize_x = prize.real + offset
    prize_y = prize.imag + offset
    a_count = ((b.imag * prize_x) - (b.real * prize_y)) / (
        (a.real * b.imag) - (b.real * a.imag)
    )
    b_count = (prize_x - (a.real * a_count)) / b.real
    if not all(n.is_integer() for n in (a_count, b_count)):
        return 0
    tokens = (a_count * 3) + b_count
    return int(tokens)


class Day13(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        res = sum(play_machine(**machine) for machine in parsed)
        return res

    def part2(self, parsed):
        offset = 10_000_000_000_000
        res = sum(play_machine(**machine, offset=offset) for machine in parsed)
        return res


if __name__ == "__main__":
    aoc_main(Day13)
