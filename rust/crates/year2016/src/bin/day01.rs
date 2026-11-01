use std::{collections::HashSet, ops::Deref};

use util::{Day, IVec2, aoc_main};

#[derive(Debug)]
struct Step {
    turn: IVec2,
    count: usize,
}

impl From<&str> for Step {
    fn from(value: &str) -> Self {
        let mut it = value.trim().chars();
        let turn = match it.next().unwrap() {
            'L' => IVec2::Y,
            'R' => IVec2::NEG_Y,
            other => panic!("Unknown direction: '{other}'"),
        };

        let count = it.collect::<String>().parse().expect("A valid int");
        Self { turn, count }
    }
}

impl From<&str> for Steps {
    fn from(value: &str) -> Self {
        Self(value.trim().split(", ").map(Into::into).collect())
    }
}

#[derive(Debug)]
struct Steps(Vec<Step>);

impl Deref for Steps {
    type Target = Vec<Step>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day01;

impl Day for Day01 {
    type Parsed = Steps;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> i32 {
        let steps = input;
        let mut dir = IVec2::Y;
        let mut pos = IVec2::ZERO;

        for step in steps.iter() {
            dir = dir.rotate(step.turn);
            pos += dir * IVec2::splat(step.count.try_into().unwrap());
        }

        pos.abs().element_sum()
    }

    fn part2(input: &Self::Parsed) -> i32 {
        let steps = input;
        let mut dir = IVec2::Y;
        let mut pos = IVec2::ZERO;

        let mut visited = HashSet::new();
        for step in steps.iter() {
            dir = dir.rotate(step.turn);
            let target = pos + (dir * IVec2::splat(step.count.try_into().unwrap()));

            let diff = (target - pos).signum();
            let dist = (target.x - pos.x).abs().max((target.y - pos.y).abs());

            for _ in 0..dist {
                pos += diff;

                if !visited.insert(pos) {
                    return pos.abs().element_sum();
                }
            }
        }

        panic!("could not find a position that got visited twice");
    }
}

aoc_main!(Day01);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [("R2, L3", 5), ("R2, R2, R2", 2), ("R5, L5, R5, R3", 12)] {
            let parsed = Day01::parse(input);
            assert_eq!(Day01::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        let parsed = Day01::parse("R8, R4, R4, R8");
        assert_eq!(Day01::part2(&parsed), 4);
    }
}
