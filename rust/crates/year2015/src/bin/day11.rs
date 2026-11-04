use std::{
    collections::HashSet,
    fmt,
    ops::{Deref, DerefMut},
};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
struct PasswordInner {
    bytes: [u8; 8],
}

impl Deref for PasswordInner {
    type Target = [u8; 8];

    fn deref(&self) -> &Self::Target {
        &self.bytes
    }
}

impl DerefMut for PasswordInner {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.bytes
    }
}

#[derive(Clone, Copy, Debug)]
struct Password(PasswordInner);

impl Password {
    unsafe fn new_unchecked(bytes: [u8; 8]) -> Self {
        Self(PasswordInner { bytes })
    }
}

impl TryFrom<&PasswordInner> for Password {
    type Error = ();

    fn try_from(value: &PasswordInner) -> Result<Self, Self::Error> {
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

        Ok(Self(*value))
    }
}

impl fmt::Display for Password {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str(str::from_utf8(&*self.0).unwrap())
    }
}

#[derive(Clone, Debug)]
struct PasswordIter {
    base: PasswordInner,
}

impl PasswordIter {
    const fn new(base: Password) -> Self {
        Self { base: base.0 }
    }
}

impl Iterator for PasswordIter {
    type Item = Password;

    fn next(&mut self) -> Option<Self::Item> {
        let mut bytes = self.base;

        loop {
            for byte in bytes.iter_mut().rev() {
                if *byte == b'z' {
                    *byte = b'a'
                } else {
                    *byte += 1;
                    break;
                }
            }

            if let Ok(password) = Password::try_from(&bytes) {
                self.base = bytes;
                return Some(password);
            };
        }
    }
}

struct Day11;

impl Day for Day11 {
    type Parsed = Password;

    fn parse(input: &str) -> Self::Parsed {
        // SAFETY: input should always be with length of 8
        unsafe { Password::new_unchecked(input.as_bytes().try_into().unwrap()) }
    }

    fn part1(input: &Self::Parsed) -> String {
        PasswordIter::new(*input).next().unwrap().to_string()
    }

    fn part2(input: &Self::Parsed) -> String {
        PasswordIter::new(*input).nth(1).unwrap().to_string()
    }
}

aoc_main!(Day11);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [("abcdefgh", "abcdffaa"), ("ghijklmn", "ghjaabcc")] {
            assert_eq!(Day11::part1(&Day11::parse(input)), expected, "{input}");
        }
    }
}
