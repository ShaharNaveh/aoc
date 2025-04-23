use std::{collections::BTreeMap, hash::Hash};

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

fn p1(input: &str) -> usize {
    parse_puzzle(input)
        .into_iter()
        .map(|passphrase| Counter::from_iter(passphrase.split_whitespace()))
        .filter(|counter| counter.values().all(|v| *v == 1))
        .count()
}

fn p2(input: &str) -> usize {
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

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("aa bb cc dd ee"), 1);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1("aa bb cc dd aa"), 0);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1("aa bb cc dd aaa"), 1);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2("abcde fghij"), 1);
    }

    #[test]
    fn p2e2() {
        assert_eq!(p2("abcde xyz ecdab"), 0);
    }

    #[test]
    fn p2e3() {
        assert_eq!(p2("a ab abc abd abf abj"), 1);
    }

    #[test]
    fn p2e4() {
        assert_eq!(p2("iiii oiii ooii oooi oooo"), 1);
    }

    #[test]
    fn p2e5() {
        assert_eq!(p2("oiii ioii iioi iiio"), 0);
    }
}
