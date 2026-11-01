from utils import Day, run


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


def iter_puzzle(puzzle):
    inp = puzzle.strip()
    yield from map(lambda s: map(str.split, s.split("|")), inp.splitlines())


class Day08(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return sum(
            len(output) in (2, 3, 4, 7) for _, outputs in parsed for output in outputs
        )

    def part2(self, parsed):
        return sum(decode(*pair) for pair in parsed)


if __name__ == "__main__":
    run(Day08)
