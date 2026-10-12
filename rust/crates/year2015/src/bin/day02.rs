use std::ops::Deref;

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
struct Present {
    l: usize,
    w: usize,
    h: usize,
}

impl Present {
    fn wrapping_paper(self) -> usize {
        let Self { h, w, l } = self;
        let a = l * w;
        let b = w * h;
        let c = h * l;

        let surface_area = 2 * a + 2 * b + 2 * c;
        let smallest_side = a.min(b).min(c);
        surface_area + smallest_side
    }

    fn ribbon(self) -> usize {
        let Self { h, w, l } = self;
        let mut sides = vec![h, w, l];
        sides.sort_unstable();

        let shortest_dist = sides[0] * 2 + sides[1] * 2;
        let volume = h * w * l;

        shortest_dist + volume
    }
}

impl From<&str> for Present {
    fn from(value: &str) -> Self {
        let [l, w, h] = value
            .trim()
            .split('x')
            .map(|s| s.parse().unwrap())
            .collect::<Vec<_>>()[..]
        else {
            unreachable!()
        };

        Self { l, w, h }
    }
}

#[derive(Debug)]
struct Presents(Box<[Present]>);

impl From<&str> for Presents {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Presents {
    type Target = Box<[Present]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day02;

impl Day for Day02 {
    type Parsed = Presents;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.iter().map(|p| p.wrapping_paper()).sum()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.iter().map(|p| p.ribbon()).sum()
    }
}

aoc_main!(Day02);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [("2x3x4", 58), ("1x1x10", 43)] {
            let parsed = Day02::parse(input);
            assert_eq!(Day02::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [("2x3x4", 34), ("1x1x10", 14)] {
            let parsed = Day02::parse(input);
            assert_eq!(Day02::part2(&parsed), expected, "{input}");
        }
    }
}
