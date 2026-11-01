use std::ops::{Deref, DerefMut, RangeInclusive};

use util::{Day, aoc_main};

#[derive(Debug)]
struct Firewall {
    blocked: Vec<RangeInclusive<u32>>,
}

impl From<&str> for Firewall {
    fn from(value: &str) -> Self {
        let mut blocked = value
            .trim()
            .lines()
            .map(|l| {
                let (start, last) = l.trim().split_once('-').unwrap();
                start.parse().unwrap()..=last.parse().unwrap()
            })
            .collect::<Vec<_>>();

        blocked.sort_by_key(|r| *r.start());

        let mut optimized: Vec<RangeInclusive<u32>> = vec![];
        for range in blocked {
            if let Some(last) = optimized.last_mut() {
                if *range.start() <= last.end().saturating_add(1) {
                    if range.end() > last.end() {
                        *last = *last.start()..=*range.end();
                    }

                    continue;
                }
            }
            optimized.push(range);
        }

        Self { blocked: optimized }
    }
}

impl Deref for Firewall {
    type Target = Vec<RangeInclusive<u32>>;

    fn deref(&self) -> &Self::Target {
        &self.blocked
    }
}

impl DerefMut for Firewall {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.blocked
    }
}

struct Day20;

impl Day for Day20 {
    type Parsed = Firewall;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> u32 {
        input.first().unwrap().end() + 1
    }

    fn part2(input: &Self::Parsed) -> u32 {
        (u32::MAX - input.iter().map(|r| r.end() - r.start() + 1).sum::<u32>()) + 1
    }
}

aoc_main!(Day20);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]

    fn p1e1() {
        let fw = Firewall::from(
            "
5-8
0-2
4-7
            ",
        );

        assert_eq!(
            (0..=9)
                .into_iter()
                .filter(|n| fw.iter().all(|range| !range.contains(&n)))
                .collect::<Vec<_>>(),
            [3, 9]
        );
    }
}
