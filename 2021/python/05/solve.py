import collections
import pathlib
import typing


class Line(typing.NamedTuple):
    start: complex
    end: complex

    def iter_pos(self) -> typing.Iterable[complex]:
        x1, x2 = self.x1, self.x2
        y1, y2 = self.y1, self.y2

        if self.is_horizontal:
            y = self.y1
            for x in range(min(x1, x2), max(x1, x2) + 1):
                yield complex(x, y)
        elif self.is_vertical:
            x = self.x1
            for y in range(min(y1, y2), max(y1, y2) + 1):
                yield complex(x, y)
        else:
            xstep = 1 if self.x2 > self.x1 else -1
            ystep = 1 if self.y2 > self.y1 else -1
            for n in range(abs(x2 - x1) + 1):
                yield complex(x1 + (xstep * n), y1 + (ystep * n))

    @property
    def is_straight(self) -> bool:
        return self.is_horizontal or self.is_vertical

    @property
    def is_vertical(self) -> bool:
        return self.x1 == self.x2

    @property
    def is_horizontal(self) -> bool:
        return self.y1 == self.y2

    def __getattr__(self, name: str):
        match name:
            case "x1":
                return int(self.start.real)
            case "y1":
                return int(self.start.imag)
            case "x2":
                return int(self.end.real)
            case "y2":
                return int(self.end.imag)
            case _:
                return getattr(self, attr)

    @classmethod
    def from_str(cls, raw: str):
        start, end = (complex(*map(int, seg.split(","))) for seg in raw.split("->"))
        return Line(start=start, end=end)


def overlap_count(counter: collections.Counter) -> int:
    return sum(count >= 2 for count in counter.values())


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(Line.from_str, inp.splitlines())


def p1(puzzle_file):
    counter = collections.Counter(
        pos
        for line in iter_puzzle(puzzle_file)
        for pos in line.iter_pos()
        if line.is_straight
    )
    return overlap_count(counter)


def p2(puzzle_file):
    counter = collections.Counter(
        pos for line in iter_puzzle(puzzle_file) for pos in line.iter_pos()
    )
    return overlap_count(counter)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
