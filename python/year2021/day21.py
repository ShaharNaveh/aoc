import functools
import itertools
import typing
import unittest

from utils import Day, run


class State(typing.NamedTuple):
    pos: int
    score: int = 0


def play(p0: State, p1: State) -> int:
    states = {0: p0, 1: p1}
    dice = itertools.cycle(range(1, 101))
    rolled_count = 0

    player = False
    while True:
        steps = sum(itertools.islice(dice, 3))
        rolled_count += 3

        pos, score = states[player]
        npos = (pos + steps - 1) % 10 + 1
        nscore = score + npos

        nplayer = not player
        if nscore >= 1000:
            return states[nplayer].score * rolled_count

        states[player] = State(pos=npos, score=nscore)
        player = nplayer


@functools.cache
def play_p2(a: State, b: State) -> tuple[int, int]:
    aw = bw = 0
    for roll in itertools.product(range(1, 4), repeat=3):
        apos, ascore = a
        napos = (apos + sum(roll) - 1) % 10 + 1
        nascore = ascore + napos

        if nascore >= 21:
            aw += 1
            continue

        added_bw, added_aw = play_p2(b, State(napos, nascore))
        aw += added_aw
        bw += added_bw
    return aw, bw


class Day21(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return tuple(map(lambda l: State(int(l[-1])), inp.splitlines()))

    def part1(self, parsed):
        return play(*parsed)

    def part2(self, parsed):
        return max(play_p2(*parsed))


TEST_PUZZLE = """\
Player 1 starting position: 4
Player 2 starting position: 8"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day21()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 739785)

    def test_part2_test_puzzle(self):
        d = Day21()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 444356092776315)


if __name__ == "__main__":
    run(Day21)
