import collections

from utils import Day, run

INV = {"0": "1", "1": "0"}


def most_common(s) -> str | None:
    counter = collections.Counter(s)
    most_common = counter.most_common()
    if most_common[0][1] > most_common[1][1]:
        return most_common[0][0]


def solve(puzzle: list[str]) -> int:
    gamma = epsilon = ""
    for col in zip(*puzzle):
        common_bit = most_common(col)
        gamma += common_bit
        epsilon += INV[common_bit]
    return int(gamma, 2) * int(epsilon, 2)


def solve_p2(nums: tuple[str, ...], inv: bool = False, idx: int = 0):
    if len(nums) == 1:
        return int(nums[0], 2)

    common = most_common(num[idx] for num in nums)
    if common is None:
        char = "0" if inv else "1"
    elif inv:
        char = INV[common]
    else:
        char = common

    nnums = tuple(num for num in nums if num[idx] == char)
    return solve_p2(nnums, inv, idx + 1)


class Day03(Day):
    def parse(self, inp: str):
        inp = inp.strip()
        return inp.splitlines()

    def part1(self, parsed):
        return solve(parsed)

    def part2(self, parsed):
        nums = tuple(parsed)
        return solve_p2(nums) * solve_p2(nums, True)


if __name__ == "__main__":
    run(Day03)
