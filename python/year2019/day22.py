import enum
import re

from utils import Day, run


@enum.unique
class Technique(enum.Enum):
    DealIntoNewStack = enum.auto()
    Cut = enum.auto()
    DealWithIncrement = enum.auto()

    @classmethod
    def from_str(cls, raw: str) -> "Technique":
        if "new" in raw:
            technique = Technique.DealIntoNewStack
        elif raw.startswith("cut"):
            technique = Technique.Cut
        else:
            technique = Technique.DealWithIncrement

        return technique


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        technique = Technique.from_str(line)
        amount = int(next(iter(re.findall(r"-?\d+", line)), 0))
        yield technique, amount


def solve(instructions, cards: int = 10_007, repeats: int = 1, idx: int = 2019):
    mul, diff = 1, 0
    for technique, amount in instructions:
        match technique:
            case Technique.DealIntoNewStack:
                mul = -mul % cards
                diff = (diff + mul) % cards
            case Technique.Cut:
                diff = (diff + amount * mul) % cards
            case Technique.DealWithIncrement:
                mul = (mul * pow(amount, cards - 2, cards)) % cards

    increment = pow(mul, repeats, cards)
    offset = (diff * (1 - increment) * pow((1 - mul) % cards, cards - 2, cards)) % cards

    return (offset + idx * increment) % cards


class Day22(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return solve(parsed)

    def part2(self, parsed):
        return solve(parsed, 119_315_717_514_047, 101_741_582_076_661, 2020)


if __name__ == "__main__":
    run(Day22)
