import functools
import itertools
import json
import math
import pathlib


def compare_pair(left, right) -> bool:
    if right is None:
        return False

    if left is None:
        return True

    if all(isinstance(packet, int) for packet in (left, right)):
        if left == right:
            return None
        return right > left

    if all(isinstance(packet, list) for packet in (left, right)):
        for pair in itertools.zip_longest(left, right):
            if (res := compare_pair(*pair)) is not None:
                return res
        return None

    if isinstance(left, list):
        return compare_pair(left, [right])

    return compare_pair([left], right)


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from (
        tuple(map(json.loads, pair.splitlines())) for pair in inp.split("\n" * 2)
    )


def p1(puzzle_file):
    return sum(
        idx
        for idx, pair in enumerate(iter_puzzle(puzzle_file), 1)
        if compare_pair(*pair)
    )


def p2(puzzle_file):
    divider_packets = [[[n]] for n in (2, 6)]
    packets = (
        list(itertools.chain.from_iterable(iter_puzzle(puzzle_file))) + divider_packets
    )

    return math.prod(
        idx
        for idx, packet in enumerate(
            sorted(
                packets,
                key=functools.cmp_to_key(
                    lambda left, right: -1 if compare_pair(left, right) else 1
                ),
            ),
            start=1,
        )
        if packet in divider_packets
    )


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
