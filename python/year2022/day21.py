import operator
import unittest

from utils import Day, main


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


class Day21(Day):
    def parse(self, inp: str):
        inp = inp.strip()

        ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
        }
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

    def part1(self, monkeys):
        return int(resolve(monkeys))

    def part2(self, monkeys):
        _, l_name, r_name = monkeys["root"]

        cache = {}
        resolve(monkeys | {"humn": 1j}, cache=cache)

        l, r = cache[l_name], cache[r_name]
        return int(abs((l.real - r.real) // (l.imag - r.imag)))


TEST_PUZZLE = """\
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


class Tests(unittest.TestCase):
    DAY = Day21()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 152)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 301)


if __name__ == "__main__":
    main(Day21)
