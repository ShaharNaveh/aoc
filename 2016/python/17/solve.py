#!/usr/bin/env python
import dataclasses
import hashlib
import heapq
import pathlib

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


def parse_puzzle(puzzle_file):
    return puzzle_file.read_text().strip()


def p1(puzzle_file):
    base = parse_puzzle(puzzle_file)

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


def p2(puzzle_file):
    res = -1

    base = parse_puzzle(puzzle_file)

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


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
