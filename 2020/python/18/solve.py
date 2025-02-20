import ast
import pathlib


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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.splitlines()


def p1(puzzle_file):
    trans = str.maketrans({"*": "-"})
    transformers = (Sub2Mult,)
    return sum(solve(line, trans, transformers) for line in iter_puzzle(puzzle_file))


def p2(puzzle_file):
    trans = str.maketrans({"*": "-", "+": "*"})
    transformers = (Mult2Add, Sub2Mult)
    return sum(solve(line, trans, transformers) for line in iter_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
