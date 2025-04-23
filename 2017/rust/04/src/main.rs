use std::{collections::BTreeMap, hash::Hash};

const PUZZLE_FILE: &str = "puzzle.txt";

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

fn parse_puzzle(inp: &str) -> Vec<&str> {
    inp.trim().lines().collect()
}

fn p1(inp: &str) -> usize {
    parse_puzzle(inp)
        .into_iter()
        .map(|passphrase| Counter::from_iter(passphrase.split_whitespace()))
        .filter(|counter| counter.values().all(|v| *v == 1))
        .count()
}

fn p2(inp: &str) -> usize {
    parse_puzzle(inp)
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

fn main() {
    let inp = std::fs::read_to_string(PUZZLE_FILE).unwrap();
    println!("{}", p1(&inp));
    println!("{}", p2(&inp));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let inp = "aa bb cc dd ee";
        assert_eq!(p1(inp), 1);
    }

    #[test]
    fn p1e2() {
        let inp = "aa bb cc dd aa";
        assert_eq!(p1(inp), 0);
    }

    #[test]
    fn p1e3() {
        let inp = "aa bb cc dd aaa";
        assert_eq!(p1(inp), 1);
    }

    #[test]
    fn p2e1() {
        let inp = "abcde fghij";
        assert_eq!(p2(inp), 1);
    }

    #[test]
    fn p2e2() {
        let inp = "abcde xyz ecdab";
        assert_eq!(p2(inp), 0);
    }

    #[test]
    fn p2e3() {
        let inp = "a ab abc abd abf abj";
        assert_eq!(p2(inp), 1);
    }

    #[test]
    fn p2e4() {
        let inp = "iiii oiii ooii oooi oooo";
        assert_eq!(p2(inp), 1);
    }

    #[test]
    fn p2e5() {
        let inp = "oiii ioii iioi iiio";
        assert_eq!(p2(inp), 0);
    }
}
