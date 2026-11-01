import functools
import hashlib
import itertools
import re
import unittest
from collections.abc import Iterable

from utils import Day, main

PATTERN = re.compile(r"(.)\1\1")


@functools.cache
def build_hash(salt: str, index: int, *, iterations: int = 1) -> str:
    res = f"{salt}{index}"

    for _ in range(iterations):
        res = hashlib.md5(res.encode()).hexdigest()

    return res


def iter_hashes(salt: str, it: Iterable[int], f=build_hash):
    yield from (f(salt, index) for index in it)


def get_triple(s: str) -> str | None:
    m = PATTERN.search(s)
    return m.group(1) if m else None


def iter_keys(salt: str, f=build_hash):
    for index in itertools.count():
        key = f(salt, index)
        c = get_triple(key)
        if c is None:
            continue

        target = c * 5
        nindex = index + 1
        range_ = range(nindex, nindex + 1000)
        if not any(target in nkey for nkey in iter_hashes(salt, range_, f)):
            continue

        yield index


class Day14(Day):
    def parse(self, inp: str) -> str:
        return inp.strip()

    def part1(self, parsed: str) -> int:
        return next(itertools.islice(iter_keys(parsed), 64 - 1, None))

    def part2(self, parsed: str) -> int:
        f = functools.partial(build_hash, iterations=2016 + 1)
        return next(itertools.islice(iter_keys(parsed, f), 64 - 1, None))


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day14()
        self.assertEqual(d.part1(d.parse("abc")), 22728)

    def test_part2(self):
        d = Day14()
        self.assertEqual(d.part2(d.parse("abc")), 22551)


if __name__ == "__main__":
    main(Day14)
