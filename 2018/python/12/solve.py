import collections
import itertools
import pathlib

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


def parse_puzzle(puzzle_file) -> tuple[Plants, Notes]:
    inp = puzzle_file.read_text().strip()
    raw_state, raw_notes = inp.split("\n" * 2)
    state = {idx for idx, char in enumerate(raw_state.split()[-1]) if char == "#"}
    notes = frozenset(
        (tuple(char == "#" for char in raw_note), dest == "#")
        for raw_note, dest in map(
            lambda x: tuple(x.split(" => ")), raw_notes.splitlines()
        )
    )

    return state, notes


def p1(puzzle_file):
    return sum(
        next(
            plants
            for generation, plants in enumerate(simulate(*parse_puzzle(puzzle_file)), 1)
            if generation == 20
        )
    )


def p2(puzzle_file):
    window_size = 100
    for generation, window in enumerate(
        sliding_window(map(sum, simulate(*parse_puzzle(puzzle_file))), window_size),
        window_size,
    ):
        l, r, *rest = window
        diff = r - l
        if all(b - a == diff for a, b in sliding_window(rest, 2)):
            break

    return window[-1] + (50_000_000_000 - generation) * diff


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
