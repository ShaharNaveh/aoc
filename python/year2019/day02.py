import itertools

from utils import Day, aoc_main


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


class Day02(Day):
    def parse(self, input: str):
        inp = input.strip()
        return list(map(int, inp.split(",")))

    def part1(self, program):
        program[1], program[2] = 12, 2
        return run(program)

    def part2(self, original_program):
        for noun, verb in itertools.product(range(100), repeat=2):
            program = original_program.copy()
            program[1], program[2] = noun, verb
            if run(program) == 19690720:
                return 100 * noun + verb


if __name__ == "__main__":
    aoc_main(Day02)
