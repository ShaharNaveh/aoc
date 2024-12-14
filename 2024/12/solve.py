import collections
import itertools
import pathlib

DIRECTIONS = {0+1j, 1, 0-1j, -1}

def calc_cost(puzzle, *, is_p2: bool = False) -> int:
    seen = set()
    fences = collections.defaultdict(list)

    cost = 0
    for pos in puzzle:
        if pos is seen:
            continue

        size = 0
        region = [pos]
        while region:
            plant_pos = region.pop()
            if plant_pos in seen:
                continue

            seen.add(plant_pos)
            size += 1
            for direction in DIRECTIONS:
                npos = plant_pos + direction
                if puzzle[plant_pos] == puzzle.get(npos):
                    region.append(npos)
                    continue

                neigh = []
                for idx, fence in enumerate(fences[direction]):
                    for member in fence:
                        if any(
                            plant_pos == (member + direction * offset)
                            for offset in {1j, -1j}
                        ):
                            neigh.append(idx)
                match len(neigh):
                    case 0:
                        fences[direction].append([plant_pos])
                    case 1:
                        fences[direction][neigh[0]].append(plant_pos)
                    case 2:
                        fences[direction][
                            neigh[0]
                        ].extend(
                            fences[direction][neigh[1]] + [plant_pos]
                        )
                        del fences[direction][neigh[1]]
        if is_p2:
            cost += size * sum(len(edges) for edges in fences.values())
        else:
            cost += size * sum(
                len(list(itertools.chain.from_iterable(edges)))
                for edges in fences.values()
            )
        fences.clear()
    return cost


def load_puzzle(path):
    inp = path.read_text().strip()
    puzzle = {}
    for row_idx, row in enumerate(inp.splitlines()):
        for col_idx, plant in enumerate(row):
            puzzle[complex(col_idx, row_idx)] = plant
    return puzzle

def p1(path):
    puzzle = load_puzzle(path)
    res = calc_cost(puzzle)
    print(res)

def p2(path):
    puzzle = load_puzzle(path)
    res = calc_cost(puzzle, is_p2=True)
    print(res)



puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
