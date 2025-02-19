import collections
import itertools
import pathlib


def simulate(nums):
    turns = collections.defaultdict(lambda: collections.deque(maxlen=2))

    for start_turn, num in enumerate(nums, 1):
        last_spoken = num
        turns[num].append(start_turn)

    for turn in itertools.count(start_turn + 1):
        spoken_turns = turns[last_spoken]
        if len(spoken_turns) == 2:
            l, r = turns[last_spoken]
            spoken = r - l
        else:
            spoken = 0

        turns[spoken].append(turn)
        last_spoken = spoken

        yield turn, spoken


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(int, inp.split(","))


def p1(puzzle_file):
    return next(
        spoken for turn, spoken in simulate(iter_puzzle(puzzle_file)) if turn == 2020
    )


def p2(puzzle_file):
    return next(
        spoken
        for turn, spoken in simulate(iter_puzzle(puzzle_file))
        if turn == 30_000_000
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
