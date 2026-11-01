# Python solutions

Standard library only (no third-party packages), Python 3.12+.

```
python/
  utils/          # shared code: `Day` base class, `run` entry point, Vec2/Vec3
  yearYYYY/
    dayDD.py      # one module per day, tests included
```

Puzzle inputs live in `../inputs/yearYYYY/dayDD.txt`.

## Running

From this directory:

```sh
python3 -m year2022.day05                 # uses ../inputs/year2022/day05.txt
python3 -m year2022.day05 path/to/input   # any other file
```

## Testing

```sh
python3 -m unittest discover -t . -p '*.py'                  # everything
python3 -m unittest discover -s year2022 -t . -p '*.py'      # one year
python3 -m unittest year2022.day05                           # one day
python3 -m unittest year2022.day05.Tests.test_part1_test_puzzle  # one test
```

Some tests (e.g. MD5 brute force in 2016) take a while; run them selectively.

## Writing a day

```python
import unittest

from utils import Day, run


class Day01(Day):
    def parse(self, inp):
        return [{"(": 1, ")": -1}[c] for c in inp.strip()]

    def part1(self, data):
        return sum(data)

    # `part2` is optional; the base class raises NotImplementedError and `run` skips it.


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day01()
        self.assertEqual(d.part1(d.parse("(()(()(")), 3)


if __name__ == "__main__":
    run(Day01)
```

- `run` calls `parse` once per part, so a part may mutate the data it receives.
- Code shared by several days of a year goes in `yearYYYY/__init__.py` or a sibling
  module.
