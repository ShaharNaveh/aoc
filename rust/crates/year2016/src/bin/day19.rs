use std::ops::{Deref, DerefMut};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
struct Elf {
    target: usize,
}

#[derive(Clone, Debug)]
struct Elves(Vec<Elf>);

impl From<usize> for Elves {
    fn from(n: usize) -> Self {
        Self(
            (1..=n)
                .into_iter()
                .map(|id| Elf { target: id % n })
                .collect(),
        )
    }
}

impl From<&str> for Elves {
    fn from(value: &str) -> Self {
        value.trim().parse::<usize>().unwrap().into()
    }
}

impl Deref for Elves {
    type Target = Vec<Elf>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Elves {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Debug)]
struct Game {
    /// Current elf that play.
    current: usize,
    /// All elves.
    elves: Elves,
    /// How many elves are still playing.
    alive: usize,
}

impl Game {
    fn new(elves: Elves) -> Self {
        Self {
            current: 0,
            alive: elves.len(),
            elves,
        }
    }

    fn solve<F>(&mut self, mut target_parent: usize, steal_cond: F) -> usize
    where
        F: Fn(&Self) -> bool,
    {
        loop {
            let target = self[target_parent].target;
            self[target_parent].target = self[target].target;

            self.alive -= 1;
            if self.alive == 1 {
                break;
            }

            self.current = self[self.current].target;
            if steal_cond(&self) {
                target_parent = self[target_parent].target;
            };
        }

        self.current + 1
    }
}

impl From<&str> for Game {
    fn from(value: &str) -> Self {
        Self::new(value.into())
    }
}

impl Deref for Game {
    type Target = Elves;

    fn deref(&self) -> &Self::Target {
        &self.elves
    }
}

impl DerefMut for Game {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.elves
    }
}

struct Day19;

impl Day for Day19 {
    type Parsed = Game;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().solve(0, |_| true)
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut game = input.clone();
        game.solve((game.alive >> 1) - 1, |g| g.alive & 1 == 0)
    }
}

aoc_main!(Day19);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(Day19::part1(&Day19::parse("5")), 3)
    }

    #[test]
    fn p2e1() {
        assert_eq!(Day19::part2(&Day19::parse("5")), 2)
    }
}
