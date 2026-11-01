from utils import Day, main


def iter_pos(offsets: tuple[tuple[complex, int]]):
    pos = 0
    for offset, amount in offsets:
        for _ in range(amount):
            pos += offset
            yield pos


class Day03(Day):
    def parse(self, inp: str):
        inp = inp.strip()

        return tuple(
            tuple(
                ({"L": -1, "D": 1j, "R": 1, "U": -1j}[offset[0]], int(offset[1:]))
                for offset in offsets.split(",")
            )
            for offsets in inp.splitlines()
        )

    def part1(self, parsed):
        wires = parsed
        wire1, wire2 = (set(iter_pos(offsets)) for offsets in parsed)
        return int(min(abs(pos.real) + abs(pos.imag) for pos in (wire1 & wire2)))

    def part2(self, parsed):
        wires = parsed
        wire1, wire2 = (list(iter_pos(offsets)) for offsets in parsed)
        intersection = set(wire1) & set(wire2)
        return min(wire1.index(pos) + wire2.index(pos) for pos in intersection) + 2


if __name__ == "__main__":
    main(Day03)
