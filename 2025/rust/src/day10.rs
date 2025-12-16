use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashSet},
    ops::Deref,
};

#[derive(Debug)]
struct Lights(Box<[bool]>);

impl Deref for Lights {
    type Target = [bool];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Lights {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .trim_start_matches('[')
                .trim_end_matches(']')
                .chars()
                .map(|c| c == '#')
                .collect(),
        )
    }
}

#[derive(Debug)]
struct Button(Box<[usize]>);

impl Deref for Button {
    type Target = [usize];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Button {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .trim_start_matches('(')
                .trim_end_matches(')')
                .split(',')
                .map(|v| v.parse().unwrap())
                .collect(),
        )
    }
}

#[derive(Debug)]
struct Buttons(Box<[Button]>);

impl Deref for Buttons {
    type Target = [Button];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<'a> FromIterator<&'a str> for Buttons {
    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = &'a str>,
    {
        Self(iter.into_iter().map(Into::into).collect())
    }
}

#[derive(Debug)]
struct Joltage(Box<[usize]>);

impl From<&str> for Joltage {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .trim_start_matches('{')
                .trim_end_matches('}')
                .split(',')
                .map(|v| v.parse().unwrap())
                .collect(),
        )
    }
}

#[derive(Debug)]
struct Machine {
    /// Target lights.
    lights: Lights,
    buttons: Buttons,
    /// Target joltage.
    joltage: Joltage,
}

impl From<&str> for Machine {
    fn from(value: &str) -> Self {
        let mut it = value.trim().split_whitespace();
        let lights = it.next().unwrap().into();
        let joltage = it.next_back().unwrap().into();
        let buttons = it.collect();
        Self {
            lights,
            buttons,
            joltage,
        }
    }
}

impl Machine {
    #[must_use]
    fn configure_lights(&self) -> usize {
        let target_lights = self
            .lights
            .into_iter()
            .enumerate()
            .filter(|&(_, &light)| light)
            .map(|(i, _)| 2_usize.pow(i.try_into().unwrap()))
            .sum::<usize>();

        let buttons = self
            .buttons
            .into_iter()
            .map(|button| {
                button.iter().fold(0, |acc, target| {
                    acc | 2_usize.pow(u32::try_from(*target).unwrap())
                })
            })
            .collect::<Vec<_>>();

        let mut seen = HashSet::new();
        let mut pq = BinaryHeap::new();
        pq.push((Reverse(0), 0));

        while let Some(state) = pq.pop() {
            let steps = state.0.0;
            let lights = state.1;

            if lights == target_lights {
                return steps;
            }

            if !seen.insert(lights) {
                continue;
            }

            let nsteps = steps + 1;
            for button in &buttons {
                pq.push((Reverse(nsteps), lights ^ button));
            }
        }

        panic!("Could not find lights configuration");
    }
}

#[derive(Debug)]
struct Machines(Box<[Machine]>);

impl Deref for Machines {
    type Target = [Machine];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Machines {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Machines {
    #[must_use]
    fn configure_lights(&self) -> usize {
        self.iter().map(|machine| machine.configure_lights()).sum()
    }
}

fn p1(input: &str) -> usize {
    Machines::from(input).configure_lights()
}

fn p2(_input: &str) -> usize {
    //let x = Machines::from(input);
    0
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT0: &str = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
    const INPUT1: &str = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}";
    const INPUT2: &str = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}";

    fn input() -> String {
        vec![INPUT0, INPUT1, INPUT2].join("\n")
    }

    #[test]
    fn indicator_lights() {
        assert_eq!(p1(INPUT1), 3);
        assert_eq!(p1(INPUT2), 2);
    }

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT0), 2);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1(INPUT1), 3);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1(INPUT2), 2);
    }

    #[test]
    fn p1_res() {
        assert_eq!(p1(&input()), 7);
    }

    /*
    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT0), 10);
    }

    #[test]
    fn p2e2() {
        assert_eq!(p2(INPUT1), 12);
    }

    #[test]
    fn p2e3() {
        assert_eq!(p2(INPUT2), 11);
    }

    #[test]
    fn p2_res() {
        assert_eq!(p2(&input()), 33);
    }
    */
}
