use std::{
    collections::HashMap,
    ops::{Deref, DerefMut},
};

use util::{Day, aoc_main, calculate_hash};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Wire(u64);

impl From<&str> for Wire {
    fn from(value: &str) -> Self {
        Self(calculate_hash(&value.trim()))
    }
}

#[derive(Clone, Debug, Default, Eq, PartialEq)]
struct Wires(HashMap<Wire, u16>);

impl Deref for Wires {
    type Target = HashMap<Wire, u16>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Wires {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Copy, Clone, Debug)]
enum Value {
    Constant(u16),
    Wire(Wire),
}

impl From<&str> for Value {
    fn from(value: &str) -> Self {
        value
            .trim()
            .parse()
            .map_or_else(|_| Self::Wire(value.into()), |v| Self::Constant(v))
    }
}

#[derive(Copy, Clone, Debug)]
enum Expr {
    Value(Value),
    And { lhs: Value, rhs: Value },
    Or { lhs: Value, rhs: Value },
    Not(Wire),
    LShift { lhs: Wire, rhs: u16 },
    RShift { lhs: Wire, rhs: u16 },
}

impl From<&str> for Expr {
    fn from(value: &str) -> Self {
        let parts = value.split_ascii_whitespace().collect::<Vec<_>>();

        if value.starts_with("NOT") {
            return Self::Not((*parts.last().unwrap()).into());
        }

        parts.get(1).map_or_else(
            || Self::Value((*parts.first().unwrap()).into()),
            |&op| match op {
                "LSHIFT" => Self::LShift {
                    lhs: (*parts.first().unwrap()).into(),
                    rhs: parts.last().unwrap().parse().unwrap(),
                },
                "RSHIFT" => Self::RShift {
                    lhs: (*parts.first().unwrap()).into(),
                    rhs: parts.last().unwrap().parse().unwrap(),
                },
                "AND" => Self::And {
                    lhs: (*parts.first().unwrap()).into(),
                    rhs: (*parts.last().unwrap()).into(),
                },
                "OR" => Self::Or {
                    lhs: (*parts.first().unwrap()).into(),
                    rhs: (*parts.last().unwrap()).into(),
                },
                other => unreachable!("unknown op: '{other}'"),
            },
        )
    }
}

#[derive(Clone, Debug)]
struct Booklet(HashMap<Wire, Expr>);

impl Deref for Booklet {
    type Target = HashMap<Wire, Expr>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Booklet {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| {
                    line.trim()
                        .split_once("->")
                        .map(|(expr, wire)| (wire.trim().into(), expr.trim().into()))
                        .unwrap()
                })
                .collect(),
        )
    }
}

#[derive(Clone, Debug)]
struct Circut {
    booklet: Booklet,
    wires: Wires,
}

impl From<&str> for Circut {
    fn from(value: &str) -> Self {
        Self {
            booklet: value.into(),
            wires: Wires::default(),
        }
    }
}

impl Circut {
    fn resolve(&mut self, wire: Wire) -> u16 {
        if let Some(v) = self.wires.get(&wire) {
            return *v;
        } else {
            let value = self.resolve_expr(self.booklet[&wire]);
            self.wires.insert(wire, value);
            value
        }
    }

    fn resolve_expr(&mut self, expr: Expr) -> u16 {
        match expr {
            Expr::Value(value) => self.resolve_value(value),
            Expr::And { lhs, rhs } => self.resolve_value(lhs) & self.resolve_value(rhs),
            Expr::Or { lhs, rhs } => self.resolve_value(lhs) | self.resolve_value(rhs),
            Expr::LShift { lhs, rhs } => self.resolve(lhs) << rhs,
            Expr::RShift { lhs, rhs } => self.resolve(lhs) >> rhs,
            Expr::Not(wire) => !self.resolve(wire),
        }
    }

    fn resolve_value(&mut self, value: Value) -> u16 {
        match value {
            Value::Constant(v) => v,
            Value::Wire(wire) => self.resolve(wire),
        }
    }
}

struct Day07;

impl Day for Day07 {
    type Parsed = Circut;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> u16 {
        let mut circut = input.clone();
        circut.resolve("a".into())
    }

    fn part2(input: &Self::Parsed) -> u16 {
        let mut circut = input.clone();
        let a = circut.resolve("a".into());

        circut.wires.clear();
        circut.wires.insert("b".into(), a);

        circut.resolve("a".into())
    }
}

aoc_main!(Day07);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        let mut circut = Circut::from(
            "
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
",
        );

        let raw_wires = "
d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456
";

        let expected_wires = Wires(
            raw_wires
                .trim()
                .lines()
                .filter_map(|l| {
                    l.split_once(':')
                        .map(|(wire, value)| (wire.into(), value.trim().parse().unwrap()))
                })
                .collect(),
        );

        for (&wire, &expected) in expected_wires.iter() {
            assert_eq!(circut.resolve(wire), expected, "{wire:?}");
        }
    }
}
