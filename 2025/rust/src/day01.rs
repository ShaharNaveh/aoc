use std::ops::Deref;

#[derive(Clone, Copy, Debug)]
enum Direction {
    Left,
    Right,
}

impl From<char> for Direction {
    fn from(value: char) -> Self {
        match value {
            'L' => Self::Left,
            'R' => Self::Right,
            _ => panic!("Unknown direction: {value}"),
        }
    }
}

#[derive(Clone, Copy, Debug)]
struct Rotation {
    direction: Direction,
    distance: u16,
}

impl From<&str> for Rotation {
    fn from(value: &str) -> Self {
        let mut it = value.chars();

        let direction = Direction::from(it.next().unwrap());
        let distance = it.collect::<String>().parse().unwrap();
        Self {
            direction,
            distance,
        }
    }
}

impl Rotation {
    /// Returns the wrapped delta (distance % 100).
    #[must_use]
    fn delta(&self) -> i16 {
        let dir = match self.direction {
            Direction::Left => -1,
            Direction::Right => 1,
        };
        i16::try_from(self.distance % 100).unwrap() * dir
    }
}

#[derive(Debug)]
struct Rotations(Box<[Rotation]>);

impl From<&str> for Rotations {
    fn from(value: &str) -> Self {
        Self(value.lines().map(Rotation::from).collect())
    }
}

impl Deref for Rotations {
    type Target = [Rotation];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug)]
struct Dial {
    pos: u8,
    on_zero: u16,
    /// 0x434C49434B is ASCII for "CLICK".
    clicks: u16,
}

impl From<&str> for Dial {
    fn from(value: &str) -> Self {
        let mut dial = Self::default();
        let rotations = Rotations::from(value.trim());
        dial.do_rotations(&rotations);
        dial
    }
}

impl Default for Dial {
    fn default() -> Self {
        Self {
            pos: 50,
            on_zero: 0,
            clicks: 0,
        }
    }
}

impl Dial {
    fn do_rotation(&mut self, rotation: &Rotation) {
        self.clicks += rotation.distance / 100; // Add full rotation count
        let npos = i16::from(self.pos) + rotation.delta();
        let npos_wrapped = npos.rem_euclid(100);

        match rotation.direction {
            Direction::Left => {
                if self.pos != 0 && (npos_wrapped == 0 || npos_wrapped > npos) {
                    self.clicks += 1;
                }
            }
            Direction::Right => {
                if npos_wrapped < npos {
                    self.clicks += 1;
                }
            }
        }

        self.pos = u8::try_from(npos_wrapped).unwrap();
    }

    fn do_rotations(&mut self, rotations: &Rotations) {
        for rotation in rotations.iter() {
            self.do_rotation(rotation);

            if self.pos == 0 {
                self.on_zero += 1;
            }
        }
    }
}

fn p1(input: &str) -> u16 {
    Dial::from(input).on_zero
}

fn p2(input: &str) -> u16 {
    Dial::from(input).clicks
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 3);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 6);
    }
}
