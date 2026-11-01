import collections
import itertools
import re
import unittest

from utils import Day, aoc_main


class Day07(Day):
    def parse(self, input: str):
        inp = input.strip()
        steps = collections.defaultdict(set)
        for dependency, step in re.findall(
            r"^Step (\w) must be finished before step (\w) can begin\.$",
            inp,
            re.MULTILINE,
        ):
            steps[step].add(dependency)
        return steps

    def part1(self, steps):
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

    def part2(self, steps):
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


TEST_PUZZLE = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day07()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), "CABDFE")


if __name__ == "__main__":
    aoc_main(Day07)
