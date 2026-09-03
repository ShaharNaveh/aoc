use core::ops::Deref;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

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

fn p1(input: &str) -> usize {
    File::from(input).decompress(false)
}

fn p2(input: &str) -> usize {
    File::from(input).decompress(true)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(p1("ADVENT"), 6);
    }

    #[test]
    fn p1e2() {
        assert_eq!(p1("A(1x5)BC"), 7);
    }

    #[test]
    fn p1e3() {
        assert_eq!(p1("(3x3)XYZ"), 9);
    }

    #[test]
    fn p1e4() {
        assert_eq!(p1("A(2x2)BCD(2x2)EFG"), 11);
    }

    #[test]
    fn p1e5() {
        assert_eq!(p1("(6x1)(1x3)A"), 6);
    }

    #[test]
    fn p1e6() {
        assert_eq!(p1("X(8x2)(3x3)ABCY"), 18);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2("(3x3)XYZ"), 9);
    }

    #[test]
    fn p2e2() {
        assert_eq!(p2("X(8x2)(3x3)ABCY"), 20);
    }

    #[test]
    fn p2e3() {
        assert_eq!(p2("(27x12)(20x12)(13x14)(7x10)(1x12)A"), 241920);
    }

    #[test]
    fn p2e4() {
        assert_eq!(
            p2("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"),
            445
        );
    }
}
