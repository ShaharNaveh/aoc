import itertools
import operator
import pathlib

ANS1 = 1374934
ANS2 = None

def fence_sides(_fences) -> int:


def garden_info(puzzle):
    garden = {plant: [] for plant in set(puzzle.values())}
    for loc, plant in puzzle.items():
        if loc in itertools.chain.from_iterable(
            map(operator.itemgetter("plots"), garden[plant])
        ):
            continue

        plots = {loc}
        fences_pos = set()
        while True:
            old_plots = plots.copy()

            for plot in old_plots:
                direction = -1
                for _ in range(4):
                    nplot = plot + direction
                    if puzzle.get(nplot) == plant:
                        plots.add(nplot)
                    else:
                        fences_pos.add((plot, nplot))
                    direction *= -1j

            if old_plots == plots:
                break

        garden[plant].append({"plots": plots, "fences": fences_pos})

    return garden

def p1(path):
    puzzle = load_puzzle(path)
    garden = garden_info(puzzle)
    res = 0
    for plant, regions in garden.items():
        for region in regions:
            plots = region["plots"]
            fences = region["fences"]
            res += len(plots) * len(fences)
    print(res)

def p2(path):
    puzzle = load_puzzle(path)
    garden = garden_info(puzzle)
    res = 0
    for plant, regions in garden.items():
        for region in regions:
            plots = region["plots"]
            fences = region["fences"]
            res += len(plots) * fence_sides(fences)
    print(res)

def load_puzzle(path):
    inp = path.read_text().strip()
    puzzle = {}
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, plant in enumerate(row):
            puzzle[complex(col_idx, row_idx)] = plant
    return puzzle


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "dummy.txt"

if not ANS1:
    p1(puzzle_file)

if not ANS2:
    p2(puzzle_file)
