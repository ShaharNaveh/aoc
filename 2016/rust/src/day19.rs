use std::ops::{Deref, DerefMut};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Elf {
    target: usize,
}

#[derive(Debug)]
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

#[derive(Debug)]
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

fn p1(input: &str) -> usize {
    Game::from(input).solve(0, |_| true)
}

fn p2(input: &str) -> usize {
    let mut game = Game::from(input);
    game.solve((game.alive >> 1) - 1, |g| g.alive & 1 == 0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("5"), 3)
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2("5"), 2)
    }
}
