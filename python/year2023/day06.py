import unittest

from utils import Day, main


def possible_race_ways(race: complex):
    race_time, distance_rec = int(race.real), int(race.imag)

    prev_distance = 0
    for hold in range(1, race_time):
        distance = hold * (race_time - hold)
        if distance_rec >= distance:
            if prev_distance > distance:
                break
            continue
        yield hold
        prev_distance = distance


class Day06(Day):
    def parse(self, inp: str) -> tuple[str, str]:
        time_line, distance_line = inp.strip().splitlines()
        return time_line, distance_line

    def part1(self, parsed: tuple[str, str]) -> int:
        time_line, distance_line = parsed
        times = map(int, time_line.split(":")[1].strip().split())
        distances = map(int, distance_line.split(":")[1].strip().split())
        races = {complex(time, distance) for time, distance in zip(times, distances)}

        res = 1
        for race in races:
            res *= sum(1 for _ in possible_race_ways(race))
        return res

    def part2(self, parsed: tuple[str, str]) -> int:
        time_line, distance_line = parsed
        time = int(time_line.split(":")[1].replace(" ", ""))
        distance = int(distance_line.split(":")[1].replace(" ", ""))
        race = complex(time, distance)
        return sum(1 for _ in possible_race_ways(race))


TEST_PUZZLE = """\
Time:      7  15   30
Distance:  9  40  200"""


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day06()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 288)

    def test_part2(self):
        d = Day06()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), 71503)


if __name__ == "__main__":
    main(Day06)
