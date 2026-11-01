import functools
import itertools
import operator

from utils import Day, run


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        val, nums = line.split(":")
        yield int(val), list(map(int, nums.strip().split()))


def is_possible(nums: list[int], val: int, allowed_ops: list[callable]) -> bool:
    for ops in itertools.product(allowed_ops, repeat=len(nums) - 1):
        actions = iter(ops)
        if val == functools.reduce(lambda x, y: next(actions)(x, y), nums):
            return True
    return False


class Day07(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        allowed_ops = [operator.add, operator.mul]
        res = 0
        for val, nums in parsed:
            if not is_possible(nums=nums, val=val, allowed_ops=allowed_ops):
                continue
            res += val
        return res

    def part2(self, parsed):
        allowed_ops = [operator.add, operator.mul, lambda a, b: int(str(a) + str(b))]
        res = 0
        for val, nums in parsed:
            if not is_possible(nums=nums, val=val, allowed_ops=allowed_ops):
                continue
            res += val
        return res


if __name__ == "__main__":
    run(Day07)
