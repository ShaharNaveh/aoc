use std::{
    cmp::Ordering,
    collections::{BTreeSet, HashMap},
    ops::{Deref, DerefMut},
};

use crate::utils::IVec2;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct MagicNumber(i32);

impl From<i32> for MagicNumber {
    fn from(value: i32) -> Self {
        Self(value)
    }
}

impl From<&str> for MagicNumber {
    fn from(value: &str) -> Self {
        Self(value.trim().parse().unwrap())
    }
}

impl Deref for MagicNumber {
    type Target = i32;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum Tile {
    Wall,
    OpenSpace,
}

impl Tile {
    const fn from_pos(pos: IVec2, magic_number: MagicNumber) -> Self {
        let IVec2 { x, y } = pos;

        let ones = ((x * x) + (3 * x) + (2 * x * y) + y + (y * y) + magic_number.0).count_ones();

        if ones.rem_euclid(2) == 0 {
            Self::OpenSpace
        } else {
            Self::Wall
        }
    }
}

#[derive(Clone, Debug, Default, Eq, PartialEq)]
struct Tiles(HashMap<IVec2, Tile>);

impl Deref for Tiles {
    type Target = HashMap<IVec2, Tile>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Tiles {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct State {
    steps: usize,
    pos: IVec2,
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        self.steps
            .cmp(&other.steps)
            .then_with(|| self.pos.x.cmp(&other.pos.x))
            .then_with(|| self.pos.y.cmp(&other.pos.y))
    }
}

fn walk<F>(pred: F, magic_number: MagicNumber) -> HashMap<IVec2, usize>
where
    F: Fn(State) -> bool,
{
    let mut tiles = Tiles::default();
    let mut states = BTreeSet::from([State {
        steps: 0,
        pos: IVec2::splat(1),
    }]);
    let mut costs = HashMap::new();

    while let Some(state) = states.pop_first() {
        let State { steps, pos } = state;

        let entry = costs.entry(pos).or_insert(usize::MAX);
        if steps < *entry {
            *entry = steps;
        } else {
            continue;
        }

        if pred(state) {
            break;
        }

        let nsteps = steps + 1;

        for offset in IVec2::NEIGHBORS_4 {
            let npos = pos + offset;
            if npos.x.is_negative() || npos.y.is_negative() {
                continue;
            }

            if *tiles
                .entry(npos)
                .or_insert_with(|| Tile::from_pos(npos, magic_number))
                == Tile::OpenSpace
            {
                states.insert(State {
                    steps: nsteps,
                    pos: npos,
                });
            }
        }
    }

    return costs;
}

fn p1(input: &str) -> usize {
    let end = IVec2::new(31, 39);
    walk(|state| state.pos == end, input.into())[&end]
}

fn p2(input: &str) -> usize {
    walk(|state| state.steps > 50, input.into())
        .values()
        .filter(|&x| *x <= 50)
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn formula() {
        let raw_grid = "
  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
";

        let expected_tiles = Tiles(
            raw_grid
                .trim()
                .lines()
                .filter(|line| line.contains('.') || line.contains('#'))
                .enumerate()
                .map(|(y, line)| {
                    line.trim()
                        .chars()
                        .filter(|c| matches!(c, '.' | '#'))
                        .enumerate()
                        .map(move |(x, c)| {
                            (
                                IVec2::new(x.try_into().unwrap(), y.try_into().unwrap()),
                                if c == '.' {
                                    Tile::OpenSpace
                                } else {
                                    Tile::Wall
                                },
                            )
                        })
                })
                .flatten()
                .collect(),
        );

        let n = 10.into();
        let tiles = Tiles(
            (0..=6)
                .map(|y| (0..=9).map(move |x| IVec2::new(x, y)))
                .flatten()
                .map(|pos| (pos, Tile::from_pos(pos, n)))
                .collect(),
        );

        for (pos, &val) in tiles.iter() {
            assert_eq!(Some(val), expected_tiles.get(pos).copied(), "{pos:?}");
        }
    }

    #[test]
    fn p1e1() {
        let end = IVec2::new(7, 4);
        assert_eq!(walk(|state| state.pos == end, 10.into())[&end], 11);
    }
}
