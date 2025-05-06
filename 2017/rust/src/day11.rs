use crate::utils::{HexOffset, IVec2};

fn parse_puzzle(input: &str) -> (IVec2, u32) {
    input
        .trim()
        .split(',')
        .fold((IVec2::ZERO, 0), |(pos, max), dir| {
            let npos = pos + HexOffset::from(dir);
            (npos, max.max(npos.hex_manhattan_distance()))
        })
}

fn p1(input: &str) -> u32 {
    parse_puzzle(input).0.hex_manhattan_distance()
}

fn p2(input: &str) -> u32 {
    parse_puzzle(input).1
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
        for (input, expected) in [
            ("ne,ne,ne", 3),
            ("ne,ne,sw,sw", 0),
            ("ne,ne,s,s", 2),
            ("se,sw,se,sw,sw", 3),
        ] {
            assert_eq!(p1(input), expected, "{}", input);
        }
    }
}
