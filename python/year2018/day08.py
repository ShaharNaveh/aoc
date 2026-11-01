import typing
import unittest

from utils import Day, main


class Node(typing.NamedTuple):
    childrens: tuple["Node", ...] = ()
    metadata: tuple[int, ...] = ()

    @property
    def value(self) -> int:
        child_count = len(self.childrens)
        if child_count == 0:
            return sum(self.metadata)
        return sum(
            self.childrens[idx].value
            for i in self.metadata
            if (idx := i - 1) < child_count
        )

    @property
    def metadata_sum(self) -> int:
        return sum(self.metadata) + sum(child.metadata_sum for child in self.childrens)

    @staticmethod
    def load(data: list[int]) -> tuple[typing.Self, list[int]]:
        child_quantity, metadata_quantity, *leftover = data
        childrens = []
        for _ in range(child_quantity):
            child, leftover = Node.load(leftover)
            childrens.append(child)
        return Node(
            childrens=tuple(childrens), metadata=leftover[:metadata_quantity]
        ), leftover[metadata_quantity:]


class Day08(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return list(map(int, inp.split()))

    def part1(self, parsed):
        tree, _ = Node.load(parsed)
        return tree.metadata_sum

    def part2(self, parsed):
        tree, _ = Node.load(parsed)
        return tree.value


TEST_PUZZLE = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


class Tests(unittest.TestCase):
    DAY = Day08()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 138)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 66)


if __name__ == "__main__":
    main(Day08)
