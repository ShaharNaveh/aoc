import itertools
import pathlib


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()
    raw_ts, raw_buses = inp.splitlines()
    buses = tuple(
        (idx, int(bus)) for idx, bus in enumerate(raw_buses.split(",")) if bus != "x"
    )
    return int(raw_ts), buses


def p1(puzzle_file):
    start_ts, buses = parse_puzzle(puzzle_file)
    return next(
        (ts - start_ts) * target_bus
        for ts in itertools.count(start_ts)
        if any(ts % (target_bus := bus) == 0 for _, bus in buses)
    )


def p2(puzzle_file):
    ts, buses = parse_puzzle(puzzle_file)
    step = 1
    for idx, bus in buses:
        ts = next(c for c in itertools.count(ts, step) if (c + idx) % bus == 0)
        step *= bus
    return ts


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
