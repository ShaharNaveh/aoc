import itertools
import unittest

from utils import Day, run


def defrag(lst):
    _lst = lst.copy()
    while "." in _lst:
        if (char := _lst.pop()) == ".":
            continue
        index = _lst.index(".")
        _lst[index] = char
    return _lst


def defrag_p2(lst):
    _lst = lst.copy()
    file_idx_stop = len(_lst) - 1
    while file_idx_stop >= 0:
        file_id = _lst[file_idx_stop]
        if file_id == ".":
            file_idx_stop -= 1
            continue
        file_slc = slice(file_idx_stop, file_idx_stop + 1)
        while True:
            new_file_slc = slice(file_slc.start - 1, file_slc.stop)
            if len(set(_lst[new_file_slc])) != 1:
                break
            file_slc = new_file_slc
        window_len = file_slc.stop - file_slc.start
        search_area = _lst[: file_slc.start]
        for offset in range(len(search_area) - window_len + 1):
            free_slc = slice(offset, offset + window_len)
            if search_area[free_slc].count(".") == window_len:
                break
        else:
            free_slc = None

        if free_slc:
            _lst[file_slc], _lst[free_slc] = _lst[free_slc], _lst[file_slc]

        file_idx_stop -= window_len
    return _lst


def parse_puzzle(puzzle):
    parsed = []
    for file_id, file_meta in enumerate(itertools.batched(puzzle, 2)):
        if len(file_meta) == 2:
            file_block, free_block = file_meta
        else:
            file_block, free_block = file_meta[0], 0

        parsed += [file_id] * file_block
        parsed += ["."] * free_block
    return parsed


class Day09(Day):
    def parse(self, inp: str) -> list[int]:
        inp = inp.strip()
        return list(map(int, list(inp)))

    def part1(self, puzzle: list[int]) -> int:
        parsed = parse_puzzle(puzzle)
        lst = defrag(parsed)
        return sum(pos * file_id for pos, file_id in enumerate(lst))

    def part2(self, puzzle: list[int]) -> int:
        parsed = parse_puzzle(puzzle)
        lst = defrag_p2(parsed)
        return sum(pos * file_id for pos, file_id in enumerate(lst) if file_id != ".")


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day09()
        self.assertEqual(d.part1(d.parse("2333133121414131402")), 1928)

    def test_part2(self):
        d = Day09()
        self.assertEqual(d.part2(d.parse("2333133121414131402")), 2858)


if __name__ == "__main__":
    run(Day09)
