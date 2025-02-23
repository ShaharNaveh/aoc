import pathlib
import typing


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


def iter_puzzle(puzzle_file) -> typing.Iterator[Food]:
    inp = puzzle_file.read_text().strip()
    yield from map(Food.from_str, inp.splitlines())


def p1(puzzle_file):
    return solve(frozenset(iter_puzzle(puzzle_file)))[0]


def p2(puzzle_file):
    return solve(frozenset(iter_puzzle(puzzle_file)))[1]


puzzle_file = pathlib.Path(__file__).parent / "puzzle.txt"
# puzzle_file = puzzle_file.with_stem("test_puzzle")

print(p1(puzzle_file))
print(p2(puzzle_file))
