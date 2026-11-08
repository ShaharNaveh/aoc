use std::ops::Deref;

use util::{Day, aoc_main};

#[derive(Debug)]
struct Containers(Vec<usize>);

impl Containers {
    fn combinations<'a>(&'a self, liters: usize) -> impl Iterator<Item = Vec<&'a usize>> + 'a {
        Combinations::from(self.as_slice())
            .into_iter()
            .filter(move |comb| liters == comb.iter().copied().sum())
    }

    fn possible_min_combinations(&self, liters: usize) -> usize {
        let mut it = self.combinations(liters);
        let min_len = it.next().unwrap().len();

        it.take_while(|comb| comb.len() == min_len).count() + 1
    }
}

impl From<Vec<usize>> for Containers {
    fn from(value: Vec<usize>) -> Self {
        Self(value)
    }
}

impl From<&str> for Containers {
    fn from(value: &str) -> Self {
        Self(
            value
                .split_ascii_whitespace()
                .map(|x| x.parse().unwrap())
                .collect(),
        )
    }
}

impl Deref for Containers {
    type Target = Vec<usize>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct Combinations<'a, T> {
    items: &'a [T],
    /// Current combination length.
    len: usize,
    idx: Vec<usize>,
    /// true if [`Self::idx`] hasn't been yielded yet for this [`Self::len`].
    fresh: bool,
}

impl<'a, T> From<&'a [T]> for Combinations<'a, T> {
    fn from(items: &'a [T]) -> Self {
        Self {
            items,
            len: 0,
            idx: vec![],
            fresh: true,
        }
    }
}

impl<'a, T> Iterator for Combinations<'a, T> {
    type Item = Vec<&'a T>;

    fn next(&mut self) -> Option<Self::Item> {
        let n = self.items.len();
        loop {
            if self.len > n {
                return None;
            }

            if self.fresh {
                self.fresh = false;
                self.idx = (0..self.len).collect();
            } else {
                // find rightmost index that can be incremented.
                if let Some(i) = (0..self.len)
                    .rev()
                    .find(|&i| self.idx[i] != i + n - self.len)
                {
                    self.idx[i] += 1;
                    ((i + 1)..self.len).for_each(|j| self.idx[j] = self.idx[j - 1] + 1);
                } else {
                    self.len += 1;
                    self.fresh = true;
                    continue;
                }
            }

            return Some(self.idx.iter().map(|&i| &self.items[i]).collect());
        }
    }
}

struct Day17;

impl Day for Day17 {
    type Parsed = Containers;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.combinations(150).count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.possible_min_combinations(150)
    }
}

aoc_main!(Day17);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
20
15
10
5
5
";

    #[test]
    fn part1() {
        assert_eq!(Day17::parse(INPUT).combinations(25).count(), 4);
    }

    #[test]
    fn part2() {
        assert_eq!(Day17::parse(INPUT).possible_min_combinations(25), 3);
    }
}
