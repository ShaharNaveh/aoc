use std::collections::{HashMap, HashSet};

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

fn p1(input: &str) -> usize {
    let mut seen = HashSet::new();
    parse_puzzle(&input)
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

fn p2(input: &str) -> usize {
    let mut seen = HashMap::new();
    parse_puzzle(&input)
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

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let input = "0 2 7 0";
        assert_eq!(p1(input), 5);
    }

    #[test]
    fn p2e1() {
        let input = "0 2 7 0";
        assert_eq!(p2(input), 4);
    }
}
