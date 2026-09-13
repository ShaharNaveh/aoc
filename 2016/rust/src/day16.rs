use core::{
    fmt,
    ops::{Deref, DerefMut, Not},
};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Bit {
    Zero,
    One,
}

impl From<Bit> for char {
    fn from(value: Bit) -> Self {
        match value {
            Bit::Zero => '0',
            Bit::One => '1',
        }
    }
}

impl From<char> for Bit {
    fn from(value: char) -> Self {
        match value {
            '0' => Self::Zero,
            '1' => Self::One,
            other => panic!("unknown bit: '{other}'"),
        }
    }
}

impl From<bool> for Bit {
    fn from(value: bool) -> Self {
        if value { Bit::One } else { Bit::Zero }
    }
}

impl fmt::Display for Bit {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&char::from(*self), f)
    }
}

impl Not for Bit {
    type Output = Self;

    fn not(self) -> Self::Output {
        match self {
            Self::Zero => Self::One,
            Self::One => Self::Zero,
        }
    }
}

#[derive(Clone, Debug, Default)]
struct DiskData(Vec<Bit>);

impl FromIterator<Bit> for DiskData {
    fn from_iter<I: IntoIterator<Item = Bit>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}

impl Not for DiskData {
    type Output = Self;

    fn not(self) -> Self::Output {
        Self(self.iter().copied().map(Not::not).collect())
    }
}

impl From<&str> for DiskData {
    fn from(value: &str) -> Self {
        Self(value.chars().map(Into::into).collect())
    }
}

impl Deref for DiskData {
    type Target = Vec<Bit>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for DiskData {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl fmt::Display for DiskData {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = self.iter().copied().map(char::from).collect::<String>();
        fmt::Display::fmt(&s, f)
    }
}

#[derive(Debug)]
struct Checksum(DiskData);

impl From<DiskData> for Checksum {
    fn from(value: DiskData) -> Self {
        Self(value)
    }
}

impl From<Disk> for Checksum {
    fn from(disk: Disk) -> Self {
        let mut out = Self::from(disk.0);

        while out.len() % 2 == 0 {
            out = Self(
                out.iter()
                    .copied()
                    .collect::<Vec<_>>()
                    .chunks_exact(2)
                    .map(|c| (c[0] == c[1]).into())
                    .collect(),
            );
        }

        out
    }
}

impl Deref for Checksum {
    type Target = DiskData;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Checksum {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl fmt::Display for Checksum {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self.0, f)
    }
}

#[derive(Clone, Debug)]
struct Disk(DiskData);

impl From<&str> for Disk {
    fn from(value: &str) -> Self {
        Self(value.into())
    }
}

impl Deref for Disk {
    type Target = DiskData;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Disk {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Not for Disk {
    type Output = Self;

    fn not(self) -> Self::Output {
        Self(!self.0)
    }
}

impl Disk {
    fn fill(&mut self, size: usize) {
        while self.len() <= size {
            let mut b = self.clone();
            b.reverse();
            let b = !b;

            self.push(Bit::Zero);
            self.extend(b.iter())
        }

        self.truncate(size);
    }

    fn solve(&mut self, size: usize) -> String {
        self.fill(size);

        Checksum::from(self.clone()).to_string()
    }
}

fn main(input: &str, size: usize) -> String {
    Disk::from(input.trim()).solve(size)
}

fn p1(input: &str) -> String {
    main(input, 272)
}

fn p2(input: &str) -> String {
    main(input, 35651584)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(main("110010110100", 12), "100");
    }
}
