use std::ops::{Deref, RangeInclusive};

#[derive(Clone, Debug)]
struct ProductRange(RangeInclusive<usize>);

impl From<&str> for ProductRange {
    fn from(value: &str) -> Self {
        let (start_s, end_s) = value.split_once('-').unwrap();
        let start = start_s.parse().unwrap();
        let end = end_s.parse().unwrap();
        let range = start..=end;
        Self(range)
    }
}

#[derive(Debug)]
struct ProductRanges(Box<[ProductRange]>);

impl From<&str> for ProductRanges {
    fn from(value: &str) -> Self {
        Self(value.trim().split(',').map(ProductRange::from).collect())
    }
}

impl Deref for ProductRanges {
    type Target = [ProductRange];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl ProductRanges {
    #[must_use]
    fn iter_ids(&self) -> impl Iterator<Item = usize> {
        self.iter().flat_map(|it| it.0.clone())
    }

    #[must_use]
    fn silly_pattern_ids(&self) -> impl Iterator<Item = usize> {
        self.iter_ids().filter(|&id| is_silly_pattern(id))
    }

    #[must_use]
    fn repeated_pattern_ids(&self) -> impl Iterator<Item = usize> {
        self.iter_ids().filter(|&id| is_repeated_pattern(id))
    }
}

#[must_use]
fn is_silly_pattern(id: usize) -> bool {
    let s = id.to_string();

    let len = s.len();
    if len % 2 != 0 {
        return false;
    }

    let mid = len / 2;
    let (a, b) = s.split_at(mid);
    a == b
}

#[must_use]
fn is_repeated_pattern(id: usize) -> bool {
    let s = id.to_string();
    let bytes = s.as_bytes();
    for size in 1..=(bytes.len() / 2) {
        let mut chunks = bytes.chunks_exact(size);
        if !chunks.remainder().is_empty() {
            continue;
        }

        let pattern = chunks.next().unwrap();

        if chunks.all(|chunk| chunk == pattern) {
            return true;
        }
    }
    false
}

fn p1(input: &str) -> usize {
    ProductRanges::from(input).silly_pattern_ids().sum()
}

fn p2(input: &str) -> usize {
    ProductRanges::from(input).repeated_pattern_ids().sum()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
";

    fn get_input() -> String {
        let mut s = INPUT.to_owned();
        s.retain(|c| !c.is_ascii_whitespace());
        s
    }

    #[test]
    fn p1e1() {
        assert_eq!(p1(&get_input()), 1227775554);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(&get_input()), 4174379265);
    }

    #[test]
    fn repeated_pattern() {
        assert!(is_repeated_pattern(12341234));
        assert!(is_repeated_pattern(123123123));
        assert!(is_repeated_pattern(1111111));
        assert!(is_repeated_pattern(1212121212));
        assert!(is_repeated_pattern(565656));
        assert!(is_repeated_pattern(824824824));
        assert!(is_repeated_pattern(2121212121));
        assert!(!is_repeated_pattern(101));

        let pr = ProductRanges::from("2121212118-2121212124");
        assert_eq!(
            pr.repeated_pattern_ids().collect::<Vec<_>>(),
            vec![2121212121]
        );
    }
}
