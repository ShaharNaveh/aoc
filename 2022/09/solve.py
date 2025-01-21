import pathlib

def calc_offset(dist: complex) -> complex:
    dx = (dist.real > 0) - (dist.real < 0)
    dy = (dist.imag > 0) - (dist.imag < 0)
    return complex(dx, dy)

def simulate(instructions, rope_len: int = 2):
    rope = [0] * rope_len
    for direction, count in instructions:
        for _ in range(count):
            rope[0] += direction
            for idx in range(1, rope_len):
                dist = rope[idx - 1] - rope[idx]
                if 2 > abs(dist):
                    continue
                rope[idx] += calc_offset(dist)
                if idx == rope_len - 1:
                    yield rope[idx]

def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    offsets = {"U": -1j, "D": 1j, "L": -1, "R": 1}
    for line in inp.splitlines():
        char, count = line.split()
        yield offsets[char], int(count)

def p1(puzzle_file):
    instructions = list(iter_puzzle(puzzle_file))
    uniqe_pos = set(simulate(instructions))
    return len(uniqe_pos)

def p2(puzzle_file):
    instructions = list(iter_puzzle(puzzle_file))
    uniqe_pos = set(simulate(instructions, 10))
    return len(uniqe_pos)

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
