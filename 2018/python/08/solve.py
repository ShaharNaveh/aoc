import pathlib
import typing


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


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return list(map(int, inp.split()))


def p1(puzzle_file):
    tree, _ = Node.load(parse_puzzle(puzzle_file))
    return tree.metadata_sum


def p2(puzzle_file):
    tree, _ = Node.load(parse_puzzle(puzzle_file))
    return tree.value


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
