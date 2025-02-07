import pathlib


def decode(signals: list[str], outputs: list[str]) -> int:
    layout = {
        k: next(signal for signal in signals if len(signal) == v)
        for k, v in {1: 2, 4: 4, 7: 3, 8: 7}.items()
    }
    signals = set(signals) - set(layout.values())

    layout[3] = next(
        signal
        for signal in signals
        if (len(signal) == 5) and (set(layout[1]) < set(signal))
    )
    signals = set(signals) - set(layout.values())

    layout[6] = next(
        signal
        for signal in signals
        if (len(signal) == 6) and (not (set(layout[1]) < set(signal)))
    )
    signals = set(signals) - set(layout.values())

    layout[9] = next(
        signal
        for signal in signals
        if (len(signal) == 6) and (set(layout[4]) < set(signal))
    )
    signals = set(signals) - set(layout.values())

    layout[0] = next(signal for signal in signals if len(signal) == 6)
    signals = set(signals) - set(layout.values())

    layout[2] = next(
        signal
        for signal in signals
        if (set(layout[8]) - set(layout[9])).pop() in signal
    )
    signals = set(signals) - set(layout.values())

    signals = set(signals) - set(layout.values())
    layout[5] = signals.pop()

    layout = {frozenset(v): str(k) for k, v in layout.items()}

    return int("".join(layout[frozenset(output)] for output in outputs))


def iter_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    yield from map(lambda s: map(str.split, s.split("|")), inp.splitlines())


def p1(puzzle_file):
    return sum(
        len(output) in (2, 3, 4, 7)
        for _, outputs in iter_puzzle(puzzle_file)
        for output in outputs
    )


def p2(puzzle_file):
    return sum(decode(*pair) for pair in iter_puzzle(puzzle_file))


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"

print(p1(puzzle_file))
print(p2(puzzle_file))
