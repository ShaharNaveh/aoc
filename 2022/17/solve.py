import itertools
import pathlib

ROCKS = [
    {0, 1, 2, 3},
    {1, 1j, 1+1j, 2+1j, 1+2j},
    {0, 1, 2, 2+1j, 2+2j},
    {0, 1j, 2j, 3j},
    {0, 1, 1j, 1+1j},
]

def simulate(jets, rock_count: int = 2022):
    tower = {complex(x, 0) for x in range(7)}
    for i, fallen_rock in enumerate(itertools.cycle(ROCKS), 1):
        if i > rock_count:
            return tower

        max_y = int(max(pos.imag for pos in tower))
        rock = {complex(pos.real + 2, pos.imag + max_y + 3 + 1) for pos in fallen_rock}
        for jet in jets:
            nrock = {pos + jet for pos in rock}
            if not (
                any((0 > pos.real) or (pos.real >= 7) for pos in nrock)
                or bool(nrock & tower)
            ):
                rock = nrock
            nrock = {pos -1j for pos in rock}
            if (nrock & tower):
                tower |= rock
                break
            rock = nrock

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    dct = {"<": -1, ">": 1}
    return itertools.cycle(list(map(dct.get, inp)))

def p1(puzzle_file):
    jets = parse_puzzle(puzzle_file)
    tower = simulate(jets)
    return int(max(pos.imag for pos in tower))

def p2(puzzle_file):
    return

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
