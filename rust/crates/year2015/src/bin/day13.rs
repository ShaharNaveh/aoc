use std::{
    collections::HashMap,
    iter::Sum,
    ops::{Add, Deref, DerefMut},
};

use util::{Day, aoc_main, calculate_hash};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Guest(u64);

impl From<&str> for Guest {
    fn from(value: &str) -> Self {
        Self(calculate_hash(&value))
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum Attendee {
    Me,
    Guest(Guest),
}

impl From<Guest> for Attendee {
    fn from(guest: Guest) -> Self {
        Self::Guest(guest)
    }
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
struct Attendees(Vec<Attendee>);

impl Deref for Attendees {
    type Target = Vec<Attendee>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Attendees {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&Settings> for Attendees {
    fn from(settings: &Settings) -> Self {
        settings.keys().copied().collect()
    }
}

impl FromIterator<Attendee> for Attendees {
    fn from_iter<I: IntoIterator<Item = Attendee>>(iter: I) -> Self {
        Self(iter.into_iter().collect())
    }
}

#[derive(Clone, Debug)]
struct Settings(HashMap<Attendee, HashMap<Attendee, isize>>);

impl Settings {
    fn best_happiness(&self) -> Happiness {
        let attendees = Attendees::from(self);

        AttendeesPermutations::from(attendees)
            .into_iter()
            .map(|perm| Happiness::new(&perm, &self))
            .max()
            .unwrap()
    }
}

impl From<&str> for Settings {
    fn from(value: &str) -> Self {
        let mut table = HashMap::new();

        for line in value.trim().lines().map(|l| l.trim_end_matches('.')) {
            let parts = line.split_ascii_whitespace().collect::<Vec<_>>();

            let guest = Guest::from(parts[0]).into();
            let other = Guest::from(*parts.last().unwrap()).into();

            let happiness = {
                let value = parts[3].parse::<isize>().unwrap();
                match parts[2] {
                    "gain" => value,
                    "lose" => -value,
                    other => panic!("unknown: '{other}'"),
                }
            };

            table
                .entry(guest)
                .or_insert_with(HashMap::new)
                .insert(other, happiness);
        }

        Self(table)
    }
}

impl Deref for Settings {
    type Target = HashMap<Attendee, HashMap<Attendee, isize>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Settings {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Happiness(isize);

impl From<Happiness> for isize {
    fn from(value: Happiness) -> Self {
        value.0
    }
}

impl Add<Happiness> for Happiness {
    type Output = Happiness;

    fn add(self, rhs: Happiness) -> Self::Output {
        Self(self.0 + rhs.0)
    }
}

impl Happiness {
    pub const ZERO: Self = Self(0);

    fn new(attendees: &Attendees, settings: &Settings) -> Self {
        attendees
            .windows(2)
            .map(|w| {
                let [lhs, rhs] = w else { unreachable!() };
                Self::of(lhs, rhs, &settings)
            })
            .sum::<Happiness>()
            + Self::of(
                attendees.first().unwrap(),
                attendees.last().unwrap(),
                &settings,
            )
    }

    fn of(lhs: &Attendee, rhs: &Attendee, settings: &Settings) -> Self {
        if lhs == &Attendee::Me || rhs == &Attendee::Me {
            return Self::ZERO;
        }

        Self(settings[lhs][rhs] + settings[rhs][lhs])
    }
}

impl Sum for Happiness {
    fn sum<I: Iterator<Item = Self>>(iter: I) -> Self {
        iter.fold(Self::ZERO, |a, b| a + b)
    }
}

#[derive(Debug)]
struct AttendeesPermutations {
    attendees: Attendees,
    counter: Vec<usize>,
    idx: usize,
}

impl From<Attendees> for AttendeesPermutations {
    fn from(value: Attendees) -> Self {
        let len = value.len();
        Self {
            attendees: value,
            counter: vec![0; len],
            idx: 0,
        }
    }
}

impl Iterator for AttendeesPermutations {
    type Item = Attendees;

    fn next(&mut self) -> Option<Self::Item> {
        let len = self.attendees.len();

        loop {
            if self.idx >= len {
                return None;
            }

            if self.counter[self.idx] < self.idx {
                if self.idx % 2 == 0 {
                    self.attendees.swap(0, self.idx);
                } else {
                    self.attendees.swap(self.counter[self.idx], self.idx);
                }

                self.counter[self.idx] += 1;
                self.idx = 0;
                return Some(self.attendees.clone());
            } else {
                self.counter[self.idx] = 0;
                self.idx += 1;
            }
        }
    }
}

struct Day13;

impl Day for Day13 {
    type Parsed = Settings;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> isize {
        input.best_happiness().into()
    }

    fn part2(input: &Self::Parsed) -> isize {
        let mut settings = input.clone();
        settings.insert(Attendee::Me, HashMap::default());

        settings.best_happiness().into()
    }
}

aoc_main!(Day13);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        assert_eq!(
            Day13::part1(&Day13::parse(
                "
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
"
            )),
            330
        );
    }
}
