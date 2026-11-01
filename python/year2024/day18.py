import dataclasses
import heapq

from utils import Day, run


@dataclasses.dataclass(order=True, frozen=True, slots=True)
class Branch:
    distance: int = 0
    pos: complex = dataclasses.field(compare=False, default=0)


def dijkstra(graph, start=complex(0, 0), end=complex(70, 70)):
    dct = {pos: float("inf") for pos in graph}
    prev = {pos: None for pos in graph}

    dct[start] = 0
    pq = [Branch(distance=0, pos=start)]
    while pq:
        pqi = heapq.heappop(pq)
        dist, pos = pqi.distance, pqi.pos
        if pos == end:
            path = []
            while pos:
                path.append(pos)
                pos = prev[pos]
            return path[::-1]

        for val in graph[pos]:
            if dct[val] > (new_dist := dct[pos] + 1):
                dct[val] = new_dist
                prev[val] = pos
                heapq.heappush(pq, Branch(distance=new_dist, pos=val))


class Day18(Day):
    def parse(self, inp: str):
        graph = {complex(x, y): set() for x in range(71) for y in range(71)}
        for pos in graph:
            direction = -1
            for _ in range(4):
                npos = pos + direction
                if npos in graph:
                    graph[pos].add(npos)
                direction *= -1j

        inp = inp.strip()
        bits = [tuple(map(int, line.split(","))) for line in inp.splitlines()]
        return graph, bits

    def part1(self, parsed):
        graph, bits = parsed
        for bit in bits[:1024]:
            cbit = complex(*bit)
            for node in graph.pop(cbit, set()):
                graph[node].discard(cbit)
        res = dijkstra(graph)
        return len(res)

    def part2(self, parsed):
        graph, bits = parsed

        path = None
        for idx, bit in enumerate(bits):
            cbit = complex(*bit)
            for node in graph.pop(cbit, set()):
                graph[node].discard(cbit)

            if idx >= 1024 and (not path or cbit in path):
                path = dijkstra(graph)
                if path is None:
                    return ",".join(map(str, bit))


if __name__ == "__main__":
    run(Day18)
