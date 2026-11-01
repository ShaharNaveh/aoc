# Python solutions

Mirrors the `rust/` workspace layout. Stdlib only (no third-party packages), Python 3.12+.

```
python/
  utils/          # shared helpers: `Day` base class, runner, Vec2/Vec3
  yearYYYY/
    dayDD.py      # one module per day, with inline tests
```

Inputs are read from `../inputs/yearYYYY/dayDD.txt` (shared with Rust), unless a path is
passed as the first argument.

## Running

From this directory:

| Rust                                        | Python                                                   |
| ------------------------------------------- | -------------------------------------------------------- |
| `cargo run -p year2015 --bin day04 [path]`  | `python3 -m year2015.day04 [path]`                       |
| `cargo test -p year2015 --bin day04`        | `python3 -m unittest year2015.day04`                     |
| `cargo test -p year2015`                    | `python3 -m unittest discover -s year2015 -t . -p '*.py'` |
| `cargo test`                                | `python3 -m unittest discover -t . -p '*.py'`            |
| `cargo test -- --ignored`                   | `AOC_SLOW=1 python3 -m unittest discover -t . -p '*.py'` |

## Writing a day

```python
import unittest

from utils import Day, aoc_main


class Day01(Day[list[int]]):
    def parse(self, input: str) -> list[int]:
        return [{"(": 1, ")": -1}[c] for c in input.strip()]

    def part1(self, parsed: list[int]) -> int:
        return sum(parsed)

    # `part2` is optional; returning `None` means "not implemented yet".


class Tests(unittest.TestCase):
    def test_part1(self):
        d = Day01()
        self.assertEqual(d.part1(d.parse("(()(()(")), 3)


if __name__ == "__main__":
    aoc_main(Day01)
```

- The runner calls `parse` separately for each part, so parts may mutate what they
  receive.
- Mark slow tests with `@utils.slow` (the equivalent of `#[ignore]`).
- Helpers shared by several days of a year go in `yearYYYY/__init__.py` or a sibling module.
