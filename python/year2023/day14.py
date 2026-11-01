from utils import Day, main


def tilt_cycle(grid: tuple[str, ...]) -> tuple[str, ...]:
    for _ in range(4):
        grid = tilt_north(grid)
        grid = tuple("".join(reversed(row)) for row in zip(*grid))
    return grid


def tilt_north(grid: tuple[str, ...]) -> tuple[str, ...]:
    t_grid = tuple(map("".join, zip(*grid)))

    ngrid = []
    for row in t_grid:
        buf = []
        for part in row.split("#"):
            shifted = sorted(part, reverse=True)
            jshifted = "".join(shifted)
            buf.append(jshifted)
        nrow = "#".join(buf)
        ngrid.append(nrow)
    return tuple(map("".join, zip(*ngrid)))


def calc_load(grid: tuple[str, ...]) -> int:
    return sum(row.count("O") * i for i, row in enumerate(reversed(grid), start=1))


class Day14(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return tuple(inp.splitlines())

    def part1(self, grid):
        return calc_load(tilt_north(grid))

    def part2(self, grid):
        NTH = 1_000_000_000

        seen = {grid}
        cycle = [grid]
        for idx in range(NTH):
            grid = tilt_cycle(grid)
            if grid in seen:
                break
            seen.add(grid)
            cycle.append(grid)

        first_idx = cycle.index(grid)
        grid_idx = ((NTH - first_idx) % (idx - first_idx + 1)) + first_idx
        return calc_load(cycle[grid_idx])


if __name__ == "__main__":
    main(Day14)
