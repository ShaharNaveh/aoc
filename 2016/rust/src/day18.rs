use std::{
    collections::HashSet,
    ops::{Deref, DerefMut},
};

use crate::utils::IVec2;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Debug)]
struct Traps {
    traps: HashSet<IVec2>,
    width: i32,
}

impl Traps {
    fn is_trap(&self, pos: IVec2) -> bool {
        let left = self.contains(&(pos + IVec2::NEG_X_NEG_Y));
        // let center = self.contains(&(pos + IVec2::NEG_Y));
        let right = self.contains(&(pos + IVec2::X_NEG_Y));

        /*
        if center {
            left != right
        } else {
        }

        false
        */

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

fn p1(input: &str) -> usize {
    Traps::from(input).solve(40)
}

fn p2(input: &str) -> usize {
    Traps::from(input).solve(400_000)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(Traps::from(".^^.^.^^^^").solve(10), 38);
    }
}
