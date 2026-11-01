use std::{
    collections::HashSet,
    ops::{Deref, DerefMut},
};

use util::{Day, IVec2, aoc_main};

#[derive(Clone, Debug)]
struct Traps {
    traps: HashSet<IVec2>,
    width: i32,
}

impl Traps {
    fn is_trap(&self, pos: IVec2) -> bool {
        let left = self.contains(&(pos + IVec2::NEG_X_NEG_Y));
        let right = self.contains(&(pos + IVec2::X_NEG_Y));

        left != right
    }

    fn solve(mut self, until_row: i32) -> usize {
        let width = self.width;
        let mut safe_count = (width as usize) - self.len();

        for y in 1..until_row {
            let ntraps = (0..width)
                .into_iter()
                .filter_map(|x| {
                    let pos = IVec2::new(x, y);
                    self.is_trap(pos).then_some(pos)
                })
                .collect::<HashSet<_>>();

            safe_count += (width as usize) - ntraps.len();

            self = Self {
                traps: ntraps,
                width,
            };
        }

        safe_count
    }
}

impl From<&str> for Traps {
    fn from(mut value: &str) -> Self {
        value = value.trim();
        Self {
            traps: value
                .char_indices()
                .filter_map(|(x, c)| (c == '^').then(|| IVec2::new(x.try_into().unwrap(), 0)))
                .collect(),
            width: value.len().try_into().unwrap(),
        }
    }
}

impl Deref for Traps {
    type Target = HashSet<IVec2>;

    fn deref(&self) -> &Self::Target {
        &self.traps
    }
}

impl DerefMut for Traps {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.traps
    }
}

struct Day18;

impl Day for Day18 {
    type Parsed = Traps;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().solve(40)
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.clone().solve(400_000)
    }
}

aoc_main!(Day18);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(Traps::from(".^^.^.^^^^").solve(10), 38);
    }
}
