use std::{collections::HashSet, ops::RangeInclusive};

use util::{Day, aoc_main};

#[derive(Debug)]
struct Inventory {
    ranges: HashSet<RangeInclusive<u64>>,
    ids: HashSet<u64>,
}

impl From<&str> for Inventory {
    fn from(value: &str) -> Self {
        let (ranges_chunk, ids_chunk) = value.trim().split_once("\n\n").unwrap();

        let mut all_ranges = ranges_chunk
            .lines()
            .map(|line| line.split_once('-').unwrap())
            .map(|(start, end)| RangeInclusive::new(start.parse().unwrap(), end.parse().unwrap()))
            .collect::<Vec<_>>();

        // Some ranges overlap. Merge what's possible
        all_ranges.sort_by_key(|r| *r.start());
        let mut ranges: Vec<RangeInclusive<u64>> = vec![];

        for range in all_ranges {
            let (start, end) = range.into_inner();

            if let Some(last) = ranges.last_mut() {
                let last_end = *last.end();
                if start <= last_end + 1 {
                    let new_end = last_end.max(end);
                    *last = *last.start()..=new_end;
                    continue;
                }
            }

            ranges.push(start..=end);
        }

        let ids = ids_chunk
            .lines()
            .map(|line| line.parse().unwrap())
            .collect();
        Self {
            ranges: ranges.into_iter().collect(),
            ids,
        }
    }
}

impl Inventory {
    fn fresh_ids_count(&self) -> usize {
        self.ids
            .clone()
            .into_iter()
            .filter(|id| self.ranges.iter().any(|range| range.contains(id)))
            .count()
    }

    fn possible_fresh_ids_count(&self) -> usize {
        self.ranges
            .clone()
            .into_iter()
            .map(|range| range.into_iter().count())
            .sum()
    }
}

struct Day05;

impl Day for Day05 {
    type Parsed = Inventory;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.fresh_ids_count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.possible_fresh_ids_count()
    }
}

aoc_main!(Day05);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
3-5
10-14
16-20
12-18

1
5
8
11
17
32
";

    #[test]
    fn part1() {
        let parsed = Day05::parse(INPUT);
        assert_eq!(Day05::part1(&parsed), 3);
    }

    #[test]
    fn part2() {
        let parsed = Day05::parse(INPUT);
        assert_eq!(Day05::part2(&parsed), 14);
    }
}
