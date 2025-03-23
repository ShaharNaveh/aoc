import collections
import itertools
import pathlib
import re


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    steps = collections.defaultdict(set)
    for dependency, step in re.findall(
        r"^Step (\w) must be finished before step (\w) can begin\.$", inp, re.MULTILINE
    ):
        steps[step].add(dependency)
    return steps


def p1(puzzle_file):
    steps = parse_puzzle(puzzle_file)
    all_steps = set(
        itertools.chain(steps, itertools.chain.from_iterable(steps.values()))
    )
    done = []
    for _ in all_steps:
        nstep = min(
            nstep
            for nstep in all_steps
            if (nstep not in done) and (steps[nstep] <= set(done))
        )
        done.append(nstep)
    return "".join(done)


def p2(puzzle_file):
    steps = parse_puzzle(puzzle_file)
    all_steps = set(
        itertools.chain(steps, itertools.chain.from_iterable(steps.values()))
    )
    done = set()
    res = 0
    counts = [0] * 5
    work = [""] * 5
    while True:
        for i, count in enumerate(counts):
            if count == 1:
                done.add(work[i])
            counts[i] = max(0, count - 1)
        while 0 in counts:
            i = counts.index(0)
            candidates = [step for step in all_steps if steps[step] <= done]
            if not candidates:
                break
            step = min(candidates)
            all_steps.remove(step)
            counts[i] = ord(step) - ord("A") + 61
            work[i] = step
        if sum(counts) == 0:
            break
        res += 1
    return res


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
