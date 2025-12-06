use std::{collections::HashSet, ops::RangeInclusive};

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

fn p1(input: &str) -> usize {
    Inventory::from(input).fresh_ids_count()
}

fn p2(input: &str) -> usize {
    Inventory::from(input).possible_fresh_ids_count()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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
    fn p1e1() {
        assert_eq!(p1(INPUT), 3);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 14);
    }
}
