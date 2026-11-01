import collections

from utils import Day, aoc_main


def get_marker(signal: str, window_size: int = 4) -> int:
    for i in range(len(signal) - window_size + 1):
        window = signal[i : i + window_size]
        if all(window.count(char) == 1 for char in window):
            return i + window_size


class Day06(Day):
    def parse(self, input: str):
        inp = input.strip()
        return inp

    def part1(self, signal):
        return get_marker(signal)

    def part2(self, signal):
        return get_marker(signal, 14)


if __name__ == "__main__":
    aoc_main(Day06)
