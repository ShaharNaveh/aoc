import math

from utils import Day, main


def basin_from_low_point(low_pos: complex, grid: dict[complex, int]) -> int:
    basin = set()
    seen = set()
    todo = {low_pos}

    while todo:
        pos = todo.pop()

        basin.add(pos)
        seen.add(pos)

        for neigh in iter_neigh(pos):
            if neigh in seen:
                continue
            if grid.get(neigh, 9) == 9:
                seen.add(neigh)
                continue
            todo.add(neigh)

    return len(basin)


def iter_neigh(pos: complex):
    yield from (pos + offset for offset in (1, -1, 1j, -1j))


def iter_low_points(grid: dict[complex, int]):
    for pos, height in grid.items():
        if height == 9:
            continue
        if any(height >= grid.get(neigh, float("inf")) for neigh in iter_neigh(pos)):
            continue
        yield pos, height + 1


class Day09(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return {
            complex(x, y): int(val)
            for y, row in enumerate(inp.splitlines())
            for x, val in enumerate(row)
        }

    def part1(self, parsed):
        return sum(risk_level for _, risk_level in iter_low_points(parsed))

    def part2(self, grid):
        sizes = tuple(
            basin_from_low_point(pos, grid) for pos, _ in iter_low_points(grid)
        )
        return math.prod(sorted(sizes, reverse=True)[:3])


if __name__ == "__main__":
    main(Day09)
