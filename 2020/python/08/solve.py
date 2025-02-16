import pathlib
import typing


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


def parse_puzzle(puzzle_file) -> list[Instruction]:
    inp = puzzle_file.read_text().strip()
    return list(map(Instruction.from_str, inp.splitlines()))


def p1(puzzle_file):
    _, acc = run(parse_puzzle(puzzle_file))
    return acc


def p2(puzzle_file):
    instructions = parse_puzzle(puzzle_file)
    for idx, ins in enumerate(instructions):
        if ins.op == "acc":
            continue
        instructions_copy = instructions.copy()
        instructions_copy[idx] = ~ins
        is_infinite, acc = run(instructions_copy)
        if not is_infinite:
            return acc


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
