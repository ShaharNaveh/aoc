#[derive(Clone, Debug, Default)]
pub struct TieKnot {
    pub rope: Vec<u8>,
    pub lengths: Vec<u8>,
    pub current: usize,
    pub skip: usize,
}

impl TieKnot {
    const SALT: [u8; 5] = [17, 31, 73, 47, 23];
    const ROUNDS: u8 = 64;

    pub fn new() -> Self {
        Self {
            ..Default::default()
        }
    }

    pub fn knot_hash(mut self) -> u128 {
        self.lengths.extend(&Self::SALT);
        (0..Self::ROUNDS).for_each(|_| {
            self = self.clone().knot_tie();
        });

        let mut res = 0;
        self.rope.chunks(16).for_each(|chunk| {
            res <<= 8;
            res |= chunk.iter().fold(0, |acc, &x| acc ^ (x as u8)) as u128;
        });

        res
    }

    fn knot_tie(mut self) -> Self {
        let len = self.len();

        self.lengths
            .iter()
            .map(|&length| length as usize)
            .for_each(|length| {
                (0..length / 2).for_each(|i| {
                    self.rope.swap(
                        (self.current + i) % len,
                        (self.current + length - i - 1) % len,
                    )
                });
                self.current += length + self.skip;
                self.skip += 1;
            });

        self
    }

    pub fn with_rope<I>(mut self, iter: I) -> Self
    where
        I: IntoIterator<Item = u8>,
    {
        self.rope = iter.into_iter().collect();
        self
    }

    pub fn with_lengths<I>(mut self, iter: I) -> Self
    where
        I: IntoIterator<Item = u8>,
    {
        self.lengths = iter.into_iter().collect();
        self
    }

    fn len(&self) -> usize {
        self.rope.len()
    }
}

fn parse_puzzle(input: &str) -> Vec<u8> {
    input
        .trim()
        .split(',')
        .filter_map(|x| x.parse().ok())
        .collect()
}

fn p1(input: &str) -> u16 {
    let lengths = parse_puzzle(input);
    let knot_tie = TieKnot::new()
        .with_rope(0..=255)
        .with_lengths(lengths)
        .knot_tie();
    knot_tie.rope[0..=1].iter().map(|&x| x as u16).product()
}

fn p2(input: &str) -> String {
    format!(
        "{:032x}",
        TieKnot::new()
            .with_rope(0..=255)
            .with_lengths(input.trim().bytes())
            .knot_hash()
    )
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
