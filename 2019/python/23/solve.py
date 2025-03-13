import collections
import enum
import itertools
import pathlib

# import queue
import typing


@enum.unique
class OpcodeType(enum.IntEnum):
    Addition = 1
    Multiplication = 2
    Input = 3
    Output = 4
    Jmp = 5
    Jne = 6
    Lt = 7
    Eq = 8
    Base = 9
    Halt = 99

    @property
    def parameter_count(self) -> int:
        match self:
            case OpcodeType.Halt:
                return 0
            case OpcodeType.Input | OpcodeType.Output | OpcodeType.Base:
                return 1
            case OpcodeType.Jmp | OpcodeType.Jne:
                return 2
            case (
                OpcodeType.Addition
                | OpcodeType.Multiplication
                | OpcodeType.Lt
                | OpcodeType.Eq
            ):
                return 3

    @property
    def is_writer(self) -> bool:
        return self in (
            OpcodeType.Addition,
            OpcodeType.Multiplication,
            OpcodeType.Input,
            OpcodeType.Lt,
            OpcodeType.Eq,
        )

    @classmethod
    def from_int(cls, raw: int) -> typing.Self:
        return cls(raw % 100)


@enum.unique
class InstructionMode(enum.IntEnum):
    Position = 0
    Immediate = 1
    Relative = 2

    @classmethod
    def from_int(cls, raw: int) -> tuple[typing.Self, ...]:
        parameter_count = OpcodeType.from_int(raw).parameter_count
        return tuple(cls((raw // (10**i)) % 10) for i in range(2, parameter_count + 2))


class Instruction(typing.NamedTuple):
    parameter: int
    mode: InstructionMode

    def get_value(
        self, memory: dict[int, int], base: int, is_writer: bool = False
    ) -> int:
        if is_writer:
            if self.mode == InstructionMode.Relative:
                return base + self.parameter
            return self.parameter

        match self.mode:
            case InstructionMode.Position:
                return memory[self.parameter]
            case InstructionMode.Immediate:
                return self.parameter
            case InstructionMode.Relative:
                return memory[base + self.parameter]


def run(memory: dict[int, int], inputs: collections.deque | None = None, ip: int = 0):
    memory = memory.copy()
    inputs = inputs if inputs is not None else collections.deque()
    base = 0
    while True:
        val = memory[ip]
        opcode = OpcodeType.from_int(val)
        modes = InstructionMode.from_int(val)

        instructions = [
            Instruction(param, mode)
            for param, mode in zip(
                (memory[i] for i in range(ip + 1, ip + opcode.parameter_count + 1)),
                modes,
            )
        ]

        parameters = tuple(
            instruction.get_value(
                memory, base, is_writer=(i == len(instructions)) and opcode.is_writer
            )
            for i, instruction in enumerate(instructions, 1)
        )
        match opcode:
            case OpcodeType.Halt:
                break
            case OpcodeType.Addition:
                a, b, dest = parameters
                memory[dest] = a + b
            case OpcodeType.Multiplication:
                a, b, dest = parameters
                memory[dest] = a * b
            case OpcodeType.Input:
                dest = parameters[0]
                if len(inputs) == 0:
                    recv = -1
                    yield None
                else:
                    recv = inputs.popleft()
                memory[dest] = recv
            case OpcodeType.Output:
                yield from parameters
            case OpcodeType.Jmp:
                a, b = parameters
                if a != 0:
                    ip = b
                    continue
            case OpcodeType.Jne:
                a, b = parameters
                if a == 0:
                    ip = b
                    continue
            case OpcodeType.Lt:
                a, b, dest = parameters
                memory[dest] = int(a < b)
            case OpcodeType.Eq:
                a, b, dest = parameters
                memory[dest] = int(a == b)
            case OpcodeType.Base:
                base += parameters[0]

        ip += opcode.parameter_count + 1


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return collections.defaultdict(int, enumerate(map(int, inp.split(","))))


def init_network(memory):
    inputs = {pc: collections.deque([pc]) for pc in range(50)}
    programs = {pc: run(memory, q) for pc, q in inputs.items()}
    for pc, q in inputs.items():
        next(programs[pc])

    return programs, inputs


def p1(puzzle_file):
    programs, inputs = init_network(parse_puzzle(puzzle_file))

    while True:
        for pc, q in inputs.items():
            prog = programs[pc]
            for out in itertools.batched(prog, 3):
                if None in out:
                    break
                addr, x, y = out
                if addr == 255:
                    return y
                inputs[addr].extend([x, y])


def p2(puzzle_file):
    programs, inputs = init_network(parse_puzzle(puzzle_file))

    lnaty = natx = naty = None
    while True:
        for pc, q in inputs.items():
            prog = programs[pc]
            for out in itertools.batched(prog, 3):
                if None in out:
                    break
                addr, x, y = out
                if addr == 255:
                    natx, naty = x, y
                    continue
                inputs[addr].extend([x, y])
        if sum(map(len, inputs.values())) == 0:
            if naty == lnaty:
                return lnaty
            inputs[0].extend([natx, naty])
            lnaty = naty


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
