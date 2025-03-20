import collections
import pathlib
import re


def parse_puzzle(puzzle_file):
    inp = puzzle_file.read_text().strip()

    guards = collections.defaultdict(set)
    times = collections.defaultdict(int)
    for line in sorted(inp.splitlines()):
        raw_minute, action = re.findall(r"\:(\d+)\] (.*)", line)[0]
        minute = int(raw_minute)
        if action.startswith("Guard"):
            guard = int(re.findall(r"Guard #(\d+)", line)[0])
        elif "falls" in action:
            start = minute
        elif "wakes" in action:
            stop = minute
            guards[guard].add((start, stop))
            times[guard] += stop - start

    return guards, times


def p1(puzzle_file):
    guards, times = parse_puzzle(puzzle_file)
    guard, _ = max(times.items(), key=lambda x: x[1])
    minute = max(
        range(60), key=lambda m: sum(start <= m < stop for start, stop in guards[guard])
    )
    return guard * minute


def p2(puzzle_file):
    guards, _ = parse_puzzle(puzzle_file)
    guard, minute = max(
        ((guard, minute) for minute in range(60) for guard in guards),
        key=lambda tup: sum(start <= tup[1] < stop for start, stop in guards[tup[0]]),
    )
    return guard * minute


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
