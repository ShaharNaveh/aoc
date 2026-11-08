use std::{
    collections::HashSet,
    fmt,
    ops::{Deref, DerefMut},
};

use util::{Day, IVec2, aoc_main};

#[derive(Clone, Debug)]
struct Lights {
    lights: HashSet<IVec2>,
    max_pos: IVec2,
    stuck_corners: bool,
}

impl Lights {
    const fn iter(self) -> LightsIter {
        LightsIter(self)
    }

    fn with_stuck_corners(&mut self, stuck_corners: bool) -> Self {
        self.stuck_corners = stuck_corners;
        let mut out = self.clone();
        out.turn_on_corners();
        out
    }

    fn turn_on_corners(&mut self) {
        let max_pos = self.max_pos;

        self.extend([
            IVec2::ZERO,
            IVec2::new(max_pos.x, 0),
            IVec2::new(0, max_pos.y),
            max_pos,
        ]);
    }
}

impl fmt::Display for Lights {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let max_pos = self.max_pos;
        for y in 0..=max_pos.y {
            if y > 0 {
                writeln!(f)?;
            }

            for x in 0..=max_pos.x {
                let pos = IVec2::new(x, y);
                write!(f, "{}", if self.contains(&pos) { '#' } else { '.' })?;
            }
        }

        Ok(())
    }
}

impl From<&str> for Lights {
    fn from(value: &str) -> Self {
        Self {
            lights: value
                .trim()
                .lines()
                .enumerate()
                .flat_map(|(y, line)| {
                    line.trim().char_indices().filter_map(move |(x, c)| {
                        (c == '#').then(|| IVec2::new(x.try_into().unwrap(), y.try_into().unwrap()))
                    })
                })
                .collect(),
            max_pos: IVec2::new(
                (value.trim().lines().next().unwrap().len() - 1)
                    .try_into()
                    .unwrap(),
                (value.trim().lines().count() - 1).try_into().unwrap(),
            ),
            stuck_corners: false,
        }
    }
}

impl Deref for Lights {
    type Target = HashSet<IVec2>;

    fn deref(&self) -> &Self::Target {
        &self.lights
    }
}

impl DerefMut for Lights {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.lights
    }
}

#[derive(Debug)]
struct LightsIter(Lights);

impl Iterator for LightsIter {
    type Item = Lights;

    fn next(&mut self) -> Option<Self::Item> {
        let max_pos = self.0.max_pos;
        self.0 = Lights {
            lights: (0..=max_pos.y)
                .into_iter()
                .flat_map(|y| (0..=max_pos.x).into_iter().map(move |x| IVec2::new(x, y)))
                .filter_map(|pos| {
                    let on = pos
                        .neighbors_8()
                        .iter()
                        .filter(|npos| self.0.contains(npos))
                        .count();

                    match on {
                        3 => Some(pos),
                        2 if self.0.contains(&pos) => Some(pos),
                        _ => None,
                    }
                })
                .collect(),
            ..self.0
        };

        if self.0.stuck_corners {
            self.0.turn_on_corners();
        }

        Some(self.0.clone())
    }
}

impl From<Lights> for LightsIter {
    fn from(value: Lights) -> Self {
        Self(value)
    }
}

struct Day18;

impl Day for Day18 {
    type Parsed = Lights;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().iter().nth(100 - 1).unwrap().len()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input
            .clone()
            .with_stuck_corners(true)
            .iter()
            .nth(100 - 1)
            .unwrap()
            .len()
    }
}

aoc_main!(Day18);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
.#.#.#
...##.
#....#
..#...
#.#..#
####..
";

    #[test]
    fn part1() {
        assert_eq!(Day18::parse(INPUT).iter().nth(4 - 1).unwrap().len(), 4);
    }

    #[test]
    fn part2() {
        assert_eq!(
            Day18::parse(INPUT)
                .with_stuck_corners(true)
                .iter()
                .nth(5 - 1)
                .unwrap()
                .len(),
            17
        );
    }
}
