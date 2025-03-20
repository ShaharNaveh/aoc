import collections
import datetime
import pathlib
import re


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    guards = collections.defaultdict(set)
    times = collections.defaultdict(int)
    for line in sorted(inp.splitlines()):
        raw_dt, action = line.removeprefix("[").split("] ")
        dt = datetime.datetime.strptime(raw_dt, "%Y-%m-%d %H:%M")
        if action.startswith("Guard"):
            guard = int(re.findall(r"Guard #(\d+)", line)[0])
        elif "falls" in action:
            start = dt
        elif "wakes" in action:
            stop = dt
            guards[guard].add((start.minute, stop.minute))
            times[guard] += (stop - start).seconds

    return guards, times


def p1(puzzle_file):
    guards, times = parse_puzzle(puzzle_file)
    guard, _ = max(times.items(), key=lambda x: x[1])
    minute = max(
        range(60), key=lambda m: sum(start <= m < stop for start, stop in guards[guard])
    )
    return guard * minute


def p2(puzzle_file):
    guards, times = parse_puzzle(puzzle_file)
    tguard, _ = max(times.items(), key=lambda x: x[1])
    guard, minute = max(
        ((guard, minute) for minute in range(60) for guard in guards),
        key=lambda t: sum(start <= t[1] < stop for start, stop in guards[t[0]]),
    )
    return guard * minute


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
