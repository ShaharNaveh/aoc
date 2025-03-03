import enum
import itertools
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


def run(program: dict[int, int], inputs: list[int], default_value: int | None = None):
    program = program.copy()
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


def paint(program: dict[int, int], start_panel: int = 0) -> dict[int, int]:
    panels = {0: start_panel}
    pos, offset = 0, -1j
    inputs = [panels[pos]]

    for color, noffset in itertools.batched(run(program, inputs, default_value=0), 2):
        panels[pos] = color
        offset *= {0: -1j, 1: 1j}[noffset]
        pos += offset
        cpanel = panels.get(pos, 0)
        inputs.append(cpanel)
    return panels


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return dict(enumerate(map(int, inp.split(","))))


def p1(puzzle_file):
    return len(paint(parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    panels = paint(parse_puzzle(puzzle_file), 1)

    xs = {int(pos.real) for pos in panels}
    ys = {int(pos.imag) for pos in panels}

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    return "\n".join(
        " ".join(
            "#" if panels.get(complex(x, y), 0) == 1 else " "
            for x in range(min_x, max_x + 1)
        )
        for y in range(min_y, max_y + 1)
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
