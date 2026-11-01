import collections
import itertools

from utils import Day, aoc_main


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def find_neighbors(pos: complex) -> frozenset[complex]:
    return frozenset(pos + offset for offset in (1, -1, 1j, -1j))


def find_min_max(coords: frozenset[complex]) -> tuple[int, int, int, int]:
    xs = {pos.real for pos in coords}
    ys = {pos.imag for pos in coords}
    min_x, min_y = map(int, map(min, (xs, ys)))
    max_x, max_y = map(int, map(max, (xs, ys)))
    return min_x, max_x, min_y, max_y


def find_dangerous(coords: frozenset[complex]) -> int:
    min_x, max_x, min_y, max_y = find_min_max(coords)
    sizes = collections.defaultdict(int)
    for pos in itertools.starmap(
        complex, itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1))
    ):
        dists = {opos: manhattan(opos, pos) for opos in coords}
        a, b = sorted(dists.items(), key=lambda t: t[1])[:2]
        if a[1] == b[1]:
            continue
        sizes[a[0]] += 1
    return max(sizes.values())


def find_safe(coords: frozenset[complex]) -> int:
    min_x, max_x, min_y, max_y = find_min_max(coords)
    safe = set()
    for pos in itertools.starmap(
        complex, itertools.product(range(min_x, max_x + 1), range(min_y, max_y + 1))
    ):
        dist = 0
        for coord in coords:
            dist += manhattan(pos, coord)
            if dist >= 10_000:
                break
        else:
            safe.add(pos)

    regions = []
    while safe:
        todo = {safe.pop()}
        region = set()
        while todo:
            pos = todo.pop()
            region.add(pos)
            for npos in find_neighbors(pos):
                if npos in region:
                    continue
                if npos not in safe:
                    continue
                todo.add(npos)
        safe -= region
        regions.append(region)

    return max(map(len, regions))


class Day06(Day):
    def parse(self, input: str):
        inp = input.strip()
        return frozenset(
            complex(*map(int, line.split(","))) for line in inp.splitlines()
        )

    def part1(self, parsed):
        return find_dangerous(parsed)

    def part2(self, parsed):
        return find_safe(parsed)


if __name__ == "__main__":
    aoc_main(Day06)
