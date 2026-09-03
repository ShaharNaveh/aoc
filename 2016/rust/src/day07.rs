use core::ops::{Deref, Not};
use std::{borrow::Cow, collections::HashSet};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

impl Not for Aba {
    type Output = Self;

    fn not(self) -> Self::Output {
        Self {
            a: self.b,
            b: self.a,
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Aba {
    a: char,
    b: char,
}

impl From<Aba> for String {
    fn from(value: Aba) -> Self {
        format!("{a}{b}{a}", a = value.a, b = value.b)
    }
}

impl TryFrom<[char; 3]> for Aba {
    type Error = ();

    fn try_from(value: [char; 3]) -> Result<Self, Self::Error> {
        let [a, b, c] = value;

        (a == c && a != b).ok_or(()).map(|()| Self { a, b })
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct RawSegment<'a>(Cow<'a, str>);

impl RawSegment<'_> {
    fn has_abba(&self) -> bool {
        self.chars().collect::<Vec<_>>().windows(4).any(|w| {
            let [a, b, c, d] = w else { unreachable!() };
            (a == d) && (b == c) && (a != b)
        })
    }

    fn iter_abas(&self) -> impl Iterator<Item = Aba> + '_ {
        self.chars()
            .collect::<Vec<_>>()
            .windows(3)
            .filter_map(|w| {
                <[char; 3]>::try_from(w)
                    .ok()
                    .and_then(|arr| Aba::try_from(arr).ok())
            })
            .collect::<Vec<_>>()
            .into_iter()
    }
}

impl<'a> Deref for RawSegment<'a> {
    type Target = Cow<'a, str>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<Aba> for RawSegment<'_> {
    fn from(value: Aba) -> Self {
        String::from(value).into()
    }
}

impl From<String> for RawSegment<'_> {
    fn from(value: String) -> Self {
        Self(value.into())
    }
}

impl<'a> From<&'a str> for RawSegment<'a> {
    fn from(value: &'a str) -> Self {
        Self(value.into())
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
enum Segment<'a> {
    Super(RawSegment<'a>),
    Hyper(RawSegment<'a>),
}

#[derive(Debug)]
struct Segments<'a>(HashSet<Segment<'a>>);

impl<'a> From<&'a str> for Segments<'a> {
    fn from(value: &'a str) -> Self {
        let mut segments = HashSet::new();

        for raw in value.trim().split('[') {
            if let Some((v, supr)) = raw.rsplit_once(']') {
                segments.insert(Segment::Hyper(v.into()));
                segments.insert(Segment::Super(supr.into()));
            } else {
                segments.insert(Segment::Super(raw.into()));
            }
        }

        Self(segments)
    }
}

impl<'a> Deref for Segments<'a> {
    type Target = HashSet<Segment<'a>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct Ipv7Addr<'a>(Segments<'a>);

impl Ipv7Addr<'_> {
    fn supports_tls(&self) -> bool {
        let mut seen = false;

        for segment in self.iter() {
            match segment {
                Segment::Super(v) if !seen => seen = v.has_abba(),
                Segment::Super(_) => {}
                Segment::Hyper(v) => {
                    if v.has_abba() {
                        return false;
                    }
                }
            };
        }

        seen
    }

    fn supports_ssl(&self) -> bool {
        let mut super_abas = HashSet::new();
        let mut hyper_abas = HashSet::new();
        for segment in self.iter() {
            match segment {
                Segment::Super(v) => super_abas.extend(v.iter_abas()),
                Segment::Hyper(v) => hyper_abas.extend(v.iter_abas().map(Not::not)),
            }
        }

        super_abas.intersection(&hyper_abas).next().is_some()
    }
}

impl<'a> Deref for Ipv7Addr<'a> {
    type Target = Segments<'a>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<'a> From<&'a str> for Ipv7Addr<'a> {
    fn from(value: &'a str) -> Self {
        Self(value.into())
    }
}

fn p1(input: &str) -> usize {
    input
        .trim()
        .lines()
        .map(Ipv7Addr::from)
        .filter(|ip| ip.supports_tls())
        .count()
}

fn p2(input: &str) -> usize {
    input
        .trim()
        .lines()
        .map(Ipv7Addr::from)
        .filter(|ip| ip.supports_ssl())
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert!(Ipv7Addr::from("abba[mnop]qrst").supports_tls());
    }

    #[test]
    fn p1e2() {
        assert!(!Ipv7Addr::from("abcd[bddb]xyyx").supports_tls());
    }

    #[test]
    fn p1e3() {
        assert!(!Ipv7Addr::from("aaaa[qwer]tyui").supports_tls());
    }

    #[test]
    fn p1e4() {
        assert!(Ipv7Addr::from("ioxxoj[asdfgh]zxcvbn").supports_tls());
    }

    #[test]
    fn p2e1() {
        assert!(Ipv7Addr::from("aba[bab]xyz").supports_ssl());
    }

    #[test]
    fn p2e2() {
        assert!(!Ipv7Addr::from("xyx[xyx]xyx").supports_ssl());
    }

    #[test]
    fn p2e3() {
        assert!(Ipv7Addr::from("aaa[kek]eke").supports_ssl());
    }

    #[test]
    fn p2e4() {
        assert!(Ipv7Addr::from("zazbz[bzb]cdb").supports_ssl());
    }
}
