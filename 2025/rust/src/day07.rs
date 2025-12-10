use std::{
    collections::{HashMap, HashSet},
    ops::{Deref, DerefMut},
};

use crate::utils::IVec2;

#[derive(Clone, Debug, Default)]
struct Beams(HashMap<IVec2, usize>);

impl Deref for Beams {
    type Target = HashMap<IVec2, usize>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Beams {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Beams {
    fn hit(&mut self, key: IVec2, value: usize) {
        *self.entry(key).or_insert(0) += value;
    }
}

#[derive(Debug)]
struct Tachyon {
    beams: Beams,
    splitters: HashSet<IVec2>,
    max_pos: IVec2,
    splitter_hits: usize,
}

impl From<&str> for Tachyon {
    fn from(value: &str) -> Self {
        let mut max_pos = IVec2::ZERO;
        let mut beams = Beams::default();
        let mut splitters = HashSet::new();

        for (y, line) in value.trim().lines().enumerate() {
            for (x, ch) in line.chars().enumerate() {
                let pos = IVec2::new(x as isize, y as isize);
                match ch {
                    'S' => beams.hit(pos, 1),
                    '^' => {
                        splitters.insert(pos);
                    }
                    _ => max_pos = max_pos.max(pos),
                };
            }
        }

        Self {
            beams,
            splitters,
            max_pos,
            splitter_hits: 0,
        }
    }
}

impl Tachyon {
    fn simulate(&mut self) {
        loop {
            let mut nbeams = Beams::default();

            for (&beam, &count) in self.beams.iter() {
                if beam.y == self.max_pos.y {
                    return;
                }

                let nbeam = beam + IVec2::Y;
                if self.splitters.contains(&nbeam) {
                    self.splitter_hits += 1;
                    nbeams.hit(nbeam + IVec2::X, count);
                    nbeams.hit(nbeam + IVec2::NEG_X, count);
                } else {
                    nbeams.hit(nbeam, count);
                }
            }

            self.beams = nbeams;
        }
    }
}

fn p1(input: &str) -> usize {
    let mut tachyon = Tachyon::from(input);
    tachyon.simulate();
    tachyon.splitter_hits
}

fn p2(input: &str) -> usize {
    let mut tachyon = Tachyon::from(input);
    tachyon.simulate();
    tachyon.beams.values().sum()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 21);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 40);
    }
}
