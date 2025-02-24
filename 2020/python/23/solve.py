import pathlib


def play(cups: list[int], steps: int = 100, pad: int | None = None):
    if pad is None:
        pad = len(cups)

    nex = list(range(1, pad + 2))
    for idx, label in enumerate(cups[:-1], 1):
        nex[label] = cups[idx]

    head = cups[0]
    if pad > len(cups):
        nex[-1] = head
        nex[cups[-1]] = max(cups) + 1
    else:
        nex[cups[-1]] = head

    for _ in range(steps):
        rem = nex[head]
        nex[head] = nex[nex[nex[rem]]]
        all_rem = rem, nex[rem], nex[nex[rem]]
        if head > 1:
            dest = head - 1
        else:
            dest = pad

        while dest in all_rem:
            if dest == 1:
                dest = pad
            else:
                dest -= 1

        nex[nex[nex[rem]]] = nex[dest]
        nex[dest] = rem
        head = nex[head]

    cup = nex[1]
    while cup != 1:
        yield cup
        cup = nex[cup]


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    return list(map(int, inp))


def p1(puzzle_file):
    return "".join(map(str, play(parse_puzzle(puzzle_file))))


def p2(puzzle_file):
    it = play(parse_puzzle(puzzle_file), 10_000_000, 1_000_000)
    return next(it) * next(it)


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
