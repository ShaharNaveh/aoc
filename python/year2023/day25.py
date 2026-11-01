import copy
import itertools
import random
import re

from utils import Day, main


def split_graph(connections) -> tuple[set[str], set[str]]:
    onodes = list({node for node in itertools.chain.from_iterable(connections)})
    oedges = [(wires[0], wire) for wires in connections for wire in wires[1:]]

    while True:
        nodes = onodes.copy()
        edges = copy.deepcopy(oedges)

        random.shuffle(edges)

        connected_to = {node: node for node in nodes}
        node_count = {node: 1 for node in nodes}

        for _ in range(len(nodes) - 2):
            while True:
                edge = edges.pop()
                node = connected_to[edge[0]]
                ejected = connected_to[edge[1]]

                if node != ejected:
                    break

            nodes.remove(ejected)
            connected_to[ejected] = node

            connected_to = {n: connected_to[connected_to[n]] for n in connected_to}
            node_count[node] += node_count[ejected]

        cut = 0
        for edge in edges:
            left = connected_to[edge[0]]
            right = connected_to[edge[1]]
            if left != right:
                cut += 1

        if cut == 3:
            return node_count[nodes.pop()] * node_count[nodes.pop()]


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    pattern = re.compile(r"\w{3}")
    yield from map(pattern.findall, inp.splitlines())


class Day25(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        connections = tuple(parsed)
        return split_graph(connections)


if __name__ == "__main__":
    main(Day25)
