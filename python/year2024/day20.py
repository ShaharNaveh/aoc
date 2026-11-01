import itertools

from utils import Day, aoc_main


def path_dist(grid, cheat_len):
    start = next(pos for pos, char in grid.items() if char == "S")
    end = next(pos for pos, char in grid.items() if char == "E")

    pos = start
    distances = {start: 0}
    while pos != end:
        for direction in (1, -1, 1j, -1j):
            npos = pos + direction
            if npos not in grid:
                continue
            if npos in distances:
                continue
            distances[npos] = distances[pos] + 1
            pos = npos
            break

    res = 0
    for (pos1, pos_d1), (pos2, pos_d2) in itertools.combinations(distances.items(), 2):
        diff = pos1 - pos2
        pos_distance = abs(diff.imag) + abs(diff.real)
        if pos_distance > cheat_len:
            continue
        if abs(pos_d2 - pos_d1) - pos_distance < 100:
            continue
        res += 1
    return res


class Day20(Day):
    def parse(self, input: str):
        inp = input.strip()
        return {
            x + (y * 1j): char
            for y, line in enumerate(inp.splitlines())
            for x, char in enumerate(line)
            if char != "#"
        }

    def part1(self, grid):
        return path_dist(grid, 2)

    def part2(self, grid):
        return path_dist(grid, 20)


if __name__ == "__main__":
    aoc_main(Day20)
