import functools
import itertools
import operator
import pathlib


def iter_puzzle(path):
    inp = path.read_text().strip()
    for line in inp.splitlines():
        val, nums = line.split(":")
        yield int(val), list(map(int, nums.strip().split()))


def is_possible(nums: list[int], val: int, allowed_ops: list[callable]) -> bool:
    for ops in itertools.product(allowed_ops, repeat=len(nums) - 1):
        actions = iter(ops)
        if val == functools.reduce(lambda x, y: next(actions)(x, y), nums):
            return True
    return False


def p1(path):
    allowed_ops = [operator.add, operator.mul]
    res = 0
    for val, nums in iter_puzzle(path):
        if not is_possible(nums=nums, val=val, allowed_ops=allowed_ops):
            continue
        res += val
    print(res)


def p2(path):
    allowed_ops = [operator.add, operator.mul, lambda a, b: int(str(a) + str(b))]
    res = 0
    for val, nums in iter_puzzle(path):
        if not is_possible(nums=nums, val=val, allowed_ops=allowed_ops):
            continue
        res += val
    print(res)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

p1(puzzle_file)
p2(puzzle_file)
