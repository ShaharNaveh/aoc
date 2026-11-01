import collections
import re

from utils import Day, aoc_main


class Day04(Day):
    def parse(self, input: str):
        inp = input.strip()

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

    def part1(self, parsed):
        guards, times = parsed
        guard, _ = max(times.items(), key=lambda x: x[1])
        minute = max(
            range(60),
            key=lambda m: sum(start <= m < stop for start, stop in guards[guard]),
        )
        return guard * minute

    def part2(self, parsed):
        guards, _ = parsed
        guard, minute = max(
            ((guard, minute) for minute in range(60) for guard in guards),
            key=lambda tup: sum(
                start <= tup[1] < stop for start, stop in guards[tup[0]]
            ),
        )
        return guard * minute


if __name__ == "__main__":
    aoc_main(Day04)
