"""Shared helpers for the Advent of Code solutions."""

import abc
import argparse
import pathlib
import sys

from .vec import Vec2, Vec3

__all__ = ["Day", "Vec2", "Vec3", "run"]

INPUTS_DIR = pathlib.Path(__file__).resolve().parents[2] / "inputs"


class Day(abc.ABC):
    """Base class for a day's solution.

    ``parse`` turns the raw puzzle text into whatever both parts work on. It is called
    once per part, so a part may freely mutate what it receives.
    """

    @abc.abstractmethod
    def parse(self, inp: str): ...

    @abc.abstractmethod
    def part1(self, data): ...

    def part2(self, data):
        raise NotImplementedError


def module_file(day: type[Day]) -> pathlib.Path:
    return pathlib.Path(sys.modules[day.__module__].__file__)


def default_input_path(day: type[Day]) -> pathlib.Path:
    """``python/year2015/day04.py`` -> ``inputs/year2015/day04.txt``."""
    path = module_file(day)
    return INPUTS_DIR / path.parent.name / f"{path.stem}.txt"


def run(day: type[Day], argv: list[str] | None = None) -> None:
    """Command line entry point, meant for ``python -m yearYYYY.dayDD``."""
    path = module_file(day)
    parser = argparse.ArgumentParser(prog=f"python -m {path.parent.name}.{path.stem}")
    parser.add_argument(
        "input",
        nargs="?",
        type=pathlib.Path,
        default=default_input_path(day),
        help="puzzle input file (default: %(default)s)",
    )
    args = parser.parse_args(argv)

    try:
        inp = args.input.read_text().rstrip()
    except OSError as e:
        parser.exit(1, f"failed to read {args.input}: {e}\n")

    solution = day()
    for part in (solution.part1, solution.part2):
        try:
            answer = part(solution.parse(inp))
        except NotImplementedError:
            continue

        if answer is not None:
            print(answer)
