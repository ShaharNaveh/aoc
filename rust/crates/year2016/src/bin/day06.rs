use std::collections::HashMap;

use util::{Day, aoc_main};

#[derive(Debug)]
struct Messages(Vec<Vec<char>>);

impl Messages {
    fn counter(&self, idx: usize) -> HashMap<char, usize> {
        let mut counter = HashMap::new();
        for msg in &self.0 {
            *counter.entry(msg[idx]).or_insert(0) += 1;
        }
        counter
    }

    fn most_common_at(&self, idx: usize) -> char {
        self.counter(idx)
            .iter()
            .max_by_key(|&(_, v)| *v)
            .map(|(k, _)| *k)
            .unwrap()
    }

    fn least_common_at(&self, idx: usize) -> char {
        self.counter(idx)
            .iter()
            .min_by_key(|&(_, v)| *v)
            .map(|(k, _)| *k)
            .unwrap()
    }

    fn to_corrected(&self) -> String {
        let len = self.0[0].len();
        let mut buf = String::new();
        for idx in 0..len {
            buf.push(self.most_common_at(idx));
        }
        buf
    }

    fn to_original(&self) -> String {
        let len = self.0[0].len();
        let mut buf = String::new();
        for idx in 0..len {
            buf.push(self.least_common_at(idx));
        }
        buf
    }
}

impl From<&str> for Messages {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|s| s.trim())
                .filter(|l| !l.is_empty())
                .map(|s| s.chars().collect())
                .collect(),
        )
    }
}

struct Day06;

impl Day for Day06 {
    type Parsed = Messages;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> String {
        input.to_corrected()
    }

    fn part2(input: &Self::Parsed) -> String {
        input.to_original()
    }
}

aoc_main!(Day06);

#[cfg(test)]
mod tests {
    use super::*;

    const MSG: &str = "
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
";

    #[test]
    fn part1() {
        let parsed = Day06::parse(MSG);
        assert_eq!(Day06::part1(&parsed), "easter");
    }

    #[test]
    fn part2() {
        let parsed = Day06::parse(MSG);
        assert_eq!(Day06::part2(&parsed), "advent");
    }
}
