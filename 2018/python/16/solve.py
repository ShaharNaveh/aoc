import collections
import enum
import itertools
import pathlib
import re
import typing


type Registers = dict[int, int]

PATTERN = re.compile(r"\d+", re.MULTILINE)


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
    opcode: Opcode | int
    a: int
    b: int
    c: int


class Sample(typing.NamedTuple):
    before: Registers
    after: Registers
    instruction: Instruction

    @property
    def matches(self) -> set[Opcode]:
        return {
            opcode
            for opcode in Opcode
            if execute(self.instruction._replace(opcode=opcode), self.before)
            == self.after
        }

    @property
    def raw_opcode(self) -> int:
        return self.instruction.opcode

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        raw_before, raw_instruction, raw_after = itertools.batched(
            map(int, PATTERN.findall(raw)), 4
        )
        before, after = map(lambda t: dict(enumerate(t)), (raw_before, raw_after))
        instruction = Instruction(*raw_instruction)
        return cls(before=before, after=after, instruction=instruction)


def execute(instruction: Instruction, registers: Registers) -> Registers:
    registers = registers.copy()
    opcode, a, b, c = instruction
    match opcode:
        case Opcode.Addr:
            registers[c] = registers[a] + registers[b]
        case Opcode.Addi:
            registers[c] = registers[a] + b
        case Opcode.Mulr:
            registers[c] = registers[a] * registers[b]
        case Opcode.Muli:
            registers[c] = registers[a] * b
        case Opcode.Banr:
            registers[c] = registers[a] & registers[b]
        case Opcode.Bani:
            registers[c] = registers[a] & b
        case Opcode.Borr:
            registers[c] = registers[a] | registers[b]
        case Opcode.Bori:
            registers[c] = registers[a] | b
        case Opcode.Setr:
            registers[c] = registers[a]
        case Opcode.Seti:
            registers[c] = a
        case Opcode.Gtir:
            registers[c] = int(a > registers[b])
        case Opcode.Gtri:
            registers[c] = int(registers[a] > b)
        case Opcode.Gtrr:
            registers[c] = int(registers[a] > registers[b])
        case Opcode.Eqir:
            registers[c] = int(a == registers[b])
        case Opcode.Eqri:
            registers[c] = int(registers[a] == b)
        case Opcode.Eqrr:
            registers[c] = int(registers[a] == registers[b])
    return registers


def find_opcodes(samples: tuple[Sample, ...]) -> dict[int, Opcode]:
    matches = collections.defaultdict(set)
    for sample in samples:
        matches[sample.raw_opcode] |= sample.matches

    res = {}
    while matches:
        key = next(
            raw_opcode for raw_opcode, possible in matches.items() if len(possible) == 1
        )
        hits = matches.pop(key)
        for opcode in matches:
            matches[opcode] -= hits
        res[key] = hits.pop()

    return res


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_samples, raw_test_program = inp.split("\n" * 4)
    samples = tuple(map(Sample.from_str, raw_samples.split("\n" * 2)))
    test_program = [
        list(map(int, line.split())) for line in raw_test_program.splitlines()
    ]
    return samples, test_program


def p1(puzzle_file):
    return sum(len(sample.matches) >= 3 for sample in parse_puzzle(puzzle_file)[0])


def p2(puzzle_file):
    samples, raw_instructions = parse_puzzle(puzzle_file)
    opcodes = find_opcodes(samples)
    registers = {i: 0 for i in range(4)}
    for raw_instruction in raw_instructions:
        raw_opcode, *args = raw_instruction
        instruction = Instruction(opcodes[raw_opcode], *args)
        registers = execute(instruction, registers)

    return registers[0]


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
