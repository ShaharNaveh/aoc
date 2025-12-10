use std::{
    collections::HashSet,
    ops::{Deref, DerefMut},
};

use crate::utils::IVec2;

#[derive(Debug)]
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

fn p1(input: &str) -> usize {
    Rolls::from(input).removable().count()
}

fn p2(input: &str) -> usize {
    let mut rolls = Rolls::from(input);
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

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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
    fn p1e1() {
        assert_eq!(p1(INPUT), 13);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 43);
    }
}
