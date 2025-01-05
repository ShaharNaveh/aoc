import functools
import pathlib

@functools.cache
def recurse(springs: str, groups: tuple[int, ...]):
    if not groups:
        return "#" not in springs

    cgroup, *ngroups = groups
    res = 0
    for idx in range(len(springs) - sum(ngroups) - len(ngroups) - cgroup + 1):
        if "#" in springs[:idx]:
            break
        if (
            ((nidx := idx + cgroup) <= len(springs))
            and ("." not in springs[idx:nidx])
            and (springs[nidx:nidx + 1] != "#")
        ):
            res += recurse(springs[nidx + 1:], tuple(ngroups))
    return res


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for line in inp.splitlines():
        springs, groups = line.split()
        yield springs, tuple(map(int, groups.split(",")))

def p1(puzzle_file):
    return sum(recurse(*entry) for entry in iter_puzzle(puzzle_file))

def p2(puzzle_file):
    return sum(
        recurse("?".join([springs] * 5), groups * 5)
        for springs, groups in iter_puzzle(puzzle_file)
    )

puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
#puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
