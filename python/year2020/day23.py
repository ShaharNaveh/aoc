import unittest

from utils import Day, main


def play(cups: list[int], steps: int = 100, pad: int | None = None):
    if pad is None:
        pad = len(cups)

    nex = list(range(1, pad + 2))
    for idx, label in enumerate(cups[:-1], 1):
        nex[label] = cups[idx]

    head = cups[0]
    if pad > len(cups):
        nex[-1] = head
        nex[cups[-1]] = max(cups) + 1
    else:
        nex[cups[-1]] = head

    for _ in range(steps):
        rem = nex[head]
        nex[head] = nex[nex[nex[rem]]]
        all_rem = rem, nex[rem], nex[nex[rem]]
        if head > 1:
            dest = head - 1
        else:
            dest = pad

        while dest in all_rem:
            if dest == 1:
                dest = pad
            else:
                dest -= 1

        nex[nex[nex[rem]]] = nex[dest]
        nex[dest] = rem
        head = nex[head]

    cup = nex[1]
    while cup != 1:
        yield cup
        cup = nex[cup]


class Day23(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return list(map(int, inp))

    def part1(self, parsed):
        return "".join(map(str, play(parsed)))

    def part2(self, parsed):
        it = play(parsed, 10_000_000, 1_000_000)
        return next(it) * next(it)


TEST_PUZZLE = """\
389125467"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day23()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), "67384529")

    def test_part2_test_puzzle(self):
        d = Day23()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 149245887792)


if __name__ == "__main__":
    main(Day23)
