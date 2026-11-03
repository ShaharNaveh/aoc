use core::str;
use std::{collections::HashSet, ops::Deref};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
struct Password<'a>(&'a str);

impl<'a> Deref for Password<'a> {
    type Target = &'a str;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<'a> Password<'a> {
    unsafe fn new_unchecked(value: &'a str) -> Self {
        Self(value)
    }
}

impl<'a> TryFrom<&'a [u8]> for Password<'a> {
    type Error = ();

    fn try_from(value: &'a [u8]) -> Result<Self, Self::Error> {
        if value.iter().any(|c| matches!(c, b'i' | b'l' | b'o')) {
            return Err(());
        }

        if value
            .windows(2)
            .filter_map(|w| {
                let [a, b] = w else { unreachable!() };
                (a == b).then_some(a)
            })
            .collect::<HashSet<_>>()
            .len()
            < 2
        {
            return Err(());
        }

        if !value.windows(3).any(|w| {
            let [a, b, c] = w else { unreachable!() };
            matches!(c.checked_sub(*b), Some(1)) && matches!(b.checked_sub(*a), Some(1))
        }) {
            return Err(());
        }

        Ok(Self(str::from_utf8(value).unwrap()))
    }
}

#[derive(Clone, Debug)]
struct PasswordIter<'a> {
    base: Password<'a>,
}

impl<'a> PasswordIter<'a> {
    const fn new(base: Password<'a>) -> Self {
        Self { base }
    }
}

impl<'a> Iterator for PasswordIter<'a> {
    type Item = Password<'a>;

    fn next(&mut self) -> Option<Self::Item> {
        let mut bytes = self.base.as_bytes().to_vec();

        loop {
            for byte in bytes.iter_mut().rev() {
                if *byte == b'z' {
                    *byte = b'a'
                } else {
                    *byte += 1;
                    break;
                }
            }

            if Password::try_from(bytes.as_slice()).is_ok() {
                break;
            }
        }

        // SAFETY:
        // String contains only valid UTF8 and is a valid password.
        self.base = unsafe { Password::new_unchecked(str::from_utf8_unchecked(bytes.leak())) };
        Some(self.base)
    }
}

struct Day11;

impl Day for Day11 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> &str {
        *PasswordIter::new(unsafe { Password::new_unchecked(input) })
            .next()
            .unwrap()
    }

    fn part2(input: &Self::Parsed) -> &str {
        *PasswordIter::new(unsafe { Password::new_unchecked(input) })
            .nth(1)
            .unwrap()
    }
}

aoc_main!(Day11);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [("abcdefgh", "abcdffaa"), ("ghijklmn", "ghjaabcc")] {
            assert_eq!(Day11::part1(&input.into()), expected, "{input}");
        }
    }
}
