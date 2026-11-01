import functools
import itertools
import re
import unittest

from utils import Day, run


@functools.cache
def apply_mask(val: int, mask: str, *, target: str = "X") -> int:
    return "".join(v if m == target else m for v, m in zip(f"{val:036b}", mask))


def find_addresses(mask: str) -> frozenset[str]:
    if "X" not in mask:
        return frozenset({mask})

    return frozenset(
        nmask
        for bit in ("0", "1")
        for nmask in find_addresses(mask.replace("X", bit, 1))
    )


def simulate(instructions, *, is_p2: bool = False) -> int:
    mask, mem = None, {}
    for ins, *args in instructions:
        if ins == "mask":
            mask = args[0]
            continue

        addr, val = map(int, args)
        if is_p2:
            addrs = find_addresses(apply_mask(addr, mask, target="0"))
        else:
            addrs = frozenset({addr})

        for mem_addr in addrs:
            mem[mem_addr] = val if is_p2 else int(apply_mask(val, mask), 2)
    return sum(mem.values())


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    mask_pattern = re.compile(r"(mask) = (.*)")
    mem_pattern = re.compile(r"(mem)\[(\d+)\] = (\d+)")
    yield from itertools.chain.from_iterable(
        mask_pattern.findall(line)
        if line.startswith("mask")
        else mem_pattern.findall(line)
        for line in inp.splitlines()
    )


class Day14(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return simulate(parsed)

    def part2(self, parsed):
        return simulate(parsed, is_p2=True)


TEST_PUZZLE = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


class Tests(unittest.TestCase):
    def test_part2_test_puzzle(self):
        d = Day14()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 208)


if __name__ == "__main__":
    run(Day14)
