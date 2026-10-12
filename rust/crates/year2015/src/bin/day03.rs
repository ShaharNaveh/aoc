use std::{collections::HashSet, ops::Deref};

use util::{Day, IVec2, aoc_main};

#[derive(Debug)]
struct Offsets(Box<[IVec2]>);

impl From<&str> for Offsets {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .chars()
                .map(|c| match c {
                    '^' => IVec2::NEG_Y,
                    '>' => IVec2::X,
                    'v' => IVec2::Y,
                    '<' => IVec2::NEG_X,
                    other => unreachable!("unknown: '{other}'"),
                })
                .collect(),
        )
    }
}

impl Deref for Offsets {
    type Target = Box<[IVec2]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day03;

impl Day for Day03 {
    type Parsed = Offsets;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let mut pos = IVec2::ZERO;

        let mut visited = HashSet::from([pos]);

        for &offset in input.iter() {
            pos += offset;
            visited.insert(pos);
        }

        visited.len()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut santa = IVec2::ZERO;
        let mut robot = IVec2::ZERO;

        let mut visited = HashSet::from([santa]);

        let mut switch = true;

        for &offset in input.iter() {
            if switch {
                santa += offset;
                visited.insert(santa);
            } else {
                robot += offset;
                visited.insert(robot);
            }

            switch = !switch;
        }

        visited.len()
    }
}

aoc_main!(Day03);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [(">", 2), ("^>v<", 4), ("^v^v^v^v^v", 2)] {
            let parsed = Day03::parse(input);
            assert_eq!(Day03::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [("^v", 3), ("^>v<", 3), ("^v^v^v^v^v", 11)] {
            let parsed = Day03::parse(input);
            assert_eq!(Day03::part2(&parsed), expected, "{input}");
        }
    }
}
