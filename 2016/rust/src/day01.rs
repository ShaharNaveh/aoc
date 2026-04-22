use crate::utils::IVec2;

use std::ops::Deref;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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

fn p1(input: &str) -> i32 {
    let steps = Steps::from(input);
    let mut dir = IVec2::Y;
    let mut pos = IVec2::ZERO;

    for step in steps.iter() {
        dir = dir.rotate(step.turn);
        pos += dir * IVec2::splat(step.count.try_into().unwrap());
    }

    pos.abs().element_sum()
}

fn p2(input: &str) -> usize {
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("R2, L3"), 5);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1("R2, R2, R2"), 2);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1("R5, L5, R5, R3"), 12);
    }
}
