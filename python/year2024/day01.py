import unittest

from utils import Day, aoc_main


def calc_distance(lst1, lst2):
    for d1, d2 in zip(sorted(lst1), sorted(lst2)):
        yield abs(d1 - d2)


def calc_similarity(lst1, lst2):
    for num in lst1:
        count = lst2.count(num)
        yield num * count


class Day01(Day[tuple[list[int], list[int]]]):
    def parse(self, input: str) -> tuple[list[int], list[int]]:
        l_lst = []
        r_lst = []

        for line in input.splitlines():
            line = line.strip()
            l_item, r_item = line.split(" " * 3)
            l_lst.append(l_item)
            r_lst.append(r_item)

        return list(map(int, l_lst)), list(map(int, r_lst))

    def part1(self, parsed: tuple[list[int], list[int]]) -> int:
        return sum(calc_distance(*parsed))

    def part2(self, parsed: tuple[list[int], list[int]]) -> int:
        return sum(calc_similarity(*parsed))


EXAMPLE = """\
3   4
4   3
2   5
1   3
3   9
3   3"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day01()
        self.assertEqual(d.part1(d.parse(EXAMPLE)), 11)

    def test_part2(self):
        d = Day01()
        self.assertEqual(d.part2(d.parse(EXAMPLE)), 31)


if __name__ == "__main__":
    aoc_main(Day01)
