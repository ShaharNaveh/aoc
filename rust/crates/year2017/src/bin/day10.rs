use year2017::knot_hash::TieKnot;

use util::{Day, aoc_main};

fn parse_puzzle(input: &str) -> Vec<u8> {
    input
        .trim()
        .split(',')
        .filter_map(|x| x.parse().ok())
        .collect()
}

struct Day10;

impl Day for Day10 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.to_string()
    }

    fn part1(input: &Self::Parsed) -> u16 {
        let lengths = parse_puzzle(input);
        let knot_tie = TieKnot::new()
            .with_rope(0..=255)
            .with_lengths(lengths)
            .knot_tie();
        knot_tie.rope[0..=1].iter().map(|&x| x as u16).product()
    }

    fn part2(input: &Self::Parsed) -> String {
        format!(
            "{:032x}",
            TieKnot::new()
                .with_rope(0..=255)
                .with_lengths(input.trim().bytes())
                .knot_hash()
        )
    }
}

aoc_main!(Day10);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let lengths = parse_puzzle("3,4,1,5");
        let tie_knot = TieKnot::new()
            .with_rope(0..=4)
            .with_lengths(lengths)
            .knot_tie();
        let result = tie_knot.rope[0] * tie_knot.rope[1];
        assert_eq!(result, 12);
    }

    #[test]
    fn p2e1() {
        let tie_knot = TieKnot::new().with_rope(0..=255);
        for (input, expected) in [
            ("", "a2582a3a0e66e6e86e3812dcb672a272"),
            ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
            ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
            ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
        ] {
            let result = format!(
                "{:032x}",
                tie_knot.clone().with_lengths(input.bytes()).knot_hash()
            );
            assert_eq!(result, expected);
        }
    }
}
