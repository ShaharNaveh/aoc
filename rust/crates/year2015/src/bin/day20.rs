use util::{Day, aoc_main};

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct HouseId(usize);

impl From<usize> for HouseId {
    fn from(value: usize) -> Self {
        Self(value)
    }
}

impl From<HouseId> for usize {
    fn from(value: HouseId) -> Self {
        value.0
    }
}

impl Default for HouseId {
    fn default() -> Self {
        Self(1)
    }
}

impl HouseId {
    fn divisors(&self) -> Vec<usize> {
        let mut small = (1..=self.0.isqrt())
            .into_iter()
            .filter(|i| self.0 % i == 0)
            .collect::<Vec<_>>();

        let mut large = small
            .iter()
            .filter_map(|div| (self.0 != div.pow(2)).then(|| self.0 / div))
            .collect::<Vec<_>>();

        small.append(&mut large);
        small
    }
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Presents(usize);

impl From<usize> for Presents {
    fn from(value: usize) -> Self {
        Self(value)
    }
}

impl From<&str> for Presents {
    fn from(value: &str) -> Self {
        Self(value.parse().unwrap())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct House {
    id: HouseId,
    presents: Presents,
}

trait PresentPolicy {
    fn at(&self, house: HouseId) -> Presents;
}

struct Houses<P: PresentPolicy> {
    policy: P,
    current: HouseId,
}

impl<P: PresentPolicy> Houses<P> {
    fn new(policy: P) -> Self {
        Self {
            policy,
            current: HouseId::default(),
        }
    }
}

impl<P: PresentPolicy> Iterator for Houses<P> {
    type Item = House;

    fn next(&mut self) -> Option<Self::Item> {
        let res = House {
            id: self.current,
            presents: self.policy.at(self.current),
        };

        self.current = (self.current.0 + 1).into();

        Some(res)
    }
}

struct Part1Policy;

impl PresentPolicy for Part1Policy {
    fn at(&self, house: HouseId) -> Presents {
        (house.divisors().iter().sum::<usize>() * 10).into()
    }
}

struct Part2Policy;

impl PresentPolicy for Part2Policy {
    fn at(&self, house: HouseId) -> Presents {
        (house
            .divisors()
            .into_iter()
            .filter(|div| (house.0 / div) <= 50)
            .sum::<usize>()
            * 11)
            .into()
    }
}

struct Day20;

impl Day for Day20 {
    type Parsed = Presents;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        Houses::new(Part1Policy)
            .into_iter()
            .find(|house| house.presents >= *input)
            .unwrap()
            .id
            .into()
    }

    fn part2(input: &Self::Parsed) -> usize {
        Houses::new(Part2Policy)
            .into_iter()
            .find(|house| house.presents >= *input)
            .unwrap()
            .id
            .into()
    }
}

aoc_main!(Day20);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn part1() {
        for (house, expected) in [
            (1, 10),
            (2, 30),
            (3, 40),
            (4, 70),
            (5, 60),
            (6, 120),
            (7, 80),
            (8, 150),
            (9, 130),
        ] {
            assert_eq!(
                Part1Policy.at(house.into()),
                Presents::from(expected),
                "{house}"
            );
        }
    }
}
