import collections
import itertools
import pathlib


def build_graph(pcs):
    graph = collections.defaultdict(set)
    for a, b in pcs:
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(lambda line: line.split("-"), inp.splitlines())


def p1(puzzle_file):
    pcs = iter_puzzle(puzzle_file)
    graph = build_graph(pcs)
    groups = {
        frozenset({edge, a, b})
        for edge, pcs in graph.items()
        for a, b in itertools.combinations(pcs, 2)
        if a in graph[b]
    }

    return sum(any(pc.startswith("t") for pc in group) for group in groups)


def p2(puzzle_file):
    pcs = iter_puzzle(puzzle_file)
    graph = build_graph(pcs)
    largest = max(
        (
            set(comb) | {edge}
            for edge, pcs in graph.items()
            for idx in range(len(pcs), 1, -1)
            for comb in itertools.combinations(pcs, idx)
            if all(a in graph[b] for a, b in itertools.combinations(comb, 2))
        ),
        key=len,
    )
    return ",".join(sorted(largest))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
