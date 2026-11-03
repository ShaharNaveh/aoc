use std::{
    fmt,
    num::NonZeroU8,
    ops::{Deref, DerefMut},
};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Hash, Eq, PartialEq)]
struct Group {
    chr: u8,
    len: NonZeroU8,
}

impl Group {
    const fn new(chr: u8, len: NonZeroU8) -> Self {
        Self { chr, len }
    }

    fn with_len(mut self, len: NonZeroU8) -> Self {
        self.len = len;
        self
    }
}

impl fmt::Display for Group {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.chr.to_string().repeat(self.len.get().into()))
    }
}

#[derive(Clone, Debug)]
struct Groups(Vec<Group>);

impl Groups {
    fn with_capacity(capacity: usize) -> Self {
        Self(Vec::with_capacity(capacity))
    }
}

impl Deref for Groups {
    type Target = Vec<Group>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Groups {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Groups {
    fn from(value: &str) -> Self {
        let mut res = vec![];
        let mut chars = value.trim().chars().collect::<Vec<_>>();

        while !chars.is_empty() {
            let mut len = 1;
            let mut iter = chars.windows(2);

            while let Some([l, r]) = iter.next() {
                if l == r { len += 1 } else { break }
            }

            let (head, tail) = chars.split_at(len);
            res.push(Group::new(
                head[0].to_digit(10).unwrap().try_into().unwrap(),
                u8::try_from(head.len()).unwrap().try_into().unwrap(),
            ));
            chars = tail.into();
        }

        Self(res.into())
    }
}

#[derive(Clone, Debug)]
struct LookAndSay {
    cur: Groups,
}

impl LookAndSay {
    fn len(&self) -> usize {
        self.cur
            .iter()
            .map(|group| group.len.get())
            .map(usize::from)
            .sum()
    }
}

impl fmt::Display for LookAndSay {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{}",
            self.cur
                .iter()
                .map(|group| group.to_string())
                .collect::<String>()
        )
    }
}

impl From<&str> for LookAndSay {
    fn from(value: &str) -> Self {
        Self { cur: value.into() }
    }
}

impl Iterator for LookAndSay {
    type Item = Self;

    fn next(&mut self) -> Option<Self::Item> {
        let mut groups = Groups::with_capacity(self.cur.len() + 1);

        for group in self.cur.iter() {
            for ngroup in [
                Group::new(group.len.get(), NonZeroU8::MIN),
                group.with_len(NonZeroU8::MIN),
            ] {
                if let Some(last) = groups.last_mut()
                    && last.chr == ngroup.chr
                {
                    (*last).len = (last.len.get() + ngroup.len.get()).try_into().unwrap();
                } else {
                    groups.push(ngroup);
                };
            }
        }

        self.cur = groups;
        Some(self.clone())
    }
}

struct Day10;

impl Day for Day10 {
    type Parsed = LookAndSay;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().into_iter().nth(40 - 1).unwrap().len()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.clone().into_iter().nth(50 - 1).unwrap().len()
    }
}

aoc_main!(Day10);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [
            ("1", "11"),
            ("11", "21"),
            ("21", "1211"),
            ("1211", "111221"),
            ("111221", "312211"),
        ] {
            let mut game = LookAndSay::from(input);
            let res = game.next().unwrap();

            assert_eq!(res.to_string(), expected, "{input}");
        }
    }
}
