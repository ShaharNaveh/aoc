use std::{collections::BTreeMap, hash::Hash};

use util::{Day, aoc_main};

#[derive(Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Counter<T>(BTreeMap<T, usize>);

impl<T: Eq + Hash + Ord> Counter<T> {
    fn new() -> Self {
        Self(BTreeMap::new())
    }

    fn from_iter<I>(iter: I) -> Self
    where
        I: IntoIterator<Item = T>,
    {
        let mut counter = Self::new();
        for item in iter {
            *counter.0.entry(item).or_insert(0) += 1;
        }
        counter
    }

    fn values(&self) -> impl Iterator<Item = &usize> {
        self.0.values()
    }
}

fn parse_puzzle(input: &str) -> Vec<&str> {
    input.trim().lines().collect()
}

struct Day04;

impl Day for Day04 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.to_string()
    }

    fn part1(input: &Self::Parsed) -> usize {
        parse_puzzle(input)
            .into_iter()
            .map(|passphrase| Counter::from_iter(passphrase.split_whitespace()))
            .filter(|counter| counter.values().all(|v| *v == 1))
            .count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        parse_puzzle(input)
            .into_iter()
            .map(|passphrase| {
                Counter::from_iter(
                    passphrase
                        .split_whitespace()
                        .map(|word| Counter::from_iter(word.chars())),
                )
            })
            .filter(|counter| counter.values().all(|v| *v == 1))
            .count()
    }
}

aoc_main!(Day04);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [
            ("aa bb cc dd ee", 1),
            ("aa bb cc dd aa", 0),
            ("aa bb cc dd aaa", 1),
        ] {
            let parsed = Day04::parse(input);
            assert_eq!(Day04::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [
            ("abcde fghij", 1),
            ("abcde xyz ecdab", 0),
            ("a ab abc abd abf abj", 1),
            ("iiii oiii ooii oooi oooo", 1),
            ("oiii ioii iioi iiio", 0),
        ] {
            let parsed = Day04::parse(input);
            assert_eq!(Day04::part2(&parsed), expected, "{input}");
        }
    }
}
