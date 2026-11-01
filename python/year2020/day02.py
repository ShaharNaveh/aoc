from utils import Day, main


def is_valid(line: str, *, is_p2: bool = False) -> bool:
    raw_range, letter, password = line.replace(":", "").split()
    l, m = map(int, raw_range.split("-"))

    if is_p2:
        a, b = password[l - 1], password[m - 1]
        return (a != b) and (letter in (a, b))

    return password.count(letter) in range(l, m + 1)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.splitlines()


class Day02(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(map(is_valid, parsed))

    def part2(self, parsed):
        return sum(map(lambda l: is_valid(l, is_p2=True), parsed))


if __name__ == "__main__":
    main(Day02)
