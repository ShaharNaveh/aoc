import json
import unittest

from utils import Day, main


def sum_of_numbers(data: list | dict | int, *, ignore: str | None = None) -> int:
    match data:
        case int(data):
            return data
        case str(data):
            return 0
        case list(data):
            return sum(sum_of_numbers(item, ignore=ignore) for item in data)
        case dict(data):
            items = data.values()
            if ignore in items:
                return 0

            return sum(sum_of_numbers(item, ignore=ignore) for item in items)
        case _:
            raise ValueError(f"Unknown value: '{data}'")


class Day12(Day):
    def parse(self, inp: str):
        return json.loads(inp.strip())

    def part1(self, parsed) -> int:
        return sum_of_numbers(parsed)

    def part2(self, parsed: str) -> int:
        return sum_of_numbers(parsed, ignore="red")


class Tests(unittest.TestCase):
    DAY = Day12()

    def test_part1(self):
        for inp, expected in [
            ("[1,2,3]", 6),
            ('{"a":2,"b":4}', 6),
            ("[[[3]]]", 3),
            ('{"a":{"b":4},"c":-1}', 3),
            ('{"a":[-1,1]}', 0),
            ('[-1,{"a":1}]', 0),
            ("[]", 0),
            ("{}", 0),
        ]:
            with self.subTest(inp=inp):
                self.assertEqual(self.DAY.part1(self.DAY.parse(inp)), expected)

    def test_part2(self):
        for inp, expected in [
            ("[1,2,3]", 6),
            ('[1,{"c":"red","b":2},3]', 4),
            ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
            ('[1,"red",5]', 6),
        ]:
            with self.subTest(inp=inp):
                self.assertEqual(self.DAY.part2(self.DAY.parse(inp)), expected)


if __name__ == "__main__":
    main(Day12)
