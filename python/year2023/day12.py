import functools

from utils import Day, main


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
            and (springs[nidx : nidx + 1] != "#")
        ):
            res += recurse(springs[nidx + 1 :], tuple(ngroups))
    return res


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        springs, groups = line.split()
        yield springs, tuple(map(int, groups.split(",")))


class Day12(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(recurse(*entry) for entry in parsed)

    def part2(self, parsed):
        return sum(
            recurse("?".join([springs] * 5), groups * 5) for springs, groups in parsed
        )


if __name__ == "__main__":
    main(Day12)
