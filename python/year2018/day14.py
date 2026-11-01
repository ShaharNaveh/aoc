import collections
import itertools

from utils import Day, run


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


class Day14(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return int(inp)

    def part1(self, idx):
        return "".join(map(str, itertools.islice(simulate(), idx, idx + 10)))

    def part2(self, parsed):
        target = tuple(map(int, str(parsed)))
        return next(
            i
            for i, recipies in enumerate(sliding_window(simulate(), len(target)))
            if target == recipies
        )


if __name__ == "__main__":
    run(Day14)
