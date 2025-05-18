use std::{
    collections::HashMap,
    ops::{Index, IndexMut},
};

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct Grid(Vec<Vec<bool>>);

impl Grid {
    #[inline]
    #[must_use]
    fn new(size: usize) -> Self {
        let row = vec![false; size];
        Self(vec![row; size])
    }

    #[inline]
    #[must_use]
    fn size(&self) -> usize {
        self.0.len()
    }

    #[inline]
    #[must_use]
    fn flip(&self) -> Self {
        Self(
            self.0
                .iter()
                .map(|row| row.iter().rev().map(|&v| v).collect())
                .collect(),
        )
    }

    #[must_use]
    fn rotate(&self) -> Self {
        let n = self.size();
        let mut rotated = Self::new(n);
        for x in 0..n {
            for y in 0..n {
                rotated[n - x - 1][y] = self[y][x];
            }
        }
        rotated
    }

    #[must_use]
    fn iter_possible_variations(&self) -> impl Iterator<Item = Self> {
        let mut grid = self.clone();
        std::iter::once(grid.clone()).chain((0..7).map(move |i| {
            if i == 3 {
                grid = grid.flip();
            }
            grid = grid.rotate();

            grid.clone()
        }))
    }

    #[must_use]
    fn iter_subgrids(&self) -> impl Iterator<Item = Self> {
        let len = self.size();
        let n = if len % 2 == 0 { 2 } else { 3 };
        let subgrid_size = len / n;

        (0..(subgrid_size * subgrid_size)).map(move |idx| {
            let mut subgrid = Self::new(n);

            let gx = idx % subgrid_size;
            let gy = idx / subgrid_size;
            for x in 0..n {
                for y in 0..n {
                    subgrid[y][x] = self[y + gy * n][x + gx * n];
                }
            }
            subgrid
        })
    }

    #[inline]
    #[must_use]
    fn count(&self) -> usize {
        self.0.iter().flatten().filter(|&&v| v).count()
    }
}

impl FromIterator<Grid> for Grid {
    fn from_iter<T>(iter: T) -> Self
    where
        T: IntoIterator<Item = Self>,
    {
        let parts = iter.into_iter().collect::<Vec<_>>();
        let width = (parts.len() as f64).sqrt() as usize;
        let height = parts[0].size();

        let mut grid = Self::new(width * height);
        for (idx, subgrid) in parts.iter().enumerate() {
            let gx = idx % width;
            let gy = idx / width;
            for x in 0..height {
                for y in 0..height {
                    grid[y + gy * height][x + gx * height] = subgrid[y][x];
                }
            }
        }

        grid
    }
}

impl Index<usize> for Grid {
    type Output = Vec<bool>;
    #[inline]
    fn index(&self, y: usize) -> &Self::Output {
        &self.0[y]
    }
}

impl IndexMut<usize> for Grid {
    #[inline]
    fn index_mut(&mut self, y: usize) -> &mut Self::Output {
        &mut self.0[y]
    }
}

impl Default for Grid {
    #[inline]
    fn default() -> Self {
        Self::from(".#./..#/###")
    }
}

impl From<&str> for Grid {
    fn from(raw: &str) -> Self {
        Self(
            raw.trim()
                .split('/')
                .map(|s| s.trim().chars().map(|c| c == '#').collect())
                .collect(),
        )
    }
}

#[derive(Clone, Debug)]
struct Rules(HashMap<Grid, Grid>);

impl Rules {
    fn enhance(&self, grid: &Grid) -> Grid {
        self.0.get(grid).unwrap_or(grid).clone()
    }
}

impl From<&str> for Rules {
    fn from(raw: &str) -> Self {
        Self(
            raw.trim()
                .lines()
                .filter_map(|line| line.split_once(" => "))
                .map(|(raw_src, raw_dest)| (Grid::from(raw_src), Grid::from(raw_dest)))
                .map(|(src, dest)| {
                    src.iter_possible_variations()
                        .map(|p| (p, dest.clone()))
                        .collect::<Vec<_>>()
                })
                .flatten()
                .collect(),
        )
    }
}

fn parse_puzzle(input: &str) -> (Grid, Rules) {
    (Grid::default(), input.into())
}

fn main(input: &str, t: usize) -> usize {
    let (mut grid, rules) = parse_puzzle(input);
    for _ in 0..t {
        grid = grid
            .iter_subgrids()
            .map(|subgrid| rules.enhance(&subgrid))
            .collect();
    }
    grid.count()
}

fn p1(input: &str) -> usize {
    main(input, 5)
}

fn p2(input: &str) -> usize {
    main(input, 18)
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]

    fn p1e1() {
        let input = "
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
"
        .trim();
        assert_eq!(main(input, 2), 12);
    }
}
