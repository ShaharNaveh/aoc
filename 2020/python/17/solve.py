import collections
import itertools
import operator
import pathlib


def find_neighs(cube: tuple[int, ...]):
    return {
        tuple(itertools.starmap(operator.add, zip(cube, offset)))
        for offset in itertools.product(range(-1, 2), repeat=len(cube))
        if any(offset)
    }


def simulate(cubes: set[tuple[int, ...]]) -> int:
    for _ in range(6):
        neighs = collections.Counter(
            ncube for cube in cubes for ncube in find_neighs(cube)
        )
        cubes = {
            cube
            for cube, neigh_count in neighs.items()
            if (neigh_count == 3) or ((neigh_count == 2) and (cube in cubes))
        }
    return len(cubes)


def parse_puzzle(puzzle_file, dims: int = 3):
    inp = puzzle_file.read_text().strip()
    return {
        (x, y) + (0,) * (dims - 2)
        for y, row in enumerate(inp.splitlines())
        for x, char in enumerate(row)
        if char == "#"
    }


def p1(puzzle_file):
    return simulate(parse_puzzle(puzzle_file))


def p2(puzzle_file):
    return simulate(parse_puzzle(puzzle_file, 4))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
