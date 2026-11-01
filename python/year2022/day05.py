import collections
import itertools

from utils import Day, run


def simulate(stacks, instructions, *, is_p2: bool = False):
    for count, src, dest in instructions:
        crates = [stacks[src].pop() for _ in range(count)]
        if is_p2:
            crates = reversed(crates)
        stacks[dest].extend(crates)
    return stacks


def top_crates(stacks):
    return "".join(stacks[idx][-1] for idx in sorted(stacks))


class Day05(Day):
    def parse(self, inp: str):
        inp = inp.rstrip()
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
            for _, count, _, src, _, dest in map(
                str.split, instructions_block.splitlines()
            )
        )
        return dict(stacks), instructions

    def part1(self, parsed):
        stacks, instructions = parsed
        stacks = simulate(stacks, instructions)
        return top_crates(stacks)

    def part2(self, parsed):
        stacks, instructions = parsed
        stacks = simulate(stacks, instructions, is_p2=True)
        return top_crates(stacks)


if __name__ == "__main__":
    run(Day05)
