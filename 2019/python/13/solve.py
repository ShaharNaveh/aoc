import enum
import itertools
import pathlib
import typing


@enum.unique
class TileType(enum.IntEnum):
    Empty = 0
    Walll = 1
    Block = 2
    Paddle = 3
    Ball = 4

    def can_break(self, other: "TileType") -> bool:
        match other:
            case TileType.Empty:
                return True
            case TileType.Wall:
                return False
            case TileType.Block:
                pass
            case TileType.Paddle:
                pass


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
        self,
        program: dict[int, int],
        base: int,
        is_writer: bool = False,
        default_value: int | None = None,
    ) -> int:
        if is_writer:
            if self.mode == InstructionMode.Relative:
                return base + self.parameter
            return self.parameter

        match self.mode:
            case InstructionMode.Position:
                return program.get(self.parameter, default_value)
            case InstructionMode.Immediate:
                return self.parameter
            case InstructionMode.Relative:
                return program[base + self.parameter]


def run(
    program: dict[int, int],
    inputs: list[int] | None = None,
    default_value: int | None = None,
):
    program = program.copy()
    inputs = inputs if inputs else []
    inps = iter(inputs)
    ip = base = 0
    while True:
        val = program[ip]
        opcode = OpcodeType.from_int(val)
        modes = InstructionMode.from_int(val)

        instructions = [
            Instruction(param, mode)
            for param, mode in zip(
                (program[i] for i in range(ip + 1, ip + opcode.parameter_count + 1)),
                modes,
            )
        ]

        parameters = tuple(
            instruction.get_value(
                program,
                base,
                is_writer=(i == len(instructions)) and opcode.is_writer,
                default_value=default_value,
            )
            for i, instruction in enumerate(instructions, 1)
        )
        match opcode:
            case OpcodeType.Halt:
                break
            case OpcodeType.Addition:
                a, b, dest = parameters
                program[dest] = a + b
            case OpcodeType.Multiplication:
                a, b, dest = parameters
                program[dest] = a * b
            case OpcodeType.Input:
                dest = parameters[0]
                program[dest] = next(inps)
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
                program[dest] = int(a < b)
            case OpcodeType.Eq:
                a, b, dest = parameters
                program[dest] = int(a == b)
            case OpcodeType.Base:
                base += parameters[0]

        ip += opcode.parameter_count + 1


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return dict(enumerate(map(int, inp.split(","))))


def p1(puzzle_file):
    return len(
        {
            complex(x, y)
            for x, y, tile_id in itertools.batched(run(parse_puzzle(puzzle_file)), 3)
            if TileType(tile_id) == TileType.Block
        }
    )


def p2(puzzle_file):
    return


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
