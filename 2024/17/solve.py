import pathlib
import re

def run(instructions: list[int], a: int, b: int = 0, c: int = 0) -> list[int]:
    pointer = 0
    res = []

    while pointer in range(len(instructions)):
        combo = {4: a, 5: b, 6: c}
        op = instructions[pointer + 1]
        match instructions[pointer]:
            case 0: a >>= combo.get(op, op)
            case 1: b ^= op
            case 2: b = 7 & combo.get(op, op)
            case 3: pointer = op - 2 if a else pointer
            case 4: b ^= c
            case 5: res += [combo.get(op, op) & 7]
            case 6: b = a >> combo.get(op, op)
            case 7: c = a >> combo.get(op, op)
        pointer += 2
    return res

def find_a(ins, b, c):
    possible = [(1, 0)]
    for i, start_a in possible:
        for a in range(start_a, start_a + 8):
            if run(ins, a, b, c) != ins[-i:]:
                continue
            if len(ins) == i:
                return a
            possible += [(i + 1, a * 8)]

def parse_puzzle(path) -> dict:
    inp = path.read_text().strip()
    a, b, c, *ins = map(int, re.findall(r"-?\d+", inp))
    return a, b, c, ins

def p1(path):
    a, b, c, ins = parse_puzzle(path)
    res = run(ins, a, b, c)
    return ",".join(map(str, res))

def p2(path):
    _, b, c, ins = parse_puzzle(path)
    return find_a(ins, b, c)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
