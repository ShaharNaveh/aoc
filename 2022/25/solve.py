import pathlib


def snafu_to_decimal(raw: str) -> int:
    vals = {"=": -2, "-": -1}
    return sum(
        int(vals.get(char, char)) * (5**i) for i, char in enumerate(reversed(raw))
    )


def decimal_to_snafu(num: int) -> str:
    res = ""
    while num > 0:
        rem = num % 5
        if rem >= 3:
            res += {3: "=", 4: "-"}[rem]
            num += 5 - rem
        else:
            res += str(rem)

        num //= 5
    return res[::-1]


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from inp.splitlines()


def p1(puzzle_file):
    return decimal_to_snafu(sum(map(snafu_to_decimal, iter_puzzle(puzzle_file))))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
