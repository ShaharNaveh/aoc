import functools
import itertools
import pathlib
import string

def split_str(s: str) -> tuple[set[str], set[str]]:
    middle = len(s) // 2
    return set(s[:middle]), set(s[middle:])

def matching_items(rucksacks):
    yield from functools.reduce(set.intersection, rucksacks)

def iter_puzzle(puzzle_file, *, is_p2: bool = False):
    inp = puzzle_file.read_text().strip()
    yield from itertools.batched(inp.splitlines(), 3 if is_p2 else 1)

def p1(puzzle_file):
    return sum(
        string.ascii_letters.index(item) + 1
        for rucksacks in map(
            split_str,
            itertools.chain.from_iterable(iter_puzzle(puzzle_file))
        )
        for item in matching_items(rucksacks)
    )

def p2(puzzle_file):
    return sum(
        string.ascii_letters.index(item) + 1
        for rucksacks in iter_puzzle(puzzle_file, is_p2=True)
        for item in matching_items((set(rucksack) for rucksack in rucksacks))
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
