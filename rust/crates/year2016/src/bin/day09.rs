use core::ops::Deref;

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug)]
struct File<'a>(&'a [u8]);

impl File<'_> {
    fn decompress(&self, recurse: bool) -> usize {
        let mut len = 0;
        let mut idx = 0;

        let nchars = self.len();

        while idx < nchars {
            match self[idx] as char {
                '(' => {
                    let end = self
                        .iter()
                        .skip(idx + 1)
                        .enumerate()
                        .find(|&(_, c)| (*c as char) == ')')
                        .map(|(i, _)| i + idx + 1)
                        .unwrap();

                    let (repeat, count) = str::from_utf8(&self[idx + 1..end])
                        .unwrap()
                        .split_once('x')
                        .map(|(a, b)| (a.parse::<usize>().unwrap(), b.parse::<usize>().unwrap()))
                        .unwrap();

                    idx = end + 1;
                    len += {
                        count
                            * if recurse {
                                Self::from(&self[idx..idx + repeat]).decompress(recurse)
                            } else {
                                repeat
                            }
                    };

                    idx += repeat;
                }
                '\n' => {
                    debug_assert_eq!(idx, nchars - 1);
                    break;
                }
                _ => {
                    idx += 1;
                    len += 1;
                }
            }
        }

        len
    }
}

impl<'a> From<&'a [u8]> for File<'a> {
    fn from(value: &'a [u8]) -> Self {
        Self(value)
    }
}

impl<'a> From<&'a str> for File<'a> {
    fn from(value: &'a str) -> Self {
        Self(value.as_ref())
    }
}

impl<'a> Deref for File<'a> {
    type Target = &'a [u8];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day09;

impl Day for Day09 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.to_string()
    }

    fn part1(input: &Self::Parsed) -> usize {
        File::from(input.as_str()).decompress(false)
    }

    fn part2(input: &Self::Parsed) -> usize {
        File::from(input.as_str()).decompress(true)
    }
}

aoc_main!(Day09);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (input, expected) in [
            ("ADVENT", 6),
            ("A(1x5)BC", 7),
            ("(3x3)XYZ", 9),
            ("A(2x2)BCD(2x2)EFG", 11),
            ("(6x1)(1x3)A", 6),
            ("X(8x2)(3x3)ABCY", 18),
        ] {
            let parsed = Day09::parse(input);
            assert_eq!(Day09::part1(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn part2() {
        for (input, expected) in [
            ("(3x3)XYZ", 9),
            ("X(8x2)(3x3)ABCY", 20),
            ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ] {
            let parsed = Day09::parse(input);
            assert_eq!(Day09::part2(&parsed), expected, "{input}");
        }
    }

    #[test]
    fn p2e4() {
        assert_eq!(
            Day09::part2(&Day09::parse(
                "(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"
            )),
            445
        );
    }
}
