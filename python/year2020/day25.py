import unittest

from utils import Day, aoc_main


def iter_loop_sizes():
    val = 1
    while True:
        val = (val * 7) % 20201227
        yield val


class Day25(Day):
    def parse(self, input: str):
        inp = input.strip()
        return tuple(map(int, inp.splitlines()))

    def part1(self, pub_keys):
        loop_size, device_pubkey = next(
            (loop_size, pub_key)
            for loop_size, pub_key in enumerate(iter_loop_sizes(), 1)
            if pub_key in pub_keys
        )

        subject = next(pub_key for pub_key in pub_keys if pub_key != device_pubkey)

        key = 1
        for _ in range(loop_size):
            key = (key * subject) % 20201227

        return key


TEST_PUZZLE = """\
5764801
17807724"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day25()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 14897079)


if __name__ == "__main__":
    aoc_main(Day25)
