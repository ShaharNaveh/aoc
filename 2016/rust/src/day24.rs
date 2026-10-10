use std::{
    cmp::Ordering,
    collections::{BTreeSet, HashMap, HashSet},
    ops::{Deref, DerefMut},
};

use crate::utils::{IVec2, calculate_hash};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Pos(IVec2);

impl Deref for Pos {
    type Target = IVec2;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Pos {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl PartialOrd for Pos {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Pos {
    fn cmp(&self, other: &Self) -> Ordering {
        self.x.cmp(&other.x).then(self.y.cmp(&other.y))
    }
}

impl From<IVec2> for Pos {
    fn from(value: IVec2) -> Self {
        Self(value)
    }
}

#[derive(Clone, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Numbers(BTreeSet<Pos>);

impl<T> From<T> for Numbers
where
    T: Into<BTreeSet<Pos>>,
{
    fn from(value: T) -> Self {
        Self(value.into())
    }
}

impl Deref for Numbers {
    type Target = BTreeSet<Pos>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Numbers {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct Pair(Pos, Pos);

impl Pair {
    fn new(a: Pos, b: Pos) -> Self {
        match a.cmp(&b) {
            Ordering::Less => Self(a, b),
            Ordering::Greater => Self(b, a),
            Ordering::Equal => unreachable!(),
        }
    }
}

#[derive(Debug)]
struct Layout {
    tiles: HashSet<Pos>,
    numbers: Numbers,
    start: Pos,
}

impl From<&str> for Layout {
    fn from(value: &str) -> Self {
        let mut tiles = HashSet::new();
        let mut numbers = Numbers::default();

        let mut start = None;

        for (y, line) in value.trim().lines().enumerate() {
            for (x, ch) in line.trim().char_indices() {
                if ch == '#' {
                    continue;
                }

                let pos = IVec2::new(x.try_into().unwrap(), y.try_into().unwrap()).into();

                tiles.insert(pos);

                if ch != '.' {
                    numbers.insert(pos);
                }

                if ch == '0' {
                    start = Some(pos);
                }
            }
        }

        Self {
            tiles,
            numbers,
            start: start.unwrap(),
        }
    }
}

impl Layout {
    fn walk(&self, Pair(from, to): Pair) -> usize {
        let mut pq = BTreeSet::from([State::new(from)]);
        let mut seen = HashSet::new();

        while let Some(state) = pq.pop_first() {
            let State {
                steps,
                progress: Progress { pos, .. },
            } = state;

            if pos == to {
                return steps;
            }

            if !seen.insert(pos) {
                continue;
            }

            let nsteps = steps + 1;
            for npos in pos
                .neighbors_4()
                .into_iter()
                .map(Into::into)
                .filter(|p| self.tiles.contains(p))
            {
                pq.insert(State {
                    steps: nsteps,
                    progress: Progress {
                        pos: npos,
                        visited: Numbers::default(),
                    },
                });
            }
        }

        unreachable!()
    }

    fn solve(&self, is_p2: bool) -> usize {
        let mut pq = BTreeSet::from([State::new(self.start)]);
        let mut dists = HashMap::new();
        let mut seen = HashSet::new();

        let mut final_dists: HashMap<Pos, usize> = HashMap::new();

        while let Some(state) = pq.pop_first() {
            let State {
                steps,
                progress: Progress { pos, visited },
            } = state;

            if !seen.insert(calculate_hash(&(pos, &visited))) {
                continue;
            }

            if visited == self.numbers {
                if !is_p2 {
                    return steps;
                }

                debug_assert_ne!(pos, self.start, "finished at start pos");

                final_dists
                    .entry(pos)
                    .and_modify(|v| *v = (*v).min(steps))
                    .or_insert(steps);

                continue;
            }

            for &npos in self.numbers.difference(&visited) {
                let pair = Pair::new(pos, npos);

                let distance = *dists.entry(pair).or_insert_with_key(|p| self.walk(*p));

                let mut nvisited = visited.clone();
                nvisited.insert(npos);

                pq.insert(State {
                    steps: steps + distance,
                    progress: Progress {
                        pos: npos,
                        visited: nvisited,
                    },
                });
            }
        }

        debug_assert!(is_p2, "unreachable for part1");

        final_dists
            .into_iter()
            .map(|(pos, steps)| {
                let pair = Pair::new(self.start, pos);
                let distance = *dists.entry(pair).or_insert_with_key(|p| self.walk(*p));
                steps + distance
            })
            .min()
            .unwrap()
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq, Ord, PartialOrd)]
struct Progress {
    pos: Pos,
    visited: Numbers,
}

impl Progress {
    fn new(pos: Pos) -> Self {
        Self {
            pos,
            visited: Numbers::from([pos]),
        }
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct State {
    steps: usize,
    progress: Progress,
}

impl State {
    fn new(pos: Pos) -> Self {
        Self {
            steps: 0,
            progress: Progress::new(pos),
        }
    }
}

fn p1(input: &str) -> usize {
    Layout::from(input).solve(false)
}

fn p2(input: &str) -> usize {
    Layout::from(input).solve(true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(
            p1("
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
"),
            14
        );
    }
}
