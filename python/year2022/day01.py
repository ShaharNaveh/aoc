from utils import Day, run


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
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return max(map(sum, parsed))

    def part2(self, parsed):
        return sum(sorted(map(sum, parsed), reverse=True)[:3])


if __name__ == "__main__":
    run(Day01)
