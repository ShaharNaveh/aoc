import dataclasses
import itertools
import operator
import pathlib

@dataclasses.dataclass(frozen=True, slots=True)
class Rock:
    idx: int 
    ints: tuple[int, ...]
    pos: int = 0b0010000

    def is_shiftable(self, op: callable) -> bool:
        edge = {operator.lshift: 0b1000000, operator.rshift: 0b0000001}[op]
        return not any(map(lambda x: operator.and_(x, edge), self)) 

    def __iter__(self):
        yield from self.ints

    def __and__(self, pile) -> bool:
        return any(i & layer for i, layer in zip(self, pile))

    def __lshift__(self, other):
        op = lambda x: operator.lshift(x, other)
        return dataclasses.replace(
            self, ints=tuple(map(op, self)), pos=op(self.pos)
        )

    def __rshift__(self, other):
        op = lambda x: operator.rshift(x, other)
        return dataclasses.replace(
            self, ints=tuple(map(op, self)), pos=op(self.pos)
        )

    def __len__(self) -> int:
        return len(self.ints)

@dataclasses.dataclass(frozen=True, slots=True)
class Jet:
    idx: int
    op: callable

ROCKS = tuple(itertools.starmap(
    Rock, enumerate(
        (
            (0b0011110,),
            (0b0001000, 0b0011100, 0b0001000),
            (0b0000100, 0b0000100, 0b0011100),
            (0b0010000, 0b0010000, 0b0010000, 0b0010000),
            (0b0011000, 0b0011000),
        )
    )
))

def simulate(jets, count: int = 2022) -> int:
    rocks, jets = map(itertools.cycle, (ROCKS, jets))
    pile = [0] * 10_000
    top = len(pile)
    states = {}

    for rock_idx, rock in enumerate(rocks):
        for jet, y in zip(jets, itertools.count(top - len(rock) - 3)):
            if rock.is_shiftable(jet.op):
                shifted = jet.op(rock, 1)
                if not (shifted & pile[y:]):
                    rock = shifted

            if (len(rock) + y >= len(pile)) or (rock & pile[y + 1:]):
                for idx, num in enumerate(rock):
                    pile[y + idx] |= num
                break

        top = min(top, y)
        height = len(pile) - top

        state = (jet.idx, rock.idx, rock.pos)
        if prev := states.get(state):
            prev_rock_idx, prev_height = prev

            rock_cycle = rock_idx - prev_rock_idx
            height_cycle = height - prev_height

            diff = count - rock_idx - 1
            more, remain = map(int, divmod(diff, rock_cycle))

            if remain == 0:
                return (height_cycle * more) + height
        else:
            states[state] = (rock_idx, height)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    dct = {"<": operator.lshift, ">": operator.rshift}
    return tuple(itertools.starmap(Jet, enumerate(map(dct.get, inp))))

def p1(puzzle_file):
    jets = parse_puzzle(puzzle_file)
    return simulate(jets)

def p2(puzzle_file):
    jets = parse_puzzle(puzzle_file)
    return simulate(jets, 1e12)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
