from utils import Day, main


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


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    offsets = {"U": -1j, "D": 1j, "L": -1, "R": 1}
    for line in inp.splitlines():
        char, count = line.split()
        yield offsets[char], int(count)


class Day09(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        instructions = list(parsed)
        uniqe_pos = set(simulate(instructions))
        return len(uniqe_pos)

    def part2(self, parsed):
        instructions = list(parsed)
        uniqe_pos = set(simulate(instructions, 10))
        return len(uniqe_pos)


if __name__ == "__main__":
    main(Day09)
