from utils import Day, main


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


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    for line in inp.splitlines():
        yield tuple(map(int, line.split()))


class Day09(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(map(predict_future, map(gen_seqs, parsed)))

    def part2(self, parsed):
        return sum(map(predict_past, map(gen_seqs, parsed)))


if __name__ == "__main__":
    main(Day09)
