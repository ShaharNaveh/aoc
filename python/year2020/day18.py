import ast
import unittest

from utils import Day, main


class Sub2Mult(ast.NodeTransformer):
    def visit_Sub(self, node):
        return ast.Mult()


class Mult2Add(ast.NodeTransformer):
    def visit_Mult(self, node):
        return ast.Add()


def solve(line: str, trans, transformers) -> int:
    line = line.translate(trans)
    tree = ast.parse(f"res = {line}")
    for transformer in transformers:
        transformer().visit(tree)

    code = compile(tree, filename="aoc", mode="exec")
    exec(code, globals())
    return res


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from inp.splitlines()


class Day18(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        trans = str.maketrans({"*": "-"})
        transformers = (Sub2Mult,)
        return sum(solve(line, trans, transformers) for line in parsed)

    def part2(self, parsed):
        trans = str.maketrans({"*": "-", "+": "*"})
        transformers = (Mult2Add, Sub2Mult)
        return sum(solve(line, trans, transformers) for line in parsed)


TEST_PUZZLE = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"


class Tests(unittest.TestCase):
    DAY = Day18()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 13632)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 23340)


if __name__ == "__main__":
    main(Day18)
