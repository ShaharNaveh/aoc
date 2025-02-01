import operator
import pathlib

def resolve(
    monkeys: dict[str, tuple[callable, str, str] | int],
    name: str = "root",
    *,
    cache: dict = {},
) -> int:
    out = monkeys[name]
    if isinstance(out, (int, float, complex)):
        cache[name] = out
        return out

    op, l, r = out
    res = op(resolve(monkeys, l, cache=cache), resolve(monkeys, r, cache=cache))
    cache[name] = res
    return res

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}
    monkeys = {} 
    for line in inp.splitlines():
        monkey, *dest = line.replace(":", "").split()
        if len(dest) == 1:
            out = int(dest[0])
        else:
            op = ops[dest[1]]
            out = (op, dest[0], dest[2])
        monkeys[monkey] = out
    return monkeys

def p1(puzzle_file):
    monkeys = parse_puzzle(puzzle_file)
    return int(resolve(monkeys))

def p2(puzzle_file):
    monkeys = parse_puzzle(puzzle_file)
    _, l_name, r_name =  monkeys["root"]

    cache = {}
    resolve(monkeys | {"humn": 1j}, cache=cache)

    l, r = cache[l_name], cache[r_name]
    return int(abs((l.real - r.real) // (l.imag - r.imag)))

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
