import itertools

from utils import Day, aoc_main


def parse_board(raw: str) -> frozenset[frozenset[int]]:
    board_grid = [list(map(int, row.split())) for row in raw.splitlines()]
    rows = frozenset(map(frozenset, board_grid))
    cols = frozenset(map(frozenset, zip(*board_grid)))
    return rows | cols


def simulate(nums, boards):
    drawn_nums = set()

    for num in nums:
        drawn_nums.add(num)
        nboards = set()
        for board in boards:
            if not any(row_col <= drawn_nums for row_col in board):
                nboards.add(board)
                continue
            unmarked_nums = set(itertools.chain.from_iterable(board)) - drawn_nums
            yield sum(unmarked_nums) * num
        boards = nboards


class Day04(Day):
    def parse(self, input: str):
        inp = input.strip()
        raw_nums, *raw_boards = inp.split("\n" * 2)

        nums = tuple(map(int, raw_nums.split(",")))
        boards = frozenset(map(parse_board, raw_boards))
        return nums, boards

    def part1(self, parsed):
        return next(simulate(*parsed))

    def part2(self, parsed):
        for res in simulate(*parsed):
            pass
        return res


if __name__ == "__main__":
    aoc_main(Day04)
