import collections
import dataclasses
import heapq
import itertools
import pathlib

INF = float("inf")

@dataclasses.dataclass(order=True)
class Branch:
    cost: int = 0
    steps: int = 0
    cnode: tuple[complex, bool] = dataclasses.field(compare=False, default=None)
    visited: list[tuple[complex, bool]] = dataclasses.field(
        compare=False, default_factory=list
    )

def possible_branches(grid):
    start_pos = next(pos for pos, val in grid.items() if val == "S")
    end_pos = next(pos for pos, val in grid.items() if val == "E")

    start = (start_pos, True)
    end = [(end_pos, b) for b in (True, False)]

    graph = grid_to_graph(grid)
    branch_costs = collections.defaultdict(lambda: INF) | {start: 0}

    min_cost= INF
    cheapest_branches = []
    branches = [
        Branch(cost=0, steps=0, cnode=start, visited=[start]),
    ]
    while branches:
        branch = heapq.heappop(branches)

        cost = branch.cost
        if cost > min_cost:
            break

        cnode = branch.cnode
        visited = branch.visited
        if cnode in end:
            if min_cost > cost:
                min_cost = cost
                cheapest_branches = [visited]
            elif min_cost == cost:
                cheapest_branches.append(visited)
            continue

        for neigh, ecost in graph[cnode].items():
            ncost = cost + ecost
            if ncost > branch_costs[neigh]:
                continue
            branch_costs[neigh] = ncost
            heapq.heappush(
                branches,
                Branch(
                    cost=ncost, steps=branch.steps + 1, cnode=neigh, visited=visited + [neigh]
                ),
            )

    return min_cost, cheapest_branches

def parse_puzzle(path):
    inp = path.read_text().strip()
    grid = {
        x + (y * 1j): char
        for y, row in enumerate(inp.splitlines())
        for x, char in enumerate(row)
    }
    return grid

def grid_to_graph(grid):
    graph = collections.defaultdict(dict)
    for pos in (pos for pos, val in grid.items() if val != "#"):
        wt, wf = (pos, True), (pos, False)
        graph[wt][wf] = graph[wf][wt] = 1000

        direction = -1
        for _ in range(4):
            npos = pos + direction
            if grid[npos] == "#":
                direction *= -1j
                continue

            is_x = bool(direction.real)
            graph[(pos, is_x)][(npos, is_x)] = 1
            direction *= -1j

    return dict(graph)

def p1(path):
    grid = parse_puzzle(path)
    res, _ = possible_branches(grid)
    return res

def p2(path):
    grid = parse_puzzle(path)
    _, branches = possible_branches(grid)
    res = len({visited[0] for visited in itertools.chain.from_iterable(branches)})
    return res

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"
#puzzle_file = pathlib.Path(__file__).parent / "test_puzzle2.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
