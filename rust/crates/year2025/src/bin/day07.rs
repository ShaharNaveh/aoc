use std::{
    collections::{HashMap, HashSet},
    ops::{Deref, DerefMut},
};

use util::{Day, Vec2, aoc_main};

type IVec2 = Vec2<isize>;

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

#[derive(Clone, Debug)]
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

struct Day07;

impl Day for Day07 {
    type Parsed = Tachyon;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let mut tachyon = input.clone();
        tachyon.simulate();
        tachyon.splitter_hits
    }

    fn part2(input: &Self::Parsed) -> usize {
        let mut tachyon = input.clone();
        tachyon.simulate();
        tachyon.beams.values().sum()
    }
}

aoc_main!(Day07);

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
    fn part1() {
        let parsed = Day07::parse(INPUT);
        assert_eq!(Day07::part1(&parsed), 21);
    }

    #[test]
    fn part2() {
        let parsed = Day07::parse(INPUT);
        assert_eq!(Day07::part2(&parsed), 40);
    }
}
