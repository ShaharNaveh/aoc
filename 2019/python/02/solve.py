import itertools
import pathlib


def run(program: list[int]) -> int:
    for idx in range(0, len(program), 4):
        op, *locs, dest = program[idx : idx + 4]
        if op == 99:
            break
        a, b = (program[loc] for loc in locs)
        if op == 1:
            out = a + b
        else:
            out = a * b
        program[dest] = out

    return program[0]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return list(map(int, inp.split(",")))


def p1(puzzle_file):
    program = parse_puzzle(puzzle_file)
    program[1], program[2] = 12, 2
    return run(program)


def p2(puzzle_file):
    original_program = parse_puzzle(puzzle_file)
    for noun, verb in itertools.product(range(100), repeat=2):
        program = original_program.copy()
        program[1], program[2] = noun, verb
        if run(program) == 19690720:
            return 100 * noun + verb


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
