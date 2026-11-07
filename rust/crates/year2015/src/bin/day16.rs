use std::{collections::HashMap, ops::Deref};

use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum Finding {
    Children,
    Cats,
    Samoyeds,
    Pomeranians,
    Akitas,
    Vizslas,
    Goldfish,
    Trees,
    Cars,
    Perfumes,
}

impl From<&str> for Finding {
    fn from(value: &str) -> Self {
        match value {
            "children" => Self::Children,
            "cats" => Self::Cats,
            "samoyeds" => Self::Samoyeds,
            "pomeranians" => Self::Pomeranians,
            "akitas" => Self::Akitas,
            "vizslas" => Self::Vizslas,
            "goldfish" => Self::Goldfish,
            "trees" => Self::Trees,
            "cars" => Self::Cars,
            "perfumes" => Self::Perfumes,
            other => panic!("unknown: '{other}'"),
        }
    }
}

#[derive(Debug)]
struct Aunt(HashMap<Finding, usize>);

impl Aunt {
    const KNOWN_INPUT: &str = "
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1";

    fn known() -> Self {
        Self::KNOWN_INPUT.trim().replace('\n', ",").as_str().into()
    }
}

impl Deref for Aunt {
    type Target = HashMap<Finding, usize>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl From<&str> for Aunt {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .split(',')
                .map(|s| {
                    s.trim()
                        .split_once(':')
                        .map(|(finding, amount)| (finding.into(), amount.trim().parse().unwrap()))
                        .unwrap()
                })
                .collect(),
        )
    }
}

#[derive(Debug)]
struct Aunts(Vec<Aunt>);

impl Aunts {
    fn find(&self, known: &Aunt, is_p2: bool) -> usize {
        for (idx, aunt) in self.iter().enumerate() {
            if !known.iter().all(|(finding, &amount)| {
                aunt.get(finding).is_none_or(|&value| {
                    if !is_p2 {
                        value == amount
                    } else {
                        match finding {
                            Finding::Cats | Finding::Trees => value > amount,
                            Finding::Pomeranians | Finding::Goldfish => value < amount,
                            _ => value == amount,
                        }
                    }
                })
            }) {
                continue;
            }

            return idx + 1;
        }

        panic!("Did not find which aunt");
    }
}

impl From<&str> for Aunts {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| line.split_once(':').unwrap().1.into())
                .collect(),
        )
    }
}

impl Deref for Aunts {
    type Target = Vec<Aunt>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

struct Day16;

impl Day for Day16 {
    type Parsed = Aunts;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.find(&Aunt::known(), false)
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.find(&Aunt::known(), true)
    }
}

aoc_main!(Day16);
