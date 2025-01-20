import collections
import pathlib

def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

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

def p1(puzzle_file):
    sizes = parse_puzzle(puzzle_file)
    return sum(filter(lambda size: size <= 100_000, sizes.values()))

def p2(puzzle_file):
    sizes = parse_puzzle(puzzle_file)
    used = sizes["/"]
    needed = 30_000_000 - (70_000_000 - used)
    return next(filter(lambda size: size >= needed, sorted(sizes.values())))

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
