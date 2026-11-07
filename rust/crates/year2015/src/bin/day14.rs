use std::{
    collections::HashMap,
    ops::{Deref, DerefMut},
};

use util::{Day, aoc_main, calculate_hash};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct ReindeerId(u64);

impl From<&str> for ReindeerId {
    fn from(value: &str) -> Self {
        Self(calculate_hash(&value))
    }
}

#[derive(Clone, Copy, Debug)]
struct ReindeerSpec {
    speed: usize,
    fly_duration: usize,
    rest_duration: usize,
}

impl From<&str> for ReindeerSpec {
    fn from(value: &str) -> Self {
        let nums = value
            .trim()
            .split_ascii_whitespace()
            .filter_map(|x| x.parse().ok())
            .collect::<Vec<_>>();

        Self {
            speed: nums[0],
            fly_duration: nums[1],
            rest_duration: nums[2],
        }
    }
}

#[derive(Clone, Debug)]
struct Reindeers(HashMap<ReindeerId, ReindeerSpec>);

impl From<&str> for Reindeers {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .map(|line| {
                    (
                        line.split_ascii_whitespace().next().unwrap().into(),
                        line.into(),
                    )
                })
                .collect(),
        )
    }
}

impl Deref for Reindeers {
    type Target = HashMap<ReindeerId, ReindeerSpec>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Copy, Debug)]
enum Mode {
    Rest { duration: usize },
    Fly { duration: usize },
}

impl Default for Mode {
    fn default() -> Self {
        Self::Rest { duration: 0 }
    }
}

#[derive(Clone, Copy, Debug, Default)]
struct ReindeerState {
    distance: usize,
    mode: Mode,
    points: usize,
}

#[derive(Clone, Debug)]
struct RaceState(HashMap<ReindeerId, ReindeerState>);

impl Deref for RaceState {
    type Target = HashMap<ReindeerId, ReindeerState>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for RaceState {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&Reindeers> for RaceState {
    fn from(value: &Reindeers) -> Self {
        Self(
            value
                .keys()
                .copied()
                .map(|id| (id, ReindeerState::default()))
                .collect(),
        )
    }
}

#[derive(Clone, Debug)]
struct Race {
    reindeers: Reindeers,
    state: RaceState,
}

impl Race {
    fn tick_for(mut self, seconds: usize) -> Self {
        (0..seconds).for_each(|_| self.tick());
        self
    }

    fn tick(&mut self) {
        for (id, state) in self.state.iter_mut() {
            let spec = self.reindeers[&id];
            if let Mode::Rest { duration } = state.mode
                && duration == 0
            {
                state.mode = Mode::Fly {
                    duration: spec.fly_duration,
                };
            }

            state.mode = match state.mode {
                Mode::Fly { duration } if duration == 0 => Mode::Rest {
                    duration: spec.rest_duration - 1,
                },
                Mode::Fly { duration } => {
                    state.distance += spec.speed;
                    Mode::Fly {
                        duration: duration - 1,
                    }
                }
                Mode::Rest { duration } => {
                    debug_assert_ne!(duration, 0);
                    Mode::Rest {
                        duration: duration - 1,
                    }
                }
            }
        }

        let max_dist = self.highest_distance().1.distance;
        for state in self.state.values_mut() {
            if state.distance != max_dist {
                continue;
            }

            state.points += 1;
        }
    }

    fn highest_distance(&self) -> (&ReindeerId, &ReindeerState) {
        self.state
            .iter()
            .max_by_key(|(_, state)| state.distance)
            .unwrap()
    }

    fn highest_points(&self) -> (&ReindeerId, &ReindeerState) {
        self.state
            .iter()
            .max_by_key(|(_, state)| state.points)
            .unwrap()
    }
}

impl From<&str> for Race {
    fn from(value: &str) -> Self {
        let reindeers = Reindeers::from(value);

        Self {
            state: (&reindeers).into(),
            reindeers,
        }
    }
}

struct Day14;

impl Day for Day14 {
    type Parsed = Race;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().tick_for(2503).highest_distance().1.distance
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.clone().tick_for(2503).highest_points().1.points
    }
}

aoc_main!(Day14);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
Comet can fly 14 km/s for 10 seconds , but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds , but then must rest for 162 seconds.
";

    #[test]
    fn part1() {
        let race = Day14::parse(INPUT);
        for (seconds, highest) in [(1, 16), (1000, 1120)] {
            assert_eq!(
                race.clone().tick_for(seconds).highest_distance().1.distance,
                highest,
                "{seconds}"
            );
        }
    }

    #[test]
    fn part2() {
        let race = Day14::parse(INPUT);
        for (seconds, highest) in [(1, 1), (1000, 689)] {
            assert_eq!(
                race.clone().tick_for(seconds).highest_points().1.points,
                highest,
                "{seconds}"
            );
        }
    }
}
