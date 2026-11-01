use std::collections::HashSet;
use year2017::knot_hash::TieKnot;

use util::{Day, IVec2, aoc_main};

#[derive(Clone, Debug)]
struct Tiles(HashSet<IVec2>);

impl Tiles {
    fn tile_region(&self, tile: &IVec2) -> HashSet<IVec2> {
        let mut queue = vec![*tile];
        let mut region = HashSet::new();
        while let Some(pos) = queue.pop() {
            region.insert(pos);
            for npos in pos.neighbors_4() {
                if region.contains(&npos) || !self.0.contains(&npos) {
                    continue;
                }

                queue.push(npos);
            }
        }
        region
    }

    fn region_counts(&self) -> u16 {
        let mut counts = 0;
        let mut seen = HashSet::new();

        for pos in &self.0 {
            if seen.contains(pos) {
                continue;
            }
            counts += 1;
            seen.extend(self.tile_region(pos));
        }
        counts
    }
}

impl From<&str> for Tiles {
    fn from(raw: &str) -> Self {
        let tie_knot = TieKnot::new().with_rope(0..=255);
        let input = raw.trim();
        let hashes = (0..128)
            .map(|row| {
                tie_knot
                    .clone()
                    .with_lengths(format!("{input}-{row}").bytes())
                    .knot_hash()
            })
            .collect::<Vec<_>>();

        let grid = hashes
            .iter()
            .map(|hash| {
                format!("{:032x}", hash)
                    .chars()
                    .map(|c| format!("{:04b}", c.to_digit(16).unwrap()))
                    .collect()
            })
            .collect::<Vec<String>>();

        let mut tiles = HashSet::new();
        for (y, row) in grid.iter().enumerate() {
            for (x, tile) in row.chars().enumerate() {
                if tile == '0' {
                    continue;
                }
                tiles.insert(IVec2::new(x as i32, y as i32));
            }
        }
        Self(tiles)
    }
}

struct Day14;

impl Day for Day14 {
    type Parsed = Tiles;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.0.len()
    }

    fn part2(input: &Self::Parsed) -> u16 {
        input.region_counts()
    }
}

aoc_main!(Day14);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "flqrgnkx";

    #[test]
    fn part1() {
        let parsed = Day14::parse(INPUT);
        assert_eq!(Day14::part1(&parsed), 8108);
    }

    #[test]
    fn part2() {
        let parsed = Day14::parse(INPUT);
        assert_eq!(Day14::part2(&parsed), 1242);
    }
}
