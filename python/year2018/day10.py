import itertools
import re
import typing

from utils import Day, main


class Point(typing.NamedTuple):
    pos: complex
    vel: complex

    def after(self, seconds: int) -> typing.Self:
        return self._replace(pos=self.pos + (self.vel * seconds))

    @classmethod
    def from_str(cls, raw: str):
        pos_x, pos_y, vel_x, vel_y = map(int, re.findall(r"(-?\d+)", raw))
        return cls(complex(pos_x, pos_y), complex(vel_x, vel_y))


def find_min_max(points: frozenset[Point]) -> tuple[int, int, int, int]:
    locs = {point.pos for point in points}
    xs = {pos.real for pos in locs}
    ys = {pos.imag for pos in locs}
    min_x, min_y = map(int, map(min, (xs, ys)))
    max_x, max_y = map(int, map(max, (xs, ys)))
    return min_x, max_x, min_y, max_y


def format_points(points: frozenset[Point]) -> str:
    locs = {point.pos for point in points}
    min_x, max_x, min_y, max_y = find_min_max(points)
    return "\n".join(
        "".join(" #"[complex(x, y) in locs] for x in range(min_x, max_x + 1))
        for y in range(min_y, max_y + 1)
    )


class Day10(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return frozenset(map(Point.from_str, inp.splitlines()))

    def part1(self, points):
        for seconds in itertools.count():
            npoints = {point.after(seconds) for point in points}
            min_x, max_x, min_y, max_y = find_min_max(npoints)
            if (abs(max_x) - abs(min_x) + abs(max_y) - abs(min_y)) <= 70:
                return format_points(npoints)

    def part2(self, points):
        for seconds in itertools.count():
            npoints = {point.after(seconds) for point in points}
            min_x, max_x, min_y, max_y = find_min_max(npoints)
            if (abs(max_x) - abs(min_x) + abs(max_y) - abs(min_y)) <= 70:
                return seconds


if __name__ == "__main__":
    main(Day10)
