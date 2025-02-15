import pathlib


def gen_seqs(history: tuple[int]):
    lst = [history]
    seq = lst[-1]
    while not all(n == 0 for n in seq):
        lst += [tuple(n2 - n1 for n1, n2 in zip(seq, seq[1:]))]
        seq = lst[-1]
    return lst


def predict_future(seqs: list[tuple[int]]):
    lst = seqs.copy()
    prediction = 0
    while lst:
        prediction += lst.pop()[-1]

    return prediction


def predict_past(seqs: list[tuple[int]]):
    lst = seqs.copy()
    prediction = 0
    while lst:
        prediction = lst.pop()[0] - prediction

    return prediction


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    for line in inp.splitlines():
        yield tuple(map(int, line.split()))


def p1(puzzle_file):
    return sum(map(predict_future, map(gen_seqs, iter_puzzle(puzzle_file))))


def p2(puzzle_file):
    return sum(map(predict_past, map(gen_seqs, iter_puzzle(puzzle_file))))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = pathlib.Path(__file__).parent / "test_puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
