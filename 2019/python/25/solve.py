import collections
import enum
import itertools
import pathlib
import queue
import re
import typing


@enum.unique
class Direction(enum.StrEnum):
    North = enum.auto()
    West = enum.auto()
    South = enum.auto()
    East = enum.auto()

    def __neg__(self) -> typing.Self:
        match self:
            case Direction.North:
                return Direction.South
            case Direction.South:
                return Direction.North
            case Direction.East:
                return Direction.West
            case Direction.West:
                return Direction.East


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


@enum.unique
class InstructionMode(enum.IntEnum):
    Position = 0
    Immediate = 1
    Relative = 2


class Intcode:
    def __init__(self, memory: collections.defaultdict[int, int], ip: int = 0):
        self.memory = memory.copy()
        self.ip = ip
        self.relative_base = 0
        self.inputs = queue.Queue()

    def read(self, value: int, mode: InstructionMode) -> int:
        match mode:
            case InstructionMode.Position:
                return self.memory[value]
            case InstructionMode.Immediate:
                return value
            case InstructionMode.Relative:
                return self.memory[self.relative_base + value]

    def write(self, address: int, value: int, mode: InstructionMode) -> None:
        if mode == InstructionMode.Relative:
            address += self.relative_base
        self.memory[address] = value

    def send(self, inps: str) -> None:
        for inp in map(ord, inps + "\n"):
            self.inputs.put(inp)

    def run(self) -> tuple[list[int], bool]:
        outputs = []
        while True:
            instruction = self.memory[self.ip]
            opcode = OpcodeType(instruction % 100)
            modes = tuple(
                map(
                    InstructionMode,
                    (
                        ((instruction // 100) // (10**i)) % 10
                        for i in range(opcode.parameter_count)
                    ),
                )
            )
            params = [
                self.memory[self.ip + i] for i in range(1, opcode.parameter_count + 1)
            ]

            match opcode:
                case OpcodeType.Addition:
                    a, b, _ = (
                        self.read(param, mode) for param, mode in zip(params, modes)
                    )
                    self.write(params[-1], a + b, modes[-1])
                    self.ip += 4

                case OpcodeType.Multiplication:
                    a, b, _ = (
                        self.read(param, mode) for param, mode in zip(params, modes)
                    )
                    self.write(params[-1], a * b, modes[-1])
                    self.ip += 4

                case OpcodeType.Input:
                    recv = self.inputs.get_nowait()
                    self.write(params[0], recv, modes[0])
                    self.ip += 2

                case OpcodeType.Output:
                    recv = self.read(params[0], modes[0])
                    outputs.append(recv)
                    self.ip += 2
                    return outputs, False

                case OpcodeType.Jmp:
                    recv = self.read(params[0], modes[0])
                    if recv != 0:
                        self.ip = self.read(params[1], modes[1])
                    else:
                        self.ip += 3

                case OpcodeType.Jne:
                    recv = self.read(params[0], modes[0])
                    if recv == 0:
                        self.ip = self.read(params[1], modes[1])
                    else:
                        self.ip += 3

                case OpcodeType.Lt:
                    a, b, _ = (
                        self.read(param, mode) for param, mode in zip(params, modes)
                    )
                    recv = int(a < b)
                    self.write(params[-1], recv, modes[-1])
                    self.ip += 4

                case OpcodeType.Eq:
                    a, b, _ = (
                        self.read(param, mode) for param, mode in zip(params, modes)
                    )
                    recv = int(a == b)
                    self.write(params[-1], recv, modes[-1])
                    self.ip += 4

                case OpcodeType.Base:
                    self.relative_base += self.read(params[0], modes[0])
                    self.ip += 2

                case OpcodeType.Halt:
                    break

        return outputs, True

    @property
    def prompt(self) -> tuple[str, bool]:
        prompt = ""
        while True:
            outputs, is_halted = self.run()
            prompt += "".join(map(chr, outputs))
            if is_halted or ("Command?\n" in prompt):
                break
        return prompt, is_halted


def walk(intcode):
    def _walk(
        intcode: Intcode,
        last_direction: Direction | None = None,
        history: tuple[Direction, ...] = (),
    ):
        prompt, _ = intcode.prompt
        chunks = prompt.strip().split("\n" * 2)

        name_chunk = next((chunk for chunk in chunks if chunk.startswith("==")), None)
        name = re.findall(r"== (.*) ==", name_chunk)[0]
        room_paths[name] = history

        doors_chunk = next(
            (chunk for chunk in chunks if chunk.startswith("Doors here lead:")), ""
        )
        directions = tuple(map(Direction, PATTERN.findall(doors_chunk)))

        items_chunk = next(
            (chunk for chunk in chunks if chunk.startswith("Items here:")), ""
        )
        items = PATTERN.findall(items_chunk)

        for item in items:
            if item in BAD_ITEMS:
                continue
            intcode.send(f"take {item}")
            all_items.add(item)
            intcode.prompt

        for direction in directions:
            odirection = -direction
            if odirection == last_direction:
                continue
            intcode.send(direction)
            _walk(intcode, direction, history + (direction,))

            intcode.send(odirection)
            intcode.prompt

    PATTERN = re.compile(r"^- (\w+)*$", re.MULTILINE)
    BAD_ITEMS = (
        "molten lava",
        "photons",
        "giant electromagnet",
        "infinite loop",
        "escape pod",
    )
    all_items, room_paths = set(), {}
    _walk(intcode)

    return intcode, frozenset(all_items), room_paths


def solve(
    intcode: Intcode,
    items: frozenset[str],
    room_paths: dict[str, tuple[Direction, ...]],
) -> int:
    for direction in room_paths["Security Checkpoint"]:
        intcode.send(direction)
        intcode.prompt

    for item in items:
        intcode.send(f"drop {item}")
        intcode.prompt

    direction = room_paths["Pressure-Sensitive Floor"][-1]
    for i in range(1, len(items) + 1):
        for nitems in itertools.permutations(items, r=i):
            for item in nitems:
                intcode.send(f"take {item}")
                intcode.prompt

            intcode.send(direction)
            prompt, is_halted = intcode.prompt
            if is_halted:
                return int(re.findall(r"(\d+)", prompt)[0])

            for item in nitems:
                intcode.send(f"drop {item}")
                intcode.prompt


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return collections.defaultdict(int, enumerate(map(int, inp.split(","))))


def p1(puzzle_file):
    memory = parse_puzzle(puzzle_file)
    return solve(*walk(Intcode(memory)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
