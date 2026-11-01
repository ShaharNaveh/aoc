from utils import Day, aoc_main


def overlap(s1: set[int], s2: set[int], *, is_p2: bool = False):
    if is_p2:
        return bool(s1 & s2)

    return (s1 >= s2) or (s2 >= s1)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        buf = []
        for part in line.split(","):
            start, stop = map(int, part.split("-"))
            buf += [set(range(start, stop + 1))]
        yield tuple(buf)


class Day04(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return sum(overlap(*pair) for pair in parsed)

    def part2(self, parsed):
        return sum(overlap(*pair, is_p2=True) for pair in parsed)


if __name__ == "__main__":
    aoc_main(Day04)
