use std::{
    collections::{HashMap, HashSet},
    ops::Deref,
};

use util::{Day, IVec2, aoc_main};

fn points_between(from: IVec2, to: IVec2) -> impl Iterator<Item = IVec2> {
    (from.x..=to.x).flat_map(move |x| (from.y..=to.y).map(move |y| IVec2::new(x, y)))
}

#[derive(Clone, Copy, Debug)]
enum Instruction {
    TurnOn { from: IVec2, to: IVec2 },
    TurnOff { from: IVec2, to: IVec2 },
    Toggle { from: IVec2, to: IVec2 },
}

impl Instruction {
    fn lights(self) -> impl Iterator<Item = IVec2> {
        match self {
            Self::Toggle { from, to } | Self::TurnOn { from, to } | Self::TurnOff { from, to } => {
                points_between(from, to)
            }
        }
    }
}

impl From<&str> for Instruction {
    fn from(value: &str) -> Self {
        let (name, from, to) = value
            .trim()
            .split_once("through")
            .map(|(rest, to)| {
                let (name, from) = rest.trim().rsplit_once(' ').unwrap();
                (
                    name,
                    from.trim()
                        .split_once(',')
                        .map(|(x, y)| IVec2::new(x.parse().unwrap(), y.parse().unwrap()))
                        .unwrap(),
                    to.trim()
                        .split_once(',')
                        .map(|(x, y)| IVec2::new(x.parse().unwrap(), y.parse().unwrap()))
                        .unwrap(),
                )
            })
            .unwrap();

        match name.trim() {
            "toggle" => Self::Toggle { from, to },
            "turn on" => Self::TurnOn { from, to },
            "turn off" => Self::TurnOff { from, to },
            other => unreachable!("unknown instruction: '{other}'"),
        }
    }
}

#[derive(Debug)]
struct Instructions(Box<[Instruction]>);

impl From<&str> for Instructions {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Instructions {
    type Target = Box<[Instruction]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day06;

impl Day for Day06 {
    type Parsed = Instructions;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let mut lights = HashSet::new();

        for &instruction in input.iter() {
            match instruction {
                Instruction::Toggle { from, to } => {
                    for light in points_between(from, to) {
                        if !lights.remove(&light) {
                            lights.insert(light);
                        }
                    }
                }
                Instruction::TurnOn { from, to } => lights.extend(points_between(from, to)),
                Instruction::TurnOff { from, to } => {
                    for light in points_between(from, to) {
                        lights.remove(&light);
                    }
                }
            }
        }

        lights.len()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut lights = HashMap::new();

        for &instruction in input.iter() {
            let f = match instruction {
                Instruction::Toggle { .. } => |x: usize| x.checked_add(2),
                Instruction::TurnOn { .. } => |x: usize| x.checked_add(1),
                Instruction::TurnOff { .. } => |x: usize| x.checked_sub(1),
            };

            for light in instruction.lights() {
                lights
                    .entry(light)
                    .and_modify(|v| *v = f(*v).unwrap_or(0))
                    .or_insert_with(|| f(0).unwrap_or(0));
            }
        }

        lights.values().sum()
    }
}

aoc_main!(Day06);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [
            ("turn on 0,0 through 999,999", 1_000_000),
            ("toggle 0,0 through 999,0", 1000),
        ] {
            assert_eq!(Day06::part1(&input.into()), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [
            ("turn on 0,0 through 0,0", 1),
            ("toggle 0,0 through 999,999", 2000000),
        ] {
            assert_eq!(Day06::part2(&input.into()), expected, "{input}");
        }
    }
}
