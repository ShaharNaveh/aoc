use std::ops::Add;

use util::{Day, IVec2, aoc_main};

/// This hex offset is for hex layout that looks like:
///     2
/// 7       3
///     1
/// 6       4
///     5
///
/// Which we actually implement as:
///
/// 72
/// 613
///  54
///
/// ---
///
/// While a `HorizontalHexOffset` that its layout is like:
///   2   3
///
/// 7   1   4
///
///   6   5
///     
/// We would implement as:
///
/// 23
/// 714
///  65
#[derive(Clone, Copy, Debug)]
enum VerticalHexOffset {
    North,
    NorthEast,
    NorthWest,
    South,
    SouthEast,
    SouthWest,
}

impl From<&str> for VerticalHexOffset {
    #[inline]
    fn from(raw: &str) -> Self {
        match raw {
            "n" => Self::North,
            "ne" => Self::NorthEast,
            "nw" => Self::NorthWest,
            "s" => Self::South,
            "se" => Self::SouthEast,
            "sw" => Self::SouthWest,
            _ => unreachable!(),
        }
    }
}

impl Add<VerticalHexOffset> for IVec2 {
    type Output = Self;

    #[inline]
    fn add(self, rhs: VerticalHexOffset) -> Self {
        self + IVec2::from(rhs)
    }
}

impl From<VerticalHexOffset> for IVec2 {
    #[inline]
    fn from(offset: VerticalHexOffset) -> Self {
        match offset {
            VerticalHexOffset::North => IVec2::Y,
            VerticalHexOffset::NorthEast => IVec2::X,
            VerticalHexOffset::NorthWest => IVec2::NEG_XY,
            VerticalHexOffset::South => IVec2::NEG_Y,
            VerticalHexOffset::SouthEast => IVec2::X_NEG_Y,
            VerticalHexOffset::SouthWest => IVec2::NEG_X,
        }
    }
}

fn hex_manhattan_distance(pos: IVec2) -> u32 {
    ((pos.abs().element_sum() + pos.element_sum().abs()) / 2) as u32
}

fn parse_puzzle(input: &str) -> (IVec2, u32) {
    input
        .trim()
        .split(',')
        .fold((IVec2::ZERO, 0), |(pos, max), dir| {
            let npos = pos + VerticalHexOffset::from(dir);
            (npos, max.max(hex_manhattan_distance(npos)))
        })
}

struct Day11;

impl Day for Day11 {
    type Parsed = (IVec2, u32);

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> u32 {
        hex_manhattan_distance(input.0)
    }

    fn part2(input: &Self::Parsed) -> u32 {
        input.1
    }
}

aoc_main!(Day11);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        for (input, expected) in [
            ("ne,ne,ne", 3),
            ("ne,ne,sw,sw", 0),
            ("ne,ne,s,s", 2),
            ("se,sw,se,sw,sw", 3),
        ] {
            assert_eq!(Day11::part1(&Day11::parse(input)), expected, "{}", input);
        }
    }
}
