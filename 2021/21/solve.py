import functools
import itertools
import pathlib
import typing


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


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return tuple(map(lambda l: State(int(l[-1])), inp.splitlines()))


def p1(puzzle_file):
    return play(*parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return max(play_p2(*parse_puzzle(puzzle_file)))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
