use util::{Day, aoc_main};

fn parse_puzzle(input: &str) -> Vec<u8> {
    input
        .trim()
        .chars()
        .map(|c| c.to_digit(10).unwrap() as u8)
        .collect()
}

fn solve<I>(iter: I, offset: usize) -> usize
where
    I: IntoIterator<Item = u8>,
{
    let vec = iter.into_iter().collect::<Vec<_>>();
    let len = vec.len();
    vec.iter()
        .enumerate()
        .filter(|&(i, x)| *x == vec[(i + offset) % len])
        .map(|(_, x)| *x as usize)
        .sum()
}

struct Day01;

impl Day for Day01 {
    type Parsed = Vec<u8>;

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> usize {
        solve(input.clone(), 1)
    }

    fn part2(input: &Self::Parsed) -> usize {
        let nums = input.clone();
        let offset = nums.len() / 2;
        solve(nums, offset)
    }
}

aoc_main!(Day01);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [("1122", 3), ("1111", 4), ("1234", 0), ("912129", 9)] {
            let parsed = Day01::parse(input);
            assert_eq!(Day01::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [
            ("1212", 6),
            ("1221", 0),
            ("123425", 4),
            ("123123", 12),
            ("12131415", 4),
        ] {
            let parsed = Day01::parse(input);
            assert_eq!(Day01::part2(&parsed), expected, "{input}");
        }
    }
}
