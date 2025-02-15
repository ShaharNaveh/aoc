import itertools
import pathlib


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


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_nums, *raw_boards = inp.split("\n" * 2)

    nums = tuple(map(int, raw_nums.split(",")))
    boards = frozenset(map(parse_board, raw_boards))
    return nums, boards


def p1(puzzle_file):
    return next(simulate(*parse_puzzle(puzzle_file)))


def p2(puzzle_file):
    for res in simulate(*parse_puzzle(puzzle_file)):
        pass
    return res


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
