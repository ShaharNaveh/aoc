import collections

from utils import Day, run


class Day07(Day):
    def parse(self, inp: str):
        inp = inp.strip()

        sizes = collections.defaultdict(int)
        stack = []
        for line in inp.splitlines():
            line = line.removeprefix("$ ")
            if line.startswith(("ls", "dir")):
                continue
            if line.startswith("cd"):
                dest = line.split()[-1]
                if dest == "..":
                    stack.pop()
                else:
                    path = "_".join((stack[-1], dest)) if stack else dest
                    stack.append(path)
            else:
                size, file = line.split()
                size = int(size)
                for path in stack:
                    sizes[path] += size

        return dict(sizes)

    def part1(self, sizes):
        return sum(filter(lambda size: size <= 100_000, sizes.values()))

    def part2(self, sizes):
        used = sizes["/"]
        needed = 30_000_000 - (70_000_000 - used)
        return next(filter(lambda size: size >= needed, sorted(sizes.values())))


if __name__ == "__main__":
    run(Day07)
