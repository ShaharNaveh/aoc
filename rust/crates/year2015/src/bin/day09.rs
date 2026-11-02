use std::{
    cmp::Ordering,
    collections::{BTreeSet, HashMap},
    ops::{Deref, DerefMut},
};

use util::{Day, aoc_main, calculate_hash};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Location(u64);

impl From<&str> for Location {
    fn from(value: &str) -> Self {
        Self(calculate_hash(&value))
    }
}

#[derive(Clone, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Locations(BTreeSet<Location>);

impl From<&Nodes> for Locations {
    fn from(value: &Nodes) -> Self {
        Self(value.keys().flat_map(|pair| [pair.from, pair.to]).collect())
    }
}

impl From<BTreeSet<Location>> for Locations {
    fn from(value: BTreeSet<Location>) -> Self {
        Self(value)
    }
}

impl Deref for Locations {
    type Target = BTreeSet<Location>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Locations {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Pair {
    from: Location,
    to: Location,
}

impl From<&str> for Pair {
    fn from(value: &str) -> Self {
        let (from, to) = value.trim().split_once("to").unwrap();

        Self::new(from.trim().into(), to.trim().into())
    }
}

impl Pair {
    fn new(x: Location, y: Location) -> Self {
        if x > y {
            Self { from: x, to: y }
        } else {
            Self { from: y, to: x }
        }
    }
}

#[derive(Clone, Debug)]
struct Nodes(HashMap<Pair, usize>);

impl Nodes {
    fn locations(&self) -> Locations {
        self.into()
    }

    fn search<const MAX: bool>(&self) -> usize {
        let locations = self.locations();

        let mut pq = locations
            .iter()
            .map(|loc| State::<MAX>::new(0, *loc, Locations::default()))
            .collect::<BTreeSet<_>>();

        let mut res = None;
        while let Some(State {
            dist,
            loc,
            mut visited,
        }) = pq.pop_first()
        {
            visited.insert(loc);

            if visited == locations {
                res =
                    Some(res.map_or(dist, |x: usize| if MAX { x.max(dist) } else { x.min(dist) }));
                continue;
            }

            for &nloc in locations.difference(&visited) {
                let npair = Pair::new(loc, nloc);
                let ndist = dist + self[&npair];
                pq.insert(State::<MAX>::new(ndist, nloc, visited.clone()));
            }
        }

        res.expect("Did not find path")
    }
}

impl Deref for Nodes {
    type Target = HashMap<Pair, usize>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Nodes {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| {
                    line.split_once('=')
                        .map(|(pair, dist)| (pair.into(), dist.trim().parse().unwrap()))
                        .unwrap()
                })
                .collect(),
        )
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct State<const MAX: bool> {
    dist: usize,
    loc: Location,
    visited: Locations,
}

impl<const MAX: bool> State<MAX> {
    const fn new(dist: usize, loc: Location, visited: Locations) -> Self {
        Self { dist, loc, visited }
    }
}

impl<const MAX: bool> Ord for State<MAX> {
    fn cmp(&self, other: &Self) -> Ordering {
        let res = self
            .dist
            .cmp(&other.dist)
            .then(self.visited.cmp(&other.visited))
            .then(self.loc.cmp(&other.loc));

        if MAX { res.reverse() } else { res }
    }
}

impl<const MAX: bool> PartialOrd for State<MAX> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

struct Day09;

impl Day for Day09 {
    type Parsed = Nodes;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.search::<false>()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.search::<true>()
    }
}

aoc_main!(Day09);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141
";

    #[test]
    fn part1() {
        assert_eq!(Day09::part1(&Day09::parse(INPUT)), 605);
    }

    #[test]
    fn part2() {
        assert_eq!(Day09::part2(&Day09::parse(INPUT)), 982);
    }
}
