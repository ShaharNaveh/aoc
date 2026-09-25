use std::{
    collections::VecDeque,
    ops::{Deref, DerefMut},
};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
enum Direction {
    Left,
    Right,
}

impl From<&str> for Direction {
    fn from(value: &str) -> Self {
        match value {
            "left" => Self::Left,
            "right" => Self::Right,
            other => unreachable!("unknown direction: '{other}'"),
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Instruction {
    SwapPosition { x: usize, y: usize },
    SwapLetter { x: char, y: char },
    RotatePosition { letter: char, direction: Direction },
    RotateSteps { steps: usize, direction: Direction },
    Reverse { from: usize, to: usize },
    Move { x: usize, y: usize },
}

impl From<&str> for Instruction {
    fn from(value: &str) -> Self {
        let (name, body) = value.trim().split_once(' ').unwrap();
        let parts = body.split_ascii_whitespace().collect::<Vec<_>>();

        match name {
            "swap" => match parts[0] {
                "position" => Self::SwapPosition {
                    x: parts[1].parse().unwrap(),
                    y: parts.last().unwrap().parse().unwrap(),
                },
                "letter" => Self::SwapLetter {
                    x: parts[1].chars().next().unwrap(),
                    y: parts.last().unwrap().chars().next().unwrap(),
                },
                other => unreachable!("unknown swap: '{other}'"),
            },

            "rotate" => match parts[0] {
                "based" => Self::RotatePosition {
                    letter: parts.last().unwrap().chars().next().unwrap(),
                    direction: Direction::Right,
                },
                direction @ ("left" | "right") => Self::RotateSteps {
                    steps: parts[1].parse().unwrap(),
                    direction: direction.into(),
                },
                other => unreachable!("unknown rotation: '{other}'"),
            },

            "reverse" => Self::Reverse {
                from: parts[1].parse().unwrap(),
                to: parts.last().unwrap().parse().unwrap(),
            },

            "move" => Self::Move {
                x: parts[1].parse().unwrap(),
                y: parts.last().unwrap().parse().unwrap(),
            },

            other => unreachable!("unknown instruction: '{other}'"),
        }
    }
}

#[derive(Debug)]
struct Instructions(Box<[Instruction]>);

impl From<&str> for Instructions {
    fn from(value: &str) -> Self {
        value.trim().lines().map(Into::into).collect()
    }
}

impl FromIterator<Instruction> for Instructions {
    fn from_iter<I: IntoIterator<Item = Instruction>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}

impl Deref for Instructions {
    type Target = [Instruction];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Instructions {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct Password(VecDeque<char>);

impl Password {
    fn index_of(&self, letter: char) -> usize {
        self.iter()
            .enumerate()
            .find_map(|(idx, c)| (letter == *c).then_some(idx))
            .unwrap()
    }

    fn execute(&mut self, instruction: Instruction) {
        let instruction = match instruction {
            Instruction::SwapLetter { x, y } => Instruction::SwapPosition {
                x: self.index_of(x),
                y: self.index_of(y),
            },
            Instruction::RotatePosition { letter, direction } => {
                let idx = self.index_of(letter);
                let additional = usize::from(idx >= 4);

                Instruction::RotateSteps {
                    steps: (idx + additional + 1) % self.len(),
                    direction,
                }
            }

            _ => instruction,
        };

        match instruction {
            Instruction::SwapPosition { x, y } => self.swap(x, y),
            Instruction::RotateSteps { steps, direction } => match direction {
                Direction::Left => self.rotate_left(steps),
                Direction::Right => self.rotate_right(steps),
            },
            Instruction::Move { x, y } => {
                let val = self.remove(x).unwrap();
                self.insert(y, val);
            }
            Instruction::Reverse { from, to } => self.make_contiguous()[from..=to].reverse(),
            Instruction::SwapLetter { .. } | Instruction::RotatePosition { .. } => unreachable!(),
        }
    }

    fn run(&mut self, instructions: &Instructions) {
        for &instruction in instructions.iter() {
            self.execute(instruction);
        }
    }
}

impl Deref for Password {
    type Target = VecDeque<char>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Password {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Password {
    fn from(value: &str) -> Self {
        Self(value.trim().chars().collect())
    }
}

impl From<Password> for String {
    fn from(value: Password) -> Self {
        value.iter().collect()
    }
}

struct PasswordPermutations {
    password: Password,
    counter: Vec<usize>,
    idx: usize,
}

impl From<Password> for PasswordPermutations {
    fn from(value: Password) -> Self {
        let len = value.len();
        Self {
            password: value,
            counter: vec![0; len],
            idx: 0,
        }
    }
}

impl Iterator for PasswordPermutations {
    type Item = Password;

    fn next(&mut self) -> Option<Self::Item> {
        let len = self.password.len();

        loop {
            if self.idx >= len {
                return None;
            }

            if self.counter[self.idx] < self.idx {
                if self.idx % 2 == 0 {
                    self.password.swap(0, self.idx);
                } else {
                    self.password.swap(self.counter[self.idx], self.idx);
                }

                self.counter[self.idx] += 1;
                self.idx = 0;
                return Some(self.password.clone());
            } else {
                self.counter[self.idx] = 0;
                self.idx += 1;
            }
        }
    }
}

fn p1(input: &str) -> String {
    let mut password = Password::from("abcdefgh");
    password.run(&input.into());

    password.into()
}

fn p2(input: &str) -> String {
    let scrambled = Password::from("fbgdceah");
    let instructions = Instructions::from(input);

    for mut npassword in PasswordPermutations::from(scrambled.clone()) {
        let res = npassword.clone();
        npassword.run(&instructions);
        if scrambled == npassword {
            return res.into();
        }
    }

    panic!("could not find password");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let mut password = Password::from("abcde");

        for (instruction, expected) in [
            ("swap position 4 with position 0", "ebcda"),
            ("swap letter d with letter b", "edcba"),
            ("reverse positions 0 through 4", "abcde"),
            ("rotate left 1 step", "bcdea"),
            ("move position 1 to position 4", "bdeac"),
            ("move position 3 to position 0", "abdec"),
            ("rotate based on position of letter b", "ecabd"),
            ("rotate based on position of letter d", "decab"),
        ] {
            password.execute(instruction.into());
            assert_eq!(String::from(password), expected, "{instruction}");
        }
    }
}
