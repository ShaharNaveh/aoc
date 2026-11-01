import collections
import functools

from utils import Day, run


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


class Day19(Day):
    def parse(self, inp: str):
        inp = inp.strip()
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

    def part1(self, parsed):
        tree, designs = parsed
        return sum(towels_req(tree, design) > 0 for design in designs)

    def part2(self, parsed):
        tree, designs = parsed
        return sum(towels_req(tree, design) for design in designs)


if __name__ == "__main__":
    run(Day19)
