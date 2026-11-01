use util::{Day, aoc_main};

struct Day17;

impl Day for Day17 {
    type Parsed = usize;

    fn parse(input: &str) -> Self::Parsed {
        input.trim().parse().unwrap()
    }

    fn part1(input: &Self::Parsed) -> usize {
        let step = *input;
        let mut buf = vec![0];
        let mut idx = 0;
        for x in 1..=2017 {
            idx = (idx + step) % x + 1;
            buf.insert(idx, x)
        }
        buf[idx + 1]
    }

    fn part2(input: &Self::Parsed) -> usize {
        let step = *input;
        let mut idx = 0;
        let mut res = 0;
        for x in 1..50_000_000 {
            idx = (idx + step) % x + 1;
            if idx == 1 {
                res = x;
            }
        }
        res
    }
}

aoc_main!(Day17);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        let parsed = Day17::parse("3");
        assert_eq!(Day17::part1(&parsed), 638);
    }
}
