use crate::utils::IVec2;

use std::{collections::HashMap, ops::Deref};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Debug)]
struct Keypad(HashMap<IVec2, char>);

impl Keypad {
    fn start_pos(&self) -> IVec2 {
        *self
            .iter()
            .find_map(|(k, v)| if *v == '5' { Some(k) } else { None })
            .unwrap()
    }
}

impl From<&str> for Keypad {
    fn from(value: &str) -> Self {
        let mut keypad = HashMap::new();

        for (y, line) in value.lines().filter(|l| !l.is_empty()).enumerate() {
            for (x, val) in line
                .chars()
                .step_by(2)
                .enumerate()
                .filter(|(_, c)| !c.is_whitespace())
            {
                keypad.insert(
                    IVec2::new(x.try_into().unwrap(), y.try_into().unwrap()),
                    val,
                );
            }
        }

        Self(keypad)
    }
}

impl Deref for Keypad {
    type Target = HashMap<IVec2, char>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct Code(Vec<IVec2>);

impl Deref for Code {
    type Target = Vec<IVec2>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl Code {
    fn walk(&self, start: IVec2, keypad: &Keypad) -> IVec2 {
        let mut pos = start;

        for &offset in self.iter() {
            let npos = pos + offset;

            if !keypad.contains_key(&npos) {
                continue;
            }

            pos = npos;
        }

        pos
    }
}

impl From<&str> for Code {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .chars()
                .map(|c| match c {
                    'U' => IVec2::NEG_Y,
                    'L' => IVec2::NEG_X,
                    'D' => IVec2::Y,
                    'R' => IVec2::X,
                    other => panic!("Unknown direction: '{other}'"),
                })
                .collect(),
        )
    }
}

#[derive(Debug)]
struct Codes(Vec<Code>);

impl From<&str> for Codes {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Deref for Codes {
    type Target = Vec<Code>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn main(input: &str, keypad: &Keypad) -> String {
    let codes = Codes::from(input);
    let mut buf = String::new();

    let mut pos = keypad.start_pos();
    for code in codes.iter() {
        pos = code.walk(pos, &keypad);
        let key = keypad[&pos];

        buf.push(key);
    }

    buf
}

fn p1(input: &str) -> String {
    let keymap = "
1 2 3
4 5 6
7 8 9"
        .into();

    main(input, &keymap)
}

fn p2(input: &str) -> String {
    let keymap = "
    1
  2 3 4
5 6 7 8 9
  A B C
    D"
    .into();

    main(input, &keymap)
}

#[cfg(test)]
mod tests {
    use super::*;

    const INST: &str = "
ULL
RRDDD
LURDL 
UUUUD
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INST), "1985");
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INST), "5DB3");
    }
}
