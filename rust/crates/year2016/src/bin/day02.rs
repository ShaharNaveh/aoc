use std::{collections::HashMap, ops::Deref};

use util::{Day, IVec2, aoc_main};

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

fn solve(input: &str, keypad: &Keypad) -> String {
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

struct Day02;

impl Day for Day02 {
    type Parsed = String;

    fn parse(input: &str) -> Self::Parsed {
        input.to_string()
    }

    fn part1(input: &Self::Parsed) -> String {
        let keymap = "
    1 2 3
    4 5 6
    7 8 9"
            .into();

        solve(input, &keymap)
    }

    fn part2(input: &Self::Parsed) -> String {
        let keymap = "
        1
      2 3 4
    5 6 7 8 9
      A B C
        D"
        .into();

        solve(input, &keymap)
    }
}

aoc_main!(Day02);

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
    fn part1() {
        let parsed = Day02::parse(INST);
        assert_eq!(Day02::part1(&parsed), "1985");
    }

    #[test]
    fn part2() {
        let parsed = Day02::parse(INST);
        assert_eq!(Day02::part2(&parsed), "5DB3");
    }
}
