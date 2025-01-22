import copy
import dataclasses
import math
import operator
import pathlib

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

        divisor, if_true, if_false = tuple(int(lines[idx].split()[-1]) for idx in (3, 4, 5))
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

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Monkey.from_str, inp.split("\n" * 2))

def p1(puzzle_file):
    monkeys = list(iter_puzzle(puzzle_file))
    monkeys = simulate(monkeys)
    return calc_monkey_business(monkeys)

def p2(puzzle_file):
    monkeys = list(iter_puzzle(puzzle_file))
    monkeys = simulate(monkeys, 10_000, 1)
    return calc_monkey_business(monkeys)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
