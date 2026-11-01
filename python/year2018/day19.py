import enum
import typing
import unittest

from utils import Day, run


@enum.unique
class Opcode(enum.StrEnum):
    Addr = enum.auto()
    Addi = enum.auto()
    Mulr = enum.auto()
    Muli = enum.auto()
    Banr = enum.auto()
    Bani = enum.auto()
    Borr = enum.auto()
    Bori = enum.auto()
    Setr = enum.auto()
    Seti = enum.auto()
    Gtir = enum.auto()
    Gtri = enum.auto()
    Gtrr = enum.auto()
    Eqir = enum.auto()
    Eqri = enum.auto()
    Eqrr = enum.auto()


class Instruction(typing.NamedTuple):
    opcode: Opcode
    args: tuple[int, int, int]

    def run(self, registers: list[int]) -> int:
        opcode, (a, b, c) = self
        match opcode:
            case Opcode.Addr:
                out = registers[a] + registers[b]
            case Opcode.Addi:
                out = registers[a] + b
            case Opcode.Mulr:
                out = registers[a] * registers[b]
            case Opcode.Muli:
                out = registers[a] * b
            case Opcode.Banr:
                out = registers[a] & registers[b]
            case Opcode.Bani:
                out = registers[a] & b
            case Opcode.Borr:
                out = registers[a] | registers[b]
            case Opcode.Bori:
                out = registers[a] | b
            case Opcode.Setr:
                out = registers[a]
            case Opcode.Seti:
                out = a
            case Opcode.Gtir:
                out = int(a > registers[b])
            case Opcode.Gtri:
                out = int(registers[a] > b)
            case Opcode.Gtrr:
                out = int(registers[a] > registers[b])
            case Opcode.Eqir:
                out = int(a == registers[b])
            case Opcode.Eqri:
                out = int(registers[a] == b)
            case Opcode.Eqrr:
                out = int(registers[a] == registers[b])

        return out

    @classmethod
    def from_str(cls, raw: str):
        raw_opcode, *raw_args = raw.split()
        opcode = Opcode(raw_opcode)
        args = tuple(map(int, raw_args))
        return cls(opcode, args)


def execute(
    ip_bounds: int, instructions: tuple[Instruction, ...], *, is_p2: bool = False
) -> int:
    ip = cycle = 0
    registers = [0] * 6
    max_cycles = float("inf")
    if is_p2:
        max_cycles = 10_000
        registers[0] = 1

    while ip < len(instructions):
        registers[ip_bounds] = ip
        instruction = instructions[ip]
        registers[instruction.args[-1]] = instruction.run(registers)
        ip = registers[ip_bounds] + 1
        cycle += 1
        if cycle >= max_cycles:
            break
    return registers


class Day19(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        raw_ip, *raw_instructions = inp.splitlines()
        ip = int(raw_ip.split()[-1])
        instructions = tuple(map(Instruction.from_str, raw_instructions))
        return ip, instructions

    def part1(self, parsed):
        return execute(*parsed)[0]

    def part2(self, parsed):
        max_val = max(execute(*parsed, is_p2=True))
        return sum(i for i in range(1, max_val + 1) if (max_val % i) == 0)


TEST_PUZZLE = """\
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day19()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 6)


if __name__ == "__main__":
    run(Day19)
