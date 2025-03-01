import collections
import pathlib


def orbit_count(orbit: str, orbits: dict[str, str]) -> int:
    if (norbit := orbits.get(orbit)) is None:
        return 0
    return 1 + orbit_count(norbit, orbits)


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return {k: v for v, k in map(lambda x: x.split(")"), inp.splitlines())}


def p1(puzzle_file):
    orbits = parse_puzzle(puzzle_file)
    return sum(orbit_count(orbit, orbits) for orbit in orbits)


def p2(puzzle_file):
    orbits = collections.defaultdict(set)
    for a, b in parse_puzzle(puzzle_file).items():
        orbits[a].add(b)
        orbits[b].add(a)

    todo, seen, steps = {"YOU"}, set(), 0
    while "SAN" not in todo:
        steps += 1
        ntodo = set()
        for orbit in todo:
            if orbit in seen:
                continue
            ntodo |= orbits[orbit]
        seen |= todo
        todo = ntodo

    return steps - 2


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
