import abc
import copy
import os
import pathlib
import sys
import unittest

from .vec2 import Vec2
from .vec3 import Vec3

__all__ = ["Answer", "Day", "Vec2", "Vec3", "aoc_main", "read_input", "run", "slow"]

INPUTS_DIR = pathlib.Path(__file__).resolve().parents[2] / "inputs"

# Like Rust's `#[ignore]`: only run when `AOC_SLOW` is set.
slow = unittest.skipUnless(os.environ.get("AOC_SLOW"), "slow (set AOC_SLOW=1 to run)")

# `None` means it's not implemented yet/NA.
type Answer = int | str | float | None


class Day[P](abc.ABC):
    """Result of `parse` (`P`) is shared by both parts."""

    @abc.abstractmethod
    def parse(self, input: str) -> P: ...

    @abc.abstractmethod
    def part1(self, parsed: P) -> Answer: ...

    def part2(self, parsed: P) -> Answer:
        return None


def read_input(default_path: pathlib.Path) -> str:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    try:
        return path.read_text()
    except OSError as e:
        sys.exit(f"failed to read {path}: {e}")


def run(day: type[Day], input: str) -> None:
    solver = day()
    parsed = solver.parse(input.rstrip())

    # Each part gets its own copy, so parts are free to mutate it.
    if (answer := solver.part1(copy.deepcopy(parsed))) is not None:
        print(answer)

    if (answer := solver.part2(copy.deepcopy(parsed))) is not None:
        print(answer)


def aoc_main(day: type[Day]) -> None:
    module_path = pathlib.Path(sys.modules[day.__module__].__file__)
    default_input = INPUTS_DIR / module_path.parent.name / f"{module_path.stem}.txt"

    run(day, read_input(default_input))
