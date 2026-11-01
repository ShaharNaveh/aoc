from utils import Day, aoc_main


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    buf = []
    for line in inp.splitlines():
        if line == "":
            yield buf
            buf.clear()
        else:
            buf.append(int(line))
    yield buf


class Day01(Day):
    def parse(self, input: str):
        return tuple(iter_puzzle(input))

    def part1(self, parsed):
        return max(map(sum, parsed))

    def part2(self, parsed):
        return sum(sorted(map(sum, parsed), reverse=True)[:3])


if __name__ == "__main__":
    aoc_main(Day01)
