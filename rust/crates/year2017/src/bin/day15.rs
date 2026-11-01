use util::{Day, aoc_main};

#[derive(Copy, Clone, Debug, Default)]
struct Generator {
    prev: u64,
    factor: u64,
}

impl Generator {
    const DIV: u64 = 2147483647;

    fn with_prev(mut self, prev: u64) -> Self {
        self.prev = prev;
        self
    }

    fn with_factor(mut self, factor: u64) -> Self {
        self.factor = factor;
        self
    }
}

impl Iterator for Generator {
    type Item = u64;
    fn next(&mut self) -> Option<Self::Item> {
        self.prev = (self.prev * self.factor) % Self::DIV;
        Some(self.prev)
    }
}

impl From<&str> for Generator {
    fn from(raw: &str) -> Self {
        let prev = raw.split_whitespace().last().unwrap().parse().unwrap();
        Self::default().with_prev(prev)
    }
}

fn parse_puzzle(input: &str) -> (Generator, Generator) {
    let mut it = input.trim().lines().map(Generator::from);
    let gen_a = it.next().unwrap().with_factor(16807);
    let gen_b = it.next().unwrap().with_factor(48271);
    (gen_a, gen_b)
}

struct Day15;

impl Day for Day15 {
    type Parsed = (Generator, Generator);

    fn parse(input: &str) -> Self::Parsed {
        parse_puzzle(input)
    }

    fn part1(input: &Self::Parsed) -> usize {
        let (gen_a, gen_b) = *input;
        gen_a
            .zip(gen_b)
            .take(40_000_000)
            .filter(|(a, b)| (a & 0xFFFF) == (b & 0xFFFF))
            .count()
    }

    fn part2(input: &Self::Parsed) -> usize {
        let (gen_a, gen_b) = *input;
        gen_a
            .filter(|v| v % 4 == 0)
            .zip(gen_b.filter(|v| v % 8 == 0))
            .take(5_000_000)
            .filter(|(a, b)| (a & 0xFFFF) == (b & 0xFFFF))
            .count()
    }
}

aoc_main!(Day15);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
Generator A starts with 65
Generator B starts with 8921
";

    #[test]
    fn part1() {
        let parsed = Day15::parse(INPUT);
        assert_eq!(Day15::part1(&parsed), 588);
    }

    #[test]
    fn part2() {
        let parsed = Day15::parse(INPUT);
        assert_eq!(Day15::part2(&parsed), 309);
    }
}
