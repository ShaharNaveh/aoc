import collections
import itertools

from utils import Day, run


def build_graph(pcs):
    graph = collections.defaultdict(set)
    for a, b in pcs:
        graph[a].add(b)
        graph[b].add(a)
    return dict(graph)


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(lambda line: line.split("-"), inp.splitlines())


class Day23(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, pcs):
        graph = build_graph(pcs)
        groups = {
            frozenset({edge, a, b})
            for edge, pcs in graph.items()
            for a, b in itertools.combinations(pcs, 2)
            if a in graph[b]
        }

        return sum(any(pc.startswith("t") for pc in group) for group in groups)

    def part2(self, pcs):
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


if __name__ == "__main__":
    run(Day23)
