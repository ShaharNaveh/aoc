use std::ops::{Deref, DerefMut};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
enum Op {
    Add,
    Mul,
}

impl TryFrom<char> for Op {
    type Error = String;

    fn try_from(value: char) -> Result<Self, Self::Error> {
        Ok(match value {
            '+' => Self::Add,
            '*' => Self::Mul,
            _ => return Err(format!("Unkown op: '{value}'")),
        })
    }
}

#[derive(Clone, Debug)]
struct Problem {
    items: Vec<String>,
    op: Op,
}

impl Problem {
    #[must_use]
    const fn new(items: Vec<String>, op: Op) -> Self {
        Self { items, op }
    }

    #[must_use]
    fn solve(&self) -> u64 {
        let it = self
            .items
            .clone()
            .into_iter()
            .map(|item| item.trim().parse::<u64>().unwrap());

        match self.op {
            Op::Add => it.sum(),
            Op::Mul => it.product(),
        }
    }

    fn rtl(&mut self) {
        let cols = self.items[0].len();
        let rows = self.items.len();

        let items = (0..cols)
            .map(|col| {
                (0..rows)
                    .filter_map(|row| self.items[row].get(col..=col))
                    .collect::<String>()
            })
            .map(|s| s.trim().to_owned())
            .filter(|s| !s.is_empty())
            .collect();

        self.items = items;
    }
}

#[derive(Clone, Debug)]
struct Problems(Box<[Problem]>);

impl Deref for Problems {
    type Target = [Problem];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Problems {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Problems {
    fn from(value: &str) -> Self {
        let value = value.trim_start_matches('\n');
        let mut lines = value.lines();
        let op_line = lines.next_back().unwrap();
        // `util::run` trims trailing whitespace, so the op line may be shorter than the rest.
        let width = value.lines().map(str::len).max().unwrap();

        let mut sep_indexes = vec![];
        let mut ops = vec![];
        for (idx, c) in op_line.char_indices() {
            if let Ok(op) = Op::try_from(c) {
                ops.push(op);
                sep_indexes.push(idx);
            }
        }

        sep_indexes.push(width);
        let problem_ranges = sep_indexes
            .windows(2)
            .map(|w| w[0]..w[1])
            .collect::<Vec<_>>();

        let matrix = lines
            .map(|line| {
                problem_ranges
                    .clone()
                    .into_iter()
                    .filter_map(|range| line.get(range).map(String::from))
                    .collect::<Vec<_>>()
            })
            .collect::<Vec<_>>();

        let cols = matrix[0].len();
        let rows = matrix.len();
        let all_items = (0..cols)
            .map(|col| (0..rows).map(|row| matrix[row][col].clone()).collect())
            .collect::<Vec<_>>();

        Self(
            all_items
                .into_iter()
                .zip(ops)
                .map(|(items, op)| Problem::new(items, op))
                .collect(),
        )
    }
}

impl Problems {
    #[must_use]
    fn solve(&self) -> u64 {
        self.iter().map(|problem| problem.solve()).sum::<u64>()
    }

    #[must_use]
    fn rtl(&mut self) -> Self {
        self.iter_mut().for_each(|problem| problem.rtl());
        self.clone()
    }
}

struct Day06;

impl Day for Day06 {
    type Parsed = Problems;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> u64 {
        input.solve()
    }

    fn part2(input: &Self::Parsed) -> u64 {
        input.clone().rtl().solve()
    }
}

aoc_main!(Day06);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  
";

    #[test]
    fn part1() {
        for (input, expected) in [(INPUT, 4277556), (INPUT.trim_end(), 4277556)] {
            let parsed = Day06::parse(input);
            assert_eq!(Day06::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [(INPUT, 3263827), (INPUT.trim_end(), 3263827)] {
            let parsed = Day06::parse(input);
            assert_eq!(Day06::part2(&parsed), expected, "{input}");
        }
    }
}
