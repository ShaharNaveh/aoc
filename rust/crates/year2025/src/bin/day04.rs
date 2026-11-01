use std::{
    collections::HashSet,
    ops::{Deref, DerefMut},
};

use util::{Day, Vec2, aoc_main};

type IVec2 = Vec2<isize>;

#[derive(Clone, Debug)]
struct Rolls(HashSet<IVec2>);

impl Deref for Rolls {
    type Target = HashSet<IVec2>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Rolls {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Rolls {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .enumerate()
                .map(|(y, line)| {
                    line.chars()
                        .enumerate()
                        .filter(|(_, c)| *c == '@')
                        .map(move |(x, _)| IVec2::new(x as isize, y as isize))
                })
                .flatten()
                .collect(),
        )
    }
}

impl Rolls {
    #[must_use]
    fn removable(&self) -> impl Iterator<Item = &IVec2> {
        self.iter().filter(|roll| {
            self.intersection(&roll.neighbors_8().into_iter().collect())
                .count()
                < 4
        })
    }
}

struct Day04;

impl Day for Day04 {
    type Parsed = Rolls;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.removable().count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut rolls = input.clone();
        let mut removed = 0;

        loop {
            let removable = &rolls.removable().copied().collect::<Vec<_>>();
            if removable.is_empty() {
                break;
            }

            for roll in removable {
                rolls.remove(roll);
                removed += 1;
            }
        }

        removed
    }
}

aoc_main!(Day04);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
";

    #[test]
    fn part1() {
        let parsed = Day04::parse(INPUT);
        assert_eq!(Day04::part1(&parsed), 13);
    }

    #[test]
    fn part2() {
        let parsed = Day04::parse(INPUT);
        assert_eq!(Day04::part2(&parsed), 43);
    }
}
