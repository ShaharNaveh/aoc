use util::{Day, aoc_main};

#[derive(Clone, Debug)]
struct Dance {
    programs: Vec<char>,
    dance: Vec<DanceMove>,
}

impl Dance {
    #[must_use]
    #[inline]
    fn prog_position(&self, program: char) -> usize {
        self.programs.iter().position(|&c| c == program).unwrap()
    }

    #[must_use]
    fn at(&self, nth: usize) -> String {
        let initial = self.programs.clone();
        let mut seen = vec![initial.clone()];
        for (i, programs) in self.clone().enumerate() {
            if i == nth {
                return programs.into_iter().collect();
            }
            if programs == initial {
                return seen[nth % (i + 1)].clone().into_iter().collect();
            }

            seen.push(programs.clone())
        }
        unreachable!()
    }
}

#[derive(Clone, Copy, Debug)]
enum DanceMove {
    Spin(u8),
    Exchange(u8, u8),
    Partner(char, char),
}

impl From<&str> for Dance {
    fn from(raw: &str) -> Self {
        let dance = raw.trim().split(',').map(Into::into).collect();
        Self {
            dance,
            ..Default::default()
        }
    }
}

impl From<&str> for DanceMove {
    fn from(raw: &str) -> Self {
        let mut it = raw.trim().chars();
        let id = it.next().unwrap();
        let data = it.as_str();
        match id {
            's' => Self::Spin(data.parse().unwrap()),
            'x' => {
                let (a, b) = data.split_once('/').unwrap();
                Self::Exchange(a.parse().unwrap(), b.parse().unwrap())
            }
            'p' => {
                let (a, b) = data.split_once('/').unwrap();
                Self::Partner(a.chars().next().unwrap(), b.chars().next().unwrap())
            }
            _ => unreachable!(),
        }
    }
}

impl Iterator for Dance {
    type Item = Vec<char>;

    fn next(&mut self) -> Option<Self::Item> {
        for &dance_move in &self.dance {
            match dance_move {
                DanceMove::Spin(n) => self.programs.rotate_right(n.into()),
                DanceMove::Exchange(a, b) => self.programs.swap(a.into(), b.into()),
                DanceMove::Partner(a, b) => {
                    let tmp = self.clone();

                    self.programs
                        .swap(tmp.prog_position(a), tmp.prog_position(b))
                }
            }
        }
        Some(self.programs.clone())
    }
}

impl Default for Dance {
    fn default() -> Self {
        Self {
            programs: ('a'..='p').collect(),
            dance: vec![],
        }
    }
}

struct Day16;

impl Day for Day16 {
    type Parsed = Dance;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> String {
        input.at(0)
    }

    fn part2(input: &Self::Parsed) -> String {
        input.at(1_000_000_000)
    }
}

aoc_main!(Day16);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "s1,x3/4,pe/b";
    const PROGRAMS: [char; 5] = ['a', 'b', 'c', 'd', 'e'];

    fn base_dance() -> Dance {
        Dance {
            programs: PROGRAMS.into(),
            ..Dance::from(INPUT)
        }
    }

    #[test]
    fn p1e1() {
        assert_eq!(base_dance().at(0), "baedc");
    }

    #[test]
    fn p2e1() {
        assert_eq!(base_dance().at(1), "ceadb");
    }
}
