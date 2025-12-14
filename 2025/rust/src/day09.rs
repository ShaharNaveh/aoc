use std::{
    collections::HashSet,
    ops::{Deref, RangeInclusive},
};

use crate::utils::IVec2;

#[must_use]
fn combinations(n: usize) -> impl Iterator<Item = (usize, usize)> {
    (0..n).flat_map(move |left| ((left + 1)..n).map(move |right| (left, right)))
}

#[must_use]
fn calc_area(tile0: IVec2, tile1: IVec2) -> usize {
    ((tile0 - tile1).abs() + IVec2::ONE)
        .element_product()
        .try_into()
        .unwrap()
}

#[must_use]
fn largest_area<I>(iter: I) -> usize
where
    I: Iterator<Item = (IVec2, IVec2)>,
{
    iter.fold(usize::MIN, |max, (tile0, tile1)| {
        let area = calc_area(tile0, tile1);
        if area > max { area } else { max }
    })
}

#[derive(Debug, Eq, Hash, PartialEq)]
enum Axis {
    X { y: isize, xs: RangeInclusive<isize> },
    Y { x: isize, ys: RangeInclusive<isize> },
}

impl Axis {
    #[must_use]
    fn new(pos0: IVec2, pos1: IVec2) -> Self {
        if pos0.x == pos1.x {
            let min = pos0.min(pos1);
            let max = pos0.max(pos1);
            Self::Y {
                x: pos0.x,
                ys: min.y..=max.y - 1,
            }
        } else if pos0.y == pos1.y {
            let min = pos0.min(pos1);
            let max = pos0.max(pos1);
            Self::X {
                y: pos0.y,
                xs: min.x..=max.x - 1,
            }
        } else {
            panic!("{pos0:?} {pos1:?}")
        }
    }
}

#[derive(Debug)]
struct GreenTiles(HashSet<Axis>);

impl From<&RedTiles> for GreenTiles {
    fn from(red_tiles: &RedTiles) -> Self {
        let mut tiles = red_tiles.0.clone().into_vec();
        tiles.push(*tiles.first().unwrap());

        Self(
            tiles
                .windows(2)
                .map(|w| Axis::new(w[0], w[1]))
                .collect::<HashSet<_>>(),
        )
    }
}

impl GreenTiles {
    #[must_use]
    fn is_inside(&self, pos0: IVec2, pos1: IVec2) -> bool {
        let min = pos0.min(pos1);
        let max = pos0.max(pos1);

        for axis in self.iter() {
            match axis {
                Axis::X { y, xs } => {
                    let (x_start, x_end) = xs.clone().into_inner();
                    if min.y < *y && *y < max.y && min.x < x_end && x_start < max.x {
                        return false;
                    }
                }

                Axis::Y { x, ys } => {
                    let (y_start, y_end) = ys.clone().into_inner();
                    if min.x < *x && *x < max.x && min.y < y_end && y_start < max.y {
                        return false;
                    }
                }
            }
        }

        true
    }
}

impl Deref for GreenTiles {
    type Target = HashSet<Axis>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct RedTiles(Box<[IVec2]>);

impl Deref for RedTiles {
    type Target = [IVec2];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for RedTiles {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| {
                    let (x, y) = line.split_once(',').unwrap();
                    IVec2::new(x.parse().unwrap(), y.parse().unwrap())
                })
                .collect(),
        )
    }
}

impl RedTiles {
    #[must_use]
    fn corners(&self) -> impl Iterator<Item = (IVec2, IVec2)> {
        combinations(self.len()).map(|(idx0, idx1)| (self[idx0], self[idx1]))
    }

    #[must_use]
    fn largest_red(&self) -> usize {
        largest_area(self.corners())
    }

    #[must_use]
    fn largest_green(&self) -> usize {
        let green_tiles = GreenTiles::from(self);

        largest_area(
            self.corners()
                .filter(|&(tile0, tile1)| green_tiles.is_inside(tile0, tile1)),
        )
    }
}

fn p1(input: &str) -> usize {
    RedTiles::from(input).largest_red()
}

fn p2(input: &str) -> usize {
    RedTiles::from(input).largest_green()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 50);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 24);
    }
}
