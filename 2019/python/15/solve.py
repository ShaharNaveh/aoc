import enum
import pathlib
import typing


DIRECTIONS = {i: offset for i, offset in enumerate((-1j, 1j, -1, 1), 1)}


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
        memory: dict[int, int],
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
                return memory.get(self.parameter, default_value)
            case InstructionMode.Immediate:
                return self.parameter
            case InstructionMode.Relative:
                return memory[base + self.parameter]


def run(memory: dict[int, int], ip: int = 0, default_value: int | None = None):
    memory = memory.copy()
    base = 0
    while True:
        original_ip = ip
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
                memory,
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
                memory[dest] = a + b
            case OpcodeType.Multiplication:
                a, b, dest = parameters
                memory[dest] = a * b
            case OpcodeType.Input:
                dest = parameters[0]
                memory[dest] = yield ("INPUT", memory, original_ip)
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
    return dict(enumerate(map(int, inp.split(","))))


def scan_area(memory: dict[int, int]) -> tuple[dict, complex, int]:
    program = run(memory)
    pos = 0

    _, mem, ip = next(program)
    seen = {pos: (1, mem, ip, 0)}
    todo = [pos]
    tank = None
    while todo:
        pos = todo.pop(0)
        _, mem, ip, steps = seen[pos]

        for inp, offset in DIRECTIONS.items():
            npos = pos + offset
            if npos in seen:
                continue
            nprogram = run(mem, ip=ip)
            next(nprogram)
            resp = nprogram.send(inp)
            _, nmem, nip = next(nprogram)
            seen[npos] = (resp, nmem, nip, steps + 1)
            if resp == 2:
                tank = npos
                steps_to_tank = steps + 1
            if resp != 0:
                todo.append(npos)
    return seen, tank, steps_to_tank


def p1(puzzle_file):
    _, _, steps = scan_area(parse_puzzle(puzzle_file))
    return steps


def p2(puzzle_file):
    grid, tank, _ = scan_area(parse_puzzle(puzzle_file))

    filled = {tank: 0}
    todo = [tank]
    while todo:
        pos = todo.pop(0)
        for inp, offset in DIRECTIONS.items():
            npos = pos + offset
            if npos in filled:
                continue
            if grid[npos][0] != 1:
                continue
            filled[npos] = filled[pos] + 1
            todo.append(npos)

    return max(filled.values())


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
