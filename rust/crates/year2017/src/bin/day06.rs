use std::collections::{HashMap, HashSet};

use util::{Day, aoc_main};

#[derive(Clone, Eq, Hash, PartialEq)]
struct Memory(Vec<u8>);

impl From<&str> for Memory {
    fn from(raw: &str) -> Self {
        Self(
            raw.trim()
                .split_whitespace()
                .map(|w| w.parse().unwrap())
                .collect(),
        )
    }
}

impl Iterator for Memory {
    type Item = Memory;

    fn next(&mut self) -> Option<Self::Item> {
        let (bank, value) = self
            .0
            .iter()
            .enumerate()
            .max_by_key(|&(i, v)| (v, std::cmp::Reverse(i)))
            .map(|(i, v)| (i.clone(), v.clone()))
            .unwrap();

        self.0[bank] = 0;

        let len = self.0.len();
        (1..=value as usize)
            .map(|offset| (bank + offset) % len)
            .map(|idx| self.0[idx] += 1)
            .for_each(drop);

        Some(self.clone())
    }
}

fn parse_puzzle(input: &str) -> Memory {
    input.into()
}

struct Day06;

impl Day for Day06 {
    type Parsed = Memory;

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> usize {
        let mut seen = HashSet::new();
        input
            .clone()
            .into_iter()
            .enumerate()
            .find_map(|(i, mem)| {
                if !seen.insert(mem.clone()) {
                    Some(i + 1)
                } else {
                    None
                }
            })
            .unwrap()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut seen = HashMap::new();
        input
            .clone()
            .into_iter()
            .enumerate()
            .find_map(|(i, mem)| {
                if seen.contains_key(&mem) {
                    Some(i - seen[&mem])
                } else {
                    seen.insert(mem.clone(), i);
                    None
                }
            })
            .unwrap()
    }
}

aoc_main!(Day06);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let input = "0 2 7 0";
        assert_eq!(Day06::part1(&Day06::parse(input)), 5);
    }

    #[test]
    fn p2e1() {
        let input = "0 2 7 0";
        assert_eq!(Day06::part2(&Day06::parse(input)), 4);
    }
}
