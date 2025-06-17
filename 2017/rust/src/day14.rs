use crate::{day10::TieKnot, utils::IVec2};
use std::collections::HashSet;

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

fn p1(input: &str) -> usize {
    Tiles::from(input).0.len()
}

fn p2(input: &str) -> u16 {
    Tiles::from(input).region_counts()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "flqrgnkx";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 8108);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 1242);
    }
}
