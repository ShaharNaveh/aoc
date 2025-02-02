import collections
import dataclasses
import heapq
import pathlib

OFFSETS = {"<": -1, ">": 1, "^": -1j, "v": 1j}


@dataclasses.dataclass(frozen=True, slots=True)
class Branch:
    pos: complex = dataclasses.field(compare=False, default=0, hash=True)
    visited: frozenset[complex] = dataclasses.field(
        compare=False, default_factory=frozenset, hash=True
    )

    def __len__(self):
        return len(self.visited)

    def __lt__(self, other):
        return len(self) > len(other)


def iter_neigh(pos):
    yield from (pos + offset for offset in (1, -1, 1j, -1j))


def build_graph(grid, start, end):
    pq = [(start, start)]
    graph = collections.defaultdict(dict)
    while pq:
        start, pos = pq.pop()
        visited = {start}
        while True:
            if pos == end:
                graph[start][pos] = len(visited)
                break
            visited |= {pos}
            moves = [
                npos
                for npos in iter_neigh(pos)
                if ((npos in grid) and (npos not in visited))
            ]

            if not moves:
                break

            if len(moves) == 1:
                pos = moves[0]
                continue

            if pos not in graph[start]:
                graph[start][pos] = len(visited) - 1
                pq += [(pos, npos) for npos in moves]
            break

    return graph
    return {k: dict(v) for k, v in graph.items()}


def walk_graph(graph, start, end):
    pq = [(start, 0, set())]
    while pq:
        pos, dist, visited = pq.pop()

        if pos == end:
            yield dist
            continue

        visited |= frozenset({pos})

        for npos, ndist in graph[pos].items():
            if npos in visited:
                continue
            pq += [(npos, dist + ndist, visited.copy())]


def walk(grid, start, end):
    pq = [Branch(pos=start, visited=frozenset({start}))]
    while pq:
        branch = heapq.heappop(pq)
        pos, visited = dataclasses.astuple(branch)

        while True:
            if pos == end:
                yield visited
                break

            visited |= frozenset({pos})

            tile = grid[pos]
            if offset := OFFSETS.get(tile):
                npos = pos + offset
                if npos in visited:
                    moves = []
                else:
                    moves = [npos]
            else:
                moves = [
                    npos
                    for npos in iter_neigh(pos)
                    if ((npos in grid) and (npos not in visited))
                ]

            if len(moves) == 1:
                pos = moves[0]
            else:
                for npos in moves:
                    heapq.heappush(pq, Branch(npos, visited))
                break


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {
        complex(x, y): tile
        for y, line in enumerate(inp.splitlines())
        for x, tile in enumerate(line)
        if tile != "#"
    }


def p1(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    start, *_, end = [*grid]
    return max(map(len, walk(grid, start, end)))


def p2(puzzle_file):
    grid = parse_puzzle(puzzle_file)
    start, *_, end = [*grid]
    graph = build_graph(grid, start, end)

    return max(walk_graph(graph, start, end))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
