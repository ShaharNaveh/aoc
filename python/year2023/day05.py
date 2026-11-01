import unittest

from utils import Day, main


class Day05(Day):
    def parse(self, inp: str) -> str:
        return inp.strip()

    def part1(self, puzzle: str) -> int:
        seeds, *blocks = puzzle.split("\n" * 2)
        seeds = list(map(int, seeds.split(":")[1].split()))
        for block in blocks:
            ranges = []
            for line in block.splitlines()[1:]:
                info = list(map(int, line.split()))
                ranges.append(info)

            buf = []
            for seed in seeds:
                for dest, src, range_len in ranges:
                    if src <= seed < src + range_len:
                        val = seed - src + dest
                        buf.append(val)
                        break
                else:
                    buf.append(seed)
            seeds = buf
        return min(seeds)

    def part2(self, puzzle: str) -> int:
        inputs, *blocks = puzzle.split("\n" * 2)
        inputs = list(map(int, inputs.split(":")[1].split()))

        seeds = []
        for i in range(0, len(inputs), 2):
            seeds.append((inputs[i], inputs[i] + inputs[i + 1]))

        for block in blocks:
            ranges = []
            for line in block.splitlines()[1:]:
                info = list(map(int, line.split()))
                ranges.append(info)

            buf = []
            while seeds:
                start, end = seeds.pop()
                for dest, src, range_len in ranges:
                    overlap_start = max(start, src)
                    overlap_end = min(end, src + range_len)
                    if overlap_start < overlap_end:
                        buf.append(
                            (overlap_start - src + dest, overlap_end - src + dest)
                        )
                        if overlap_start > start:
                            seeds.append((start, overlap_start))
                        if overlap_end > end:
                            seeds.append((overlap_end, end))
                        break
                else:
                    buf.append((start, end))

            seeds = buf
        return min(seeds)[0]


TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day05()
        self.assertEqual(d.part1(d.parse(TEST_INPUT)), 35)

    def test_part2(self):
        d = Day05()
        self.assertEqual(d.part2(d.parse(TEST_INPUT)), 46)


if __name__ == "__main__":
    main(Day05)
