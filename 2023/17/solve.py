import heapq
import pathlib


def min_heat_loss(
    grid: dict[complex, int], min_streak: int = 1, max_streak: int = 3
) -> int:
    start = 0
    seen = set()

    end = next(reversed(grid.keys()))
    pq = [(0, 0, 0, 1), (0, 0, 0, 1j)]
    priority = 0
    while pq:
        val, _, pos, direction = heapq.heappop(pq)

        if pos == end:
            return val

        if (pos, direction) in seen:
            continue
        seen.add((pos, direction))

        for possible_direction in (1j / direction, -1j / direction):
            for streak in range(min_streak, max_streak + 1):
                npos = pos + (possible_direction * streak)
                if npos not in grid:
                    continue
                cost = sum(
                    grid[pos + (possible_direction * i)] for i in range(1, streak + 1)
                )
                heapq.heappush(
                    pq,
                    (val + cost, (priority := priority + 1), npos, possible_direction),
                )


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): heat_loss
        for y, line in enumerate(inp.splitlines())
        for x, heat_loss in enumerate(map(int, line))
    }


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return min_heat_loss(grid)


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    return min_heat_loss(grid, 4, 10)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
