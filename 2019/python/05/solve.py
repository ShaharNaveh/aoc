import enum
import pathlib
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
    Halt = 99

    @property
    def parameter_count(self) -> int:
        match self:
            case OpcodeType.Halt:
                return 0
            case OpcodeType.Input | OpcodeType.Output:
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

    @classmethod
    def from_int(cls, raw: int) -> typing.Self:
        return cls(raw % 100)


@enum.unique
class InstructionMode(enum.IntEnum):
    Position = 0
    Immediate = 1

    @classmethod
    def from_int(cls, raw: int) -> tuple[typing.Self, ...]:
        parameter_count = OpcodeType.from_int(raw).parameter_count
        return tuple(cls((raw // (10**i)) % 10) for i in range(2, parameter_count + 2))


class Instruction(typing.NamedTuple):
    parameter: int
    mode: InstructionMode

    def get_value(self, program: list[int]) -> int:
        match self.mode:
            case InstructionMode.Position:
                return program[self.parameter]
            case InstructionMode.Immediate:
                return self.parameter


def run(program: list[int], inp: int = 1):
    ip = 0
    while program[ip] != OpcodeType.Halt:
        val = program[ip]
        opcode = OpcodeType.from_int(val)
        modes = InstructionMode.from_int(val)

        instructions = [
            Instruction(param, mode)
            for param, mode in zip(
                program[ip + 1 : ip + opcode.parameter_count + 1], modes
            )
        ]

        parameters = tuple(
            instruction.get_value(program) for instruction in instructions
        )
        match opcode:
            case OpcodeType.Addition:
                a, b, _ = parameters
                dest = instructions[-1].parameter
                program[dest] = a + b
            case OpcodeType.Multiplication:
                a, b, _ = parameters
                dest = instructions[-1].parameter
                program[dest] = a * b
            case OpcodeType.Input:
                dest = instructions[0].parameter
                program[dest] = inp
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
                a, b, _ = parameters
                dest = instructions[-1].parameter
                program[dest] = int(a < b)
            case OpcodeType.Eq:
                a, b, _ = parameters
                dest = instructions[-1].parameter
                program[dest] = int(a == b)

        ip += opcode.parameter_count + 1


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return list(map(int, inp.split(",")))


def p1(puzzle_file):
    program = parse_puzzle(puzzle_file)
    return next(out for out in run(program) if out != 0)


def p2(puzzle_file):
    program = parse_puzzle(puzzle_file)
    return next(out for out in run(program, 5) if out != 0)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
