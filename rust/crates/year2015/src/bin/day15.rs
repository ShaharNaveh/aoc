use std::ops::{Add, Deref, Mul};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Default)]
struct IngredientSpec {
    capacity: isize,
    durability: isize,
    flavor: isize,
    texture: isize,
    calories: isize,
}

impl Add<Self> for IngredientSpec {
    type Output = Self;

    fn add(self, rhs: Self) -> Self::Output {
        Self {
            capacity: self.capacity + rhs.capacity,
            durability: self.durability + rhs.durability,
            flavor: self.flavor + rhs.flavor,
            texture: self.texture + rhs.texture,
            calories: self.calories + rhs.calories,
        }
    }
}

impl Mul<isize> for IngredientSpec {
    type Output = Self;

    fn mul(self, rhs: isize) -> Self::Output {
        Self {
            capacity: self.capacity * rhs,
            durability: self.durability * rhs,
            flavor: self.flavor * rhs,
            texture: self.texture * rhs,
            calories: self.calories * rhs,
        }
    }
}

impl From<&str> for IngredientSpec {
    fn from(value: &str) -> Self {
        let nums = value
            .split_ascii_whitespace()
            .filter_map(|s| s.trim_end_matches(',').parse().ok())
            .collect::<Vec<_>>();

        Self {
            capacity: nums[0],
            durability: nums[1],
            flavor: nums[2],
            texture: nums[3],
            calories: nums[4],
        }
    }
}

#[derive(Copy, Clone, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Score(usize);

impl Score {
    const ZERO: Self = Self(0);
}

impl From<Score> for usize {
    fn from(value: Score) -> Self {
        Self::from(value.0)
    }
}

impl From<IngredientSpec> for Score {
    fn from(value: IngredientSpec) -> Self {
        Self(
            [
                value.capacity,
                value.durability,
                value.flavor,
                value.texture,
            ]
            .into_iter()
            .map(|x| usize::try_from(x).unwrap_or_default())
            .product(),
        )
    }
}

#[derive(Debug)]
struct Ingredients(Vec<IngredientSpec>);

impl Ingredients {
    fn best(&self, calories_limit: Option<isize>) -> Score {
        self.best_inner(calories_limit, 0, 100, IngredientSpec::default())
    }

    fn best_inner(
        &self,
        calories_filter: Option<isize>,
        idx: usize,
        left: usize,
        score: IngredientSpec,
    ) -> Score {
        let spec = self[idx];
        if self.len() - 1 == idx {
            let nspec = score + (spec * isize::try_from(left).unwrap());
            return if calories_filter.is_none_or(|calories| calories == nspec.calories) {
                Score::from(nspec)
            } else {
                Score::ZERO
            };
        }

        (0..=left)
            .map(|n| {
                self.best_inner(
                    calories_filter,
                    idx + 1,
                    left - n,
                    score + (spec * isize::try_from(n).unwrap()),
                )
            })
            .max()
            .unwrap()
    }
}

impl From<&str> for Ingredients {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Ingredients {
    type Target = Vec<IngredientSpec>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day15;

impl Day for Day15 {
    type Parsed = Ingredients;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.best(None).into()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.best(Some(500)).into()
    }
}

aoc_main!(Day15);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
";

    #[test]
    fn part1() {
        assert_eq!(Day15::part1(&Day15::parse(INPUT)), 62842880);
    }

    #[test]
    fn part2() {
        assert_eq!(Day15::part2(&Day15::parse(INPUT)), 57600000);
    }
}
