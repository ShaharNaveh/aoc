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

    pub fn knot_tie(mut self) -> Self {
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
