import collections
import enum
import heapq
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


def run(
    memory: dict[int, int], inputs=None, ip: int = 0, default_value: int | None = None
):
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
                memory[dest] = next(inputs)
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


def build_grid(program) -> dict[complex, str]:
    image = "".join(map(chr, run(parse_puzzle(puzzle_file))))
    return {
        complex(x, y): tile
        for y, row in enumerate(image.splitlines())
        for x, tile in enumerate(row)
        if tile != "."
    }


class Branch(typing.NamedTuple):
    pos: complex
    offset: complex
    visited: frozenset[complex]
    path: list[str]
    priority: int

    def __lt__(self, other) -> bool:
        return self.priority < other.priority


def find_path(grid: dict[complex, str]) -> list[str]:
    start_pos = next(pos for pos, tile in grid.items() if tile == "^")
    start_offset = -1j
    walkable = frozenset(grid)
    TOTAL = len(walkable)
    pq = [Branch(start_pos, -1j, frozenset({start_pos}), [], TOTAL)]
    while pq:
        pos, offset, visited, path, priority = heapq.heappop(pq)

        if visited == walkable:
            raw_path = path
            break

        npos = pos + offset
        if npos in walkable:
            nvisited = visited.copy() | {npos}
            heapq.heappush(
                pq,
                Branch(
                    npos, offset, nvisited, path.copy() + ["1"], TOTAL - len(nvisited)
                ),
            )

        for n, s in ((-1j, "L"), (1j, "R")):
            noffset = offset * n
            heapq.heappush(
                pq,
                Branch(pos, noffset, visited, path.copy() + [s], priority),
            )

    return tuple(
        key if key in "LR" else str(len(list(group)))
        for key, group in itertools.groupby(raw_path)
    )


def find_functions(moves) -> tuple[str, str, str]:
    for la in range(2, 11):
        func_a = moves[:la]
        sb = la

        while moves[sb:][:la] == func_a:
            sb += la

        for lb in range(2, 11):
            func_b = moves[sb : sb + lb]
            sc = sb + lb

            while 1:
                if moves[sc:][:la] == func_a:
                    sc += la
                elif moves[sc:][:lb] == func_b:
                    sc += lb
                else:
                    break

            for lc in range(2, 11):
                func_c = moves[sc : sc + lc]
                ok = True
                i = sc

                while i < len(moves):
                    if moves[i:][:la] == func_a:
                        i += la
                    elif moves[i:][:lb] == func_b:
                        i += lb
                    elif moves[i:][:lc] == func_c:
                        i += lc
                    else:
                        ok = False
                        break

                if ok:
                    A, B, C = (",".join(f) for f in (func_a, func_b, func_c))
                    if all(len(x) <= 20 for x in (A, B, C)):
                        return A, B, C


def p1(puzzle_file):
    grid = build_grid(run(parse_puzzle(puzzle_file)))
    return int(
        sum(
            pos.real * pos.imag
            for pos, tile in grid.items()
            if (tile == "#")
            and all(grid.get(pos + offset) == "#" for offset in (1, -1, 1j, -1j))
        )
    )


def p2(puzzle_file):
    memory = parse_puzzle(puzzle_file)
    grid = build_grid(run(memory))
    path = find_path(grid)
    A, B, C = find_functions(path)

    main = ",".join(path)
    for old, new in ((A, "A"), (B, "B"), (C, "C")):
        main = main.replace(old, new)

    inputs = map(ord, "\n".join((main, A, B, C, "n", "")))
    memory[0] = 2
    return collections.deque(run(memory, inputs), maxlen=1)[0]


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
