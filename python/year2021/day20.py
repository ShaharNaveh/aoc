import functools
import unittest

from utils import Day, main


@functools.cache
def find_neighs(pos: complex) -> tuple[complex, ...]:
    return tuple(
        pos + offset for offset in (-1 - 1j, -1j, 1 - 1j, -1, 0, 1, -1 + 1j, 1j, 1 + 1j)
    )


def is_npos_light(
    neighs: tuple[complex, ...],
    image: dict[complex, bool],
    algo: frozenset[int],
    fallback: bool,
) -> bool:
    return (
        int("".join("1" if image.get(pos, fallback) else "0" for pos in neighs), 2)
        in algo
    )


def enhance(algo: frozenset[int], image: dict[complex, bool], times: int = 2) -> int:
    fallback = False
    swap = 0 in algo
    for _ in range(times):
        nimage = {}
        for pixel in image:
            for neigh in find_neighs(pixel):
                if neigh in nimage:
                    continue
                nimage[neigh] = is_npos_light(find_neighs(neigh), image, algo, fallback)
        image = nimage
        if swap:
            fallback = not fallback

    lights = {k for k, v in image.items() if v}
    return len(lights)


class Day20(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        raw_algo, raw_image = inp.split("\n" * 2)

        algo = frozenset(idx for idx, char in enumerate(raw_algo) if char == "#")
        image = {
            complex(x, y): char == "#"
            for y, row in enumerate(raw_image.splitlines())
            for x, char in enumerate(row)
        }
        return algo, image

    def part1(self, parsed):
        return enhance(*parsed)

    def part2(self, parsed):
        return enhance(*parsed, 50)


TEST_PUZZLE = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""


class Tests(unittest.TestCase):
    DAY = Day20()

    def test_part1_test_puzzle(self):
        self.assertEqual(self.DAY.part1(self.DAY.parse(TEST_PUZZLE)), 35)

    def test_part2_test_puzzle(self):
        self.assertEqual(self.DAY.part2(self.DAY.parse(TEST_PUZZLE)), 3351)


if __name__ == "__main__":
    main(Day20)
