import dataclasses
import hashlib
import heapq
import unittest

from utils import Day, run

OK = "bcdef"

START = 1 + 1j
END = 4 + 4j


@dataclasses.dataclass(frozen=True, slots=True)
class State:
    pos: complex = START
    path: tuple[str, ...] = ()

    @property
    def steps(self) -> int:
        return len(self.path)

    def next_moves(self, base: str):
        h = hashlib.md5(f"{base}{self}".encode()).hexdigest()
        for (name, offset), c in zip(
            (("U", -1j), ("D", 1j), ("L", -1), ("R", 1)), h[:4]
        ):
            if c in OK:
                yield name, offset

    def __str__(self) -> str:
        return "".join(self.path)

    def __lt__(self, other):
        return self.steps < other.steps


class Day17(Day):
    def parse(self, inp: str):
        return inp.strip()

    def part1(self, base):
        pq = [State()]
        while pq:
            state = heapq.heappop(pq)
            pos = state.pos

            if pos == END:
                return str(state)

            path = state.path
            for name, offset in state.next_moves(base):
                npos = pos + offset

                if not (
                    (START.real <= npos.real <= END.real)
                    and (START.imag <= npos.imag <= END.imag)
                ):
                    continue

                heapq.heappush(pq, State(npos, path + (name,)))

        raise ValueError(f"could not find for: {base}")

    def part2(self, parsed):
        res = -1

        base = parsed

        states = {State()}
        while states:
            state = states.pop()
            pos = state.pos

            if pos == END:
                res = max(res, state.steps)
                continue

            path = state.path
            for name, offset in state.next_moves(base):
                npos = pos + offset

                if not (
                    (START.real <= npos.real <= END.real)
                    and (START.imag <= npos.imag <= END.imag)
                ):
                    continue

                states.add(State(npos, path + (name,)))

        return res


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day17()
        for inp, expected in [
            ("ihgpwlah", "DDRRRD"),
            ("kglvqrro", "DDUDRLRRUDRD"),
            ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR"),
        ]:
            with self.subTest(inp=inp):
                self.assertEqual(d.part1(d.parse(inp)), expected)

    def test_part2(self):
        d = Day17()
        for inp, expected in [
            ("ihgpwlah", 370),
            ("kglvqrro", 492),
            ("ulqzkmiv", 830),
        ]:
            with self.subTest(inp=inp):
                self.assertEqual(d.part2(d.parse(inp)), expected)


if __name__ == "__main__":
    run(Day17)
