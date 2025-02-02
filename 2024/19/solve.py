import collections
import functools
import pathlib


class Node:
    __slots__ = ("neigh", "val")

    def __init__(self):
        self.neigh = collections.defaultdict(lambda: None)
        self.val = None


@functools.cache
def towels_req(tree, design):
    if design == "":
        return 1

    branch = tree
    count = 0
    for char in design:
        if (branch := branch.neigh[char]) is None:
            break
        if branch.val is not None:
            count += towels_req(tree, design[len(branch.val) :])
    return count


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    towels, patterns = inp.split("\n" * 2)

    tree = Node()
    for towel in towels.split(", "):
        branch = tree
        for char in towel:
            if not branch.neigh[char]:
                branch.neigh[char] = Node()
            branch = branch.neigh[char]
        branch.val = towel

    return tree, patterns.splitlines()


def p1(puzzle_file):
    tree, designs = parse_puzzle(puzzle_file)
    return sum(towels_req(tree, design) > 0 for design in designs)


def p2(puzzle_file):
    tree, designs = parse_puzzle(puzzle_file)
    return sum(towels_req(tree, design) for design in designs)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")
print(p1(puzzle_file))
print(p2(puzzle_file))
