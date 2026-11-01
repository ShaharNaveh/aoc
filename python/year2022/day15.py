import itertools
import re

from utils import Day, run


def manhattan(a: complex, b: complex) -> int:
    return int(abs(a.real - b.real) + abs(a.imag - b.imag))


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    pattern = re.compile(r"=(-?\d*)")
    for nums in map(pattern.findall, inp.splitlines()):
        sx, sy, bx, by = map(int, nums)
        sensor, beacon = complex(sx, sy), complex(bx, by)
        yield sensor, beacon


class Day15(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        Y = 2_000_000
        dists = {(sensor, manhattan(sensor, beacon)) for sensor, beacon in parsed}
        return int(
            max(sensor.real - abs(Y - sensor.imag) + dist for sensor, dist in dists)
            - min(sensor.real + abs(Y - sensor.imag) - dist for sensor, dist in dists)
        )

    def part2(self, parsed):
        LIMIT = 4_000_000
        dists = {(sensor, manhattan(sensor, beacon)) for sensor, beacon in parsed}

        for l, r in itertools.permutations(dists, 2):
            l_sensor, l_dist = l
            r_sensor, r_dist = r

            common = r_sensor.real + r_sensor.imag + r_dist
            x = int(common + l_sensor.real - l_sensor.imag - l_dist) // 2
            y = int(common - l_sensor.real + l_sensor.imag + l_dist) // 2 + 1
            if all(0 < n < LIMIT for n in (x, y)) and all(
                manhattan(complex(x, y), sensor) > dist for sensor, dist in dists
            ):
                return (x * LIMIT) + y


if __name__ == "__main__":
    run(Day15)
