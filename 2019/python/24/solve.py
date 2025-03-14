import itertools
import pathlib

type Bug = complex
type DepthBug = tuple[int, Bug]
type Bugs = frozenset[Bug]
type DepthBugs = frozenset[tuple[Bug, int]]

GRID_SIZE = 5
CENTER = complex(GRID_SIZE // 2, GRID_SIZE // 2)


def find_neighbors(pos: Bug) -> Bugs:
    return frozenset(pos + offset for offset in (1, -1, 1j, -1j))


def is_nstate_bug(is_bug: bool, neighbors: int) -> bool:
    if is_bug:
        return neighbors == 1
    return neighbors in (1, 2)


def is_in_bounds(bug: Bug, bounds: int = GRID_SIZE) -> bool:
    return all(bounds > attr >= 0 for attr in (bug.real, bug.imag))


def infest(bugs: Bugs) -> Bugs:
    return frozenset(
        pos
        for pos in itertools.chain.from_iterable(map(find_neighbors, bugs))
        if is_in_bounds(pos)
        and is_nstate_bug(is_bug=pos in bugs, neighbors=len(find_neighbors(pos) & bugs))
    )


def find_rneighbors(pos: Bug, depth: int) -> DepthBugs:
    nbugs = set()
    for npos in find_neighbors(pos):
        match pos.real, pos.imag, npos.real, npos.imag:
            case _, _, -1, _:
                ndepth = depth - 1
                neighs = {complex(1, 2)}
            case 1, _, 2, 2:
                ndepth = depth + 1
                neighs = {complex(0, i) for i in range(GRID_SIZE)}
            case 3, _, 2, 2:
                ndepth = depth + 1
                neighs = {complex(GRID_SIZE - 1, i) for i in range(GRID_SIZE)}
            case _, _, 5, _:
                ndepth = depth - 1
                neighs = {complex(GRID_SIZE - 2, GRID_SIZE // 2)}
            case _, _, _, -1:
                ndepth = depth - 1
                neighs = {complex(GRID_SIZE // 2, 1)}
            case _, 1, 2, 2:
                ndepth = depth + 1
                neighs = {complex(i, 0) for i in range(GRID_SIZE)}
            case _, 3, 2, 2:
                ndepth = depth + 1
                neighs = {complex(i, GRID_SIZE - 1) for i in range(GRID_SIZE)}
            case _, _, _, 5:
                ndepth = depth - 1
                neighs = {complex(GRID_SIZE // 2, GRID_SIZE - 2)}
            case _, _, _, _:
                ndepth = depth
                neighs = {npos}
        nbugs |= {(neigh, ndepth) for neigh in neighs}
    return nbugs


def rinfest(bugs: DepthBugs) -> DepthBugs:
    depths = {depth for _, depth in bugs}
    min_depth, max_depth = min(depths), max(depths)
    return frozenset(
        bug
        for depth in range(min_depth - 1, max_depth + 2)
        for pos in itertools.starmap(complex, itertools.product(range(5), repeat=2))
        if (pos != CENTER)
        and is_nstate_bug(
            is_bug=(bug := (pos, depth)) in bugs,
            neighbors=len(find_rneighbors(*bug) & bugs),
        )
    )


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return frozenset(
        complex(x, y)
        for y, row in enumerate(inp.splitlines())
        for x, tile in enumerate(row)
        if tile == "#"
    )


def p1(puzzle_file):
    bugs = parse_puzzle(puzzle_file)
    seen = {bugs}

    while True:
        bugs = infest(bugs)
        if bugs in seen:
            break
        seen.add(bugs)

    return int(sum(2 ** (bug.real + bug.imag * 5) for bug in bugs))


def p2(puzzle_file):
    bugs = frozenset((bug, 0) for bug in parse_puzzle(puzzle_file))
    for _ in range(200):
        bugs = rinfest(bugs)
    return len(bugs)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
