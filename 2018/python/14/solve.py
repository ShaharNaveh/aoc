import collections
import itertools
import pathlib
import typing


def sliding_window(iterable, n: int):
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


def simulate():
    recipies = [3, 7]
    elves = [0, 1]
    yield from recipies
    while True:
        new_recipe = list(map(int, str(sum(recipies[idx] for idx in elves))))
        yield from new_recipe
        recipies.extend(new_recipe)
        elves = [(idx + recipies[idx] + 1) % len(recipies) for idx in elves]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return int(inp)


def p1(puzzle_file):
    idx = parse_puzzle(puzzle_file)
    return "".join(map(str, itertools.islice(simulate(), idx, idx + 10)))


def p2(puzzle_file):
    target = tuple(map(int, str(parse_puzzle(puzzle_file))))
    return next(
        i
        for i, recipies in enumerate(sliding_window(simulate(), len(target)))
        if target == recipies
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
