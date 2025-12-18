use std::{
    cmp::Reverse,
    collections::{BinaryHeap, HashSet},
    ops::{Deref, DerefMut},
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

#[derive(Clone, Debug)]
struct Joltage(Box<[usize]>);

impl Deref for Joltage {
    type Target = [usize];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Joltage {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

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

    #[must_use]
    fn configure_joltage(&self) -> usize {
        let buttons_mask = (1 << self.buttons.len()) - 1;
        Self::configure_joltage_impl(&self.joltage, buttons_mask, &self.buttons)
    }

    #[must_use]
    const fn is_button_available(i: usize, mask: u32) -> bool {
        mask & (1 << i) > 0
    }

    #[must_use]
    fn configure_joltage_impl(joltage: &Joltage, buttons_mask: u32, buttons: &Buttons) -> usize {
        if joltage.iter().all(|v| *v == 0) {
            return 0;
        }

        // Find the joltage value with the lowest number of combinations of buttons to try.
        //
        // If multiple joltage values are affected by the same number of buttons,
        // select the highest value
        let (min_idx, &min_joltage) = joltage
            .iter()
            .enumerate()
            .filter(|&(_, &v)| v > 0)
            .min_by_key(|&(i, &v)| {
                (
                    // lowest number of buttons
                    buttons
                        .iter()
                        .enumerate()
                        .filter(|&(j, button)| {
                            Self::is_button_available(j, buttons_mask) && button.contains(&i)
                        })
                        .count(),
                    // highest joltage value (Reverse because we're using `min_by_key`)
                    Reverse(v),
                )
            })
            .unwrap();

        // Buttons that target `min_idx`
        let matching_buttons = buttons
            .iter()
            .enumerate()
            .filter(|&(i, button)| {
                Self::is_button_available(i, buttons_mask) && button.contains(&min_idx)
            })
            .collect::<Vec<_>>();

        let mut result = usize::MAX;

        if matching_buttons.is_empty() {
            return result;
        }
        let new_mask = matching_buttons
            .iter()
            .map(|(i, _)| i)
            .fold(buttons_mask, |acc, i| acc & !(1 << i));

        let mut new_joltage = joltage.clone();
        let mut counts = vec![0; matching_buttons.len() - 1];
        counts.push(min_joltage);

        loop {
            let mut is_ok = true;
            new_joltage.copy_from_slice(joltage);

            'buttons: for (bi, &count) in counts.iter().enumerate() {
                if count == 0 {
                    continue;
                }

                for &button_target in matching_buttons[bi].1.iter() {
                    if new_joltage[button_target] >= count {
                        new_joltage[button_target] -= count;
                    } else {
                        is_ok = false;
                        break 'buttons;
                    }
                }
            }

            if is_ok {
                let res = Self::configure_joltage_impl(&new_joltage, new_mask, buttons);
                if res != usize::MAX {
                    result = result.min(min_joltage + res);
                }
            }

            let i = counts.iter().rposition(|&v| v != 0).unwrap();
            if i == 0 {
                break;
            }
            let v = counts[i];
            counts[i - 1] += 1;
            counts[i] = 0;
            *counts.last_mut().unwrap() = v - 1;
        }

        result
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

    #[must_use]
    fn configure_joltage(&self) -> usize {
        self.iter().map(|machine| machine.configure_joltage()).sum()
    }
}

fn p1(input: &str) -> usize {
    Machines::from(input).configure_lights()
}

fn p2(input: &str) -> usize {
    Machines::from(input).configure_joltage()
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
}
