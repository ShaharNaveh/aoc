import collections
import itertools
import unittest

from utils import Day, main

type Plants = frozenset[int]
type Notes = frozenset[tuple[tuple[bool, ...], bool]]


def sliding_window(iterable, n: int = 100):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def simulate(plants: Plants, notes: Notes):
    while True:
        nplants = set()
        min_plant, max_plant = min(plants), max(plants)
        for plant in range(min_plant - 4, max_plant + 5):
            idx, is_nplant = next(
                (
                    (x, dest)
                    for x in range(plant - 2, plant + 3)
                    for note, dest in notes
                    if all(
                        (a in plants) == b for a, b in zip(range(x - 2, x + 3), note)
                    )
                ),
                (plant, plant in plants),
            )
            if is_nplant:
                nplants.add(idx)

        plants = frozenset(nplants)
        yield plants


class Day12(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        raw_state, raw_notes = inp.split("\n" * 2)
        state = {idx for idx, char in enumerate(raw_state.split()[-1]) if char == "#"}
        notes = frozenset(
            (tuple(char == "#" for char in raw_note), dest == "#")
            for raw_note, dest in map(
                lambda x: tuple(x.split(" => ")), raw_notes.splitlines()
            )
        )

        return state, notes

    def part1(self, parsed):
        return sum(
            next(
                plants
                for generation, plants in enumerate(simulate(*parsed), 1)
                if generation == 20
            )
        )

    def part2(self, parsed):
        window_size = 100
        for generation, window in enumerate(
            sliding_window(map(sum, simulate(*parsed)), window_size),
            window_size,
        ):
            l, r, *rest = window
            diff = r - l
            if all(b - a == diff for a, b in sliding_window(rest, 2)):
                break

        return window[-1] + (50_000_000_000 - generation) * diff


TEST_PUZZLE = """\
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day12()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 325)


if __name__ == "__main__":
    main(Day12)
