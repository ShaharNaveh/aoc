use std::ops::Deref;

use util::{Day, aoc_main};

#[derive(Debug)]
struct Strings(Box<[String]>);

impl From<&str> for Strings {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Strings {
    type Target = Box<[String]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Spec {
    chars: usize,
    memory: usize,
}

impl Spec {
    fn part1(value: &str) -> Self {
        let mut escaping = false;
        let mut escaped = 0;
        let mut unicode = 0;

        value.chars().for_each(|c| {
            if escaping {
                if c == 'x' {
                    unicode += 1;
                } else {
                    escaped += 1;
                }

                escaping = false;
            } else if c == '\\' {
                escaping = true;
            }
        });

        let chars = value.len();

        Self {
            chars,
            memory: chars - 2 - escaped - (unicode * 3),
        }
    }

    fn part2(value: &str) -> Self {
        let chars = value.len();

        let escaped = value.chars().filter(|&c| c == '"' || c == '\\').count();

        Self {
            chars,
            memory: escaped + 2 + chars,
        }
    }
}

struct Day08;

impl Day for Day08 {
    type Parsed = Strings;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input
            .iter()
            .map(|s| Spec::part1(s.as_ref()))
            .map(|spec| spec.chars - spec.memory)
            .sum()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input
            .iter()
            .map(|s| Spec::part2(s.as_ref()))
            .map(|spec| spec.memory - spec.chars)
            .sum()
    }
}

aoc_main!(Day08);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [
            (
                r#""""#,
                Spec {
                    chars: 2,
                    memory: 0,
                },
            ),
            (
                r#""abc""#,
                Spec {
                    chars: 5,
                    memory: 3,
                },
            ),
            (
                r#""aaa\"aaa""#,
                Spec {
                    chars: 10,
                    memory: 7,
                },
            ),
            (
                r#""\x27""#,
                Spec {
                    chars: 6,
                    memory: 1,
                },
            ),
        ] {
            assert_eq!(Spec::part1(input), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [
            (
                r#""""#,
                Spec {
                    chars: 6,
                    memory: 0,
                },
            ),
            (
                r#""abc""#,
                Spec {
                    chars: 9,
                    memory: 3,
                },
            ),
            (
                r#""aaa\"aaa""#,
                Spec {
                    chars: 16,
                    memory: 7,
                },
            ),
            (
                r#""\x27""#,
                Spec {
                    chars: 11,
                    memory: 1,
                },
            ),
        ] {
            assert_eq!(Spec::part2(input), expected, "{input}");
        }
    }
}
