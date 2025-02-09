import io
import math
import operator
import pathlib

FUNCS = {0: sum, 1: math.prod, 2: min, 3: max}
COMPS = {5: operator.gt, 6: operator.lt, 7: operator.eq}


class Packet:
    def __init__(self, raw: str) -> None:
        self._buf = io.StringIO(raw)
        self.children = []

        self._version = bin_to_int(self.read(3))
        self._typ = bin_to_int(self.read(3))

        self._val = 0

        if self.is_literal:
            bits = []
            while True:
                marker, *segments = self.read(5)
                bits += segments
                if marker == "0":
                    break
            self._val = bin_to_int("".join(bits))
        else:
            if self.read(1) == "0":
                read = 0
                needs = bin_to_int(self.read(15))

                while read < needs:
                    read += self.parse_subpacket()
            else:
                count = bin_to_int(self.read(11))
                for _ in range(count):
                    self.parse_subpacket()

            self._val = self.calc_val()

    def calc_val(self):
        if (op := FUNCS.get(self.typ)) is not None:
            return op(self.children_vals)
        return COMPS[self.typ](*self.children_vals)

    @property
    def children_vals(self):
        return map(operator.attrgetter("val"), self.children)

    @property
    def val(self):
        return self._val

    def __int__(self) -> int:
        return self.version + sum(map(int, self.children))

    def parse_subpacket(self) -> int:
        sub_packet = type(self)(self.peek())
        self.children.append(sub_packet)
        self.read(len(sub_packet))
        return len(sub_packet)

    def peek(self, size: int = -1) -> str:
        idx = len(self)
        res = self.read(size)
        self._buf.seek(idx)
        return res

    def read(self, size: int = -1) -> str:
        return self._buf.read(size)

    @property
    def version(self) -> int:
        return self._version

    @property
    def typ(self) -> int:
        return self._typ

    @property
    def is_literal(self) -> bool:
        return self.typ == 4

    def __len__(self) -> int:
        return self._buf.tell()


def bin_to_int(b: str) -> int:
    return int(b, 2)


def hex_to_bits(h: str) -> str:
    return "".join(format(int(c, 16), "0>4b") for c in h)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return hex_to_bits(inp)


def p1(puzzle_file):
    return int(Packet(parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    return Packet(parse_puzzle(puzzle_file)).val


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
