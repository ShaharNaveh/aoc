import functools
import itertools
import pathlib
import re


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


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    mask_pattern = re.compile(r"(mask) = (.*)")
    mem_pattern = re.compile(r"(mem)\[(\d+)\] = (\d+)")
    yield from itertools.chain.from_iterable(
        mask_pattern.findall(line)
        if line.startswith("mask")
        else mem_pattern.findall(line)
        for line in inp.splitlines()
    )


def p1(puzzle_file):
    return simulate(iter_puzzle(puzzle_file))


def p2(puzzle_file):
    return simulate(iter_puzzle(puzzle_file), is_p2=True)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
