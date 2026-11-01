import copy
import dataclasses
import math
import operator
import unittest

from utils import Day, run

OPS = {"+": operator.add, "*": operator.mul}


@dataclasses.dataclass(slots=True)
class Monkey:
    _id: int
    op: callable
    divisor: int
    branches: tuple[int, int]
    items: list[int] = dataclasses.field(default_factory=list)
    score: int = dataclasses.field(init=False, default=0)

    @classmethod
    def from_str(cls, block: str):
        lines = block.splitlines()

        _id = int(lines[0].removesuffix(":").split()[-1])

        items = list(map(int, lines[1].split(":")[-1].split(",")))

        op_str, val = lines[2].split("= old")[-1].split()
        op_callable = {"+": operator.add, "*": operator.mul}[op_str]
        if val == "old":
            func = operator.pow
            val = 2
        else:
            func = OPS[op_str]
            val = int(val)
        op = lambda n: func(n, val)

        divisor, if_true, if_false = tuple(
            int(lines[idx].split()[-1]) for idx in (3, 4, 5)
        )
        branches = (if_false, if_true)

        return cls(_id=_id, items=items, op=op, divisor=divisor, branches=branches)


def simulate(
    monkeys: list[Monkey],
    rounds: int = 20,
    relief: int = 3,
) -> list[Monkey]:
    monkeys = copy.deepcopy(monkeys)
    minimizer = math.lcm(*map(operator.attrgetter("divisor"), monkeys))
    monkeys = sorted(monkeys, key=operator.attrgetter("_id"))

    for _ in range(rounds):
        for monkey in monkeys:
            monkey.score += len(monkey.items)

            for item in monkey.items:
                item = (monkey.op(item) // relief) % minimizer
                branches = monkey.branches
                dest = branches[item % monkey.divisor == 0]
                monkeys[dest].items.append(item)
            monkey.items.clear()
    return monkeys


def calc_monkey_business(monkeys: list[Monkey]) -> int:
    return math.prod(
        sorted(map(operator.attrgetter("score"), monkeys), reverse=True)[:2]
    )


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(Monkey.from_str, inp.split("\n" * 2))


class Day11(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        monkeys = list(parsed)
        monkeys = simulate(monkeys)
        return calc_monkey_business(monkeys)

    def part2(self, parsed):
        monkeys = list(parsed)
        monkeys = simulate(monkeys, 10_000, 1)
        return calc_monkey_business(monkeys)


TEST_PUZZLE = """\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 10605)

    def test_part2_test_puzzle(self):
        d = Day11()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 2713310158)


if __name__ == "__main__":
    run(Day11)
