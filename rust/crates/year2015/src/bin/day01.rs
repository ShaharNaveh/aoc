use std::ops::Deref;

use util::{Day, aoc_main};

#[derive(Debug)]
struct Directions(Box<[i32]>);

impl From<&str> for Directions {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .chars()
                .map(|c| match c {
                    '(' => 1,
                    ')' => -1,
                    other => unreachable!("unknown char: '{other}'"),
                })
                .collect(),
        )
    }
}

impl Deref for Directions {
    type Target = Box<[i32]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day01;

impl Day for Day01 {
    type Parsed = Directions;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> i32 {
        input.iter().sum()
    }

    fn part2(input: &Self::Parsed) -> Option<usize> {
        let mut floor = 0i32;

        for (idx, offset) in input.iter().enumerate() {
            floor += offset;

            if floor.is_negative() {
                return Some(idx + 1);
            }
        }

        panic!("Never got negative floor");
    }
}

aoc_main!(Day01);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        for (input, expected) in [
            ("(())", 0),
            ("()()", 0),
            ("(((", 3),
            ("(()(()(", 3),
            ("))(((((", 3),
            ("())", -1),
            ("))(", -1),
            (")))", -3),
            (")())())", -3),
        ] {
            let parsed = Day01::parse(input);
            assert_eq!(Day01::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn p2e1() {
        for (input, expected) in [(")", 1), ("()())", 5)] {
            let parsed = Day01::parse(input);
            assert_eq!(Day01::part2(&parsed).unwrap(), expected, "{input}");
        }
    }
}
