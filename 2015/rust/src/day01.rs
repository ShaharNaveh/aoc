use std::ops::Deref;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Debug)]
struct Directions(Box<[i32]>);

impl From<&str> for Directions {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .chars()
                .map(|c| match c {
                    '(' => 1,
                    ')' => -1,
                    other => unreachable!("unknown char: '{other}'"),
                })
                .collect(),
        )
    }
}

impl Deref for Directions {
    type Target = Box<[i32]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

fn p1(input: &str) -> i32 {
    Directions::from(input).iter().sum()
}

fn p2(input: &str) -> usize {
    let mut floor = 0i32;

    for (idx, offset) in Directions::from(input).iter().enumerate() {
        floor += offset;

        if floor.is_negative() {
            return idx + 1;
        }
    }

    panic!("Never got negative floor");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        for (input, expected) in [
            ("(())", 0),
            ("()()", 0),
            ("(((", 3),
            ("(()(()(", 3),
            ("))(((((", 3),
            ("())", -1),
            ("))(", -1),
            (")))", -3),
            (")())())", -3),
        ] {
            assert_eq!(p1(input), expected, "{input}");
        }
    }

    #[test]
    fn p2e1() {
        for (input, expected) in [(")", 1), ("()())", 5)] {
            assert_eq!(p2(input), expected, "{input}");
        }
    }
}
