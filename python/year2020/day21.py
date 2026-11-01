import typing
import unittest

from utils import Day, main


class Food(typing.NamedTuple):
    ingredients: frozenset[str]
    allergens: frozenset[str]

    @classmethod
    def from_str(cls, raw: str) -> typing.Self:
        raw_ingredients, raw_allergens = raw.removesuffix(")").split(" (contains ")
        ingredients, allergens = raw_ingredients.split(), raw_allergens.split(", ")
        return cls(*map(frozenset, (ingredients, allergens)))


def solve(foods: frozenset[Food]) -> tuple[int, str]:
    all_ingredients, all_allergens = set(), set()
    for food in foods:
        all_ingredients |= food.ingredients
        all_allergens |= food.allergens

    allergens_index = {
        allergen: frozenset.intersection(
            *(ingredients for ingredients, allergens in foods if allergen in allergens)
        )
        for allergen in all_allergens
    }

    known_ingredients = {}
    while allergens_index:
        allergen = next(
            allergen
            for allergen, ingredients in allergens_index.items()
            if len(ingredients) == 1
        )

        ingredients = allergens_index.pop(allergen)
        ingredient = next(iter(ingredients))

        known_ingredients[ingredient] = allergen
        for k, v in allergens_index.items():
            allergens_index[k] = v - {ingredient}

    dangerous_ingredients = frozenset(known_ingredients)
    safe_ingredients = all_ingredients - dangerous_ingredients

    p1_answer = sum(len(safe_ingredients & ingredients) for ingredients, _ in foods)
    p2_answer = ",".join(
        ingredient
        for ingredient, _ in sorted(known_ingredients.items(), key=lambda x: x[1])
    )
    return p1_answer, p2_answer


def iter_puzzle(puzzle) -> typing.Iterator[Food]:
    inp = puzzle.strip()
    yield from map(Food.from_str, inp.splitlines())


class Day21(Day):
    def parse(self, inp: str):
        return tuple(iter_puzzle(inp))

    def part1(self, parsed):
        return solve(frozenset(parsed))[0]

    def part2(self, parsed):
        return solve(frozenset(parsed))[1]


TEST_PUZZLE = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


class Tests(unittest.TestCase):
    def test_part1_test_puzzle(self):
        d = Day21()
        self.assertEqual(d.part1(d.parse(TEST_PUZZLE)), 5)

    def test_part2_test_puzzle(self):
        d = Day21()
        self.assertEqual(d.part2(d.parse(TEST_PUZZLE)), "mxmxvkd,sqjhc,fvjkl")


if __name__ == "__main__":
    main(Day21)
