import collections
import itertools
import pathlib


def simulate(stacks, instructions, *, is_p2: bool = False):
    for count, src, dest in instructions:
        crates = [stacks[src].pop() for _ in range(count)]
        if is_p2:
            crates = reversed(crates)
        stacks[dest].extend(crates)
    return stacks


def top_crates(stacks):
    return "".join(stacks[idx][-1] for idx in sorted(stacks))


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().rstrip()
    stacks_block, instructions_block = inp.split("\n" * 2)

    *raw_stacks, _ = stacks_block.splitlines()
    stacks = collections.defaultdict(collections.deque)
    for line in raw_stacks:
        for idx, crate_parts in enumerate(itertools.batched(line, 4), start=1):
            crate = "".join(crate_parts).strip().removeprefix("[").removesuffix("]")
            if not crate:
                continue
            stacks[idx].appendleft(crate)

    instructions = tuple(
        tuple(map(int, (count, src, dest)))
        for _, count, _, src, _, dest in map(str.split, instructions_block.splitlines())
    )
    return dict(stacks), instructions


def p1(puzzle_file):
    stacks, instructions = parse_puzzle(puzzle_file)
    stacks = simulate(stacks, instructions)
    return top_crates(stacks)


def p2(puzzle_file):
    stacks, instructions = parse_puzzle(puzzle_file)
    stacks = simulate(stacks, instructions, is_p2=True)
    return top_crates(stacks)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
