import typing
import unittest

from utils import Day, main


class Instruction(typing.NamedTuple):
    op: str
    arg: int

    def __invert__(self) -> "Instruction":
        new_op = {"nop": "jmp", "jmp": "nop"}[self.op]
        return self._replace(op=new_op)

    @classmethod
    def from_str(cls, raw: str) -> "Instruction":
        op, raw_arg = raw.split()
        return cls(op, int(raw_arg))


class Result(typing.NamedTuple):
    is_infinite: bool
    acc: int


def run(instructions: list[Instruction]) -> Result:
    seen = set()
    acc = idx = 0
    while idx < len(instructions):
        if idx in seen:
            return Result(True, acc)
        seen.add(idx)
        ins, arg = instructions[idx]
        match ins:
            case "acc":
                acc += arg
            case "jmp":
                idx += arg
                continue
        idx += 1
    return Result(False, acc)


class Day08(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return list(map(Instruction.from_str, inp.splitlines()))

    def part1(self, parsed):
        _, acc = run(parsed)
        return acc

    def part2(self, instructions):
        for idx, ins in enumerate(instructions):
            if ins.op == "acc":
                continue
            instructions_copy = instructions.copy()
            instructions_copy[idx] = ~ins
            is_infinite, acc = run(instructions_copy)
            if not is_infinite:
                return acc


TEST_PUZZLE = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day08()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 5)

    def test_part2_test_puzzle(self):
        d = Day08()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 8)


if __name__ == "__main__":
    main(Day08)
