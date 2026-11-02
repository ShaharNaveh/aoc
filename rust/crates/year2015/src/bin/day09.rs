use std::{collections::HashMap, ops::Deref};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Pair<'a> {
    x: &'a str,
    y: &'a str,
}

#[derive(Clone, Debug)]
struct Nodes<'a>(HashMap<Pair<'a>, usize>);

impl<'a> From<&'a str> for Nodes<'a> {
    fn from(value: &'a str) -> Self {
        todo!()
    }
}

struct Day09<'a>;

impl<'a> Day for Day09<'a> {
    type Parsed = Nodes<'a>;

    fn parse(input: &'a str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        0
    }

    fn part2(_input: &Self::Parsed) -> usize {
        0
    }
}

aoc_main!(Day09);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        assert_eq!(
            Day09::part1(&Day09::parse(
                "
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
"
            )),
            605
        );
    }
}
