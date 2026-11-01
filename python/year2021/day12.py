import collections
import unittest

from utils import Day, main


def walk(caves, *, is_p2: bool = False) -> int:
    paths = set()
    todo = [("start", [])]
    while todo:
        cur, path = todo.pop()
        npath = path + [cur]

        if cur == "end":
            paths.add(tuple(npath))
            continue

        for con in caves[cur]:
            if con == "start":
                continue

            if con[0].islower() and (con in npath):
                small_caves = [cave for cave in npath if cave[0].islower()]
                if is_p2 and max(collections.Counter(small_caves).values()) >= 2:
                    continue
                elif not is_p2:
                    continue
            todo.append((con, npath.copy()))

    return len(paths)


class Day12(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        caves = collections.defaultdict(set)
        for line in inp.splitlines():
            l, r = line.split("-")
            caves[l].add(r)
            caves[r].add(l)
        return dict(caves)

    def part1(self, parsed):
        return walk(parsed)

    def part2(self, parsed):
        return walk(parsed, is_p2=True)


TEST_PUZZLE = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


class Tests(unittest.TestCase):
    DAY = Day12()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 226)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 3509)


if __name__ == "__main__":
    main(Day12)
