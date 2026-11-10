use std::{
    collections::HashSet,
    fmt,
    ops::{Deref, DerefMut, Not},
};

use util::{Day, aoc_main};

#[derive(Clone, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Molecule(String);

impl fmt::Display for Molecule {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        fmt::Display::fmt(&self.0, f)
    }
}

impl From<&str> for Molecule {
    fn from(value: &str) -> Self {
        value.to_owned().into()
    }
}

impl From<String> for Molecule {
    fn from(value: String) -> Self {
        Self(value)
    }
}

impl Deref for Molecule {
    type Target = String;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Molecule {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Debug)]
struct Replacement {
    from: Molecule,
    to: Molecule,
}

impl Not for Replacement {
    type Output = Self;

    fn not(self) -> Self::Output {
        Self {
            from: self.to,
            to: self.from,
        }
    }
}

impl From<&str> for Replacement {
    fn from(value: &str) -> Self {
        let (from, to) = value.trim().split_once(" => ").unwrap();

        Self {
            from: from.into(),
            to: to.into(),
        }
    }
}

#[derive(Clone, Debug)]
struct Replacements(Vec<Replacement>);

impl Replacements {
    fn of<'a>(&'a self, molecule: &'a Molecule) -> impl Iterator<Item = Molecule> + 'a {
        self.iter().flat_map(move |replacement| {
            molecule
                .char_indices()
                .map(|(i, _)| i)
                .filter(move |&i| molecule[i..].starts_with(replacement.from.as_str()))
                .map(move |i| {
                    format!(
                        "{}{}{}",
                        &molecule[..i],
                        replacement.to,
                        &molecule[i + replacement.from.len()..]
                    )
                    .into()
                })
        })
    }

    fn walk(&self, target: &Molecule) -> usize {
        self.walk_inner(target, 0).unwrap()
    }

    fn walk_inner(&self, target: &Molecule, depth: usize) -> Option<usize> {
        if target.as_str() == "e" {
            return Some(depth);
        }

        for nmolecule in self.of(target).collect::<HashSet<_>>().iter() {
            let Some(steps) = self.walk_inner(nmolecule, depth + 1) else {
                continue;
            };
            return Some(steps);
        }

        None
    }
}

impl From<&str> for Replacements {
    fn from(value: &str) -> Self {
        value.trim().lines().map(Into::into).collect()
    }
}

impl FromIterator<Replacement> for Replacements {
    fn from_iter<I: IntoIterator<Item = Replacement>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}

impl Deref for Replacements {
    type Target = Vec<Replacement>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Debug)]
struct FusionPlant {
    replacements: Replacements,
    medicine: Molecule,
}

impl From<&str> for FusionPlant {
    fn from(value: &str) -> Self {
        let (replacements, medicine) = value.trim().split_once("\n\n").unwrap();

        Self {
            replacements: replacements.into(),
            medicine: medicine.into(),
        }
    }
}

fn part2_inner(replacements: &Replacements, target: &Molecule) -> usize {
    let inv_replacments = replacements
        .iter()
        .cloned()
        .map(Not::not)
        .collect::<Replacements>();

    inv_replacments.walk(target)
}

struct Day19;

impl Day for Day19 {
    type Parsed = FusionPlant;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input
            .replacements
            .of(&input.medicine)
            .collect::<HashSet<_>>()
            .len()
    }

    fn part2(input: &Self::Parsed) -> usize {
        part2_inner(&input.replacements, &input.medicine)
    }
}

aoc_main!(Day19);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        let replacements = Replacements::from(
            "
H => HO
H => OH
O => HH
            ",
        );

        assert_eq!(
            replacements.of(&"HOH".into()).collect::<HashSet<_>>(),
            ["HOOH", "HOHO", "OHOH", "HOOH", "HHHH"]
                .into_iter()
                .map(Into::into)
                .collect()
        );
    }

    #[test]
    fn part2() {
        let replacements = Replacements::from(
            "
e => H
e => O
H => HO
H => OH
O => HH
",
        );

        assert_eq!(part2_inner(&replacements, &"HOH".into()), 3);
        assert_eq!(part2_inner(&replacements, &"HOHOHO".into()), 6);
    }
}
