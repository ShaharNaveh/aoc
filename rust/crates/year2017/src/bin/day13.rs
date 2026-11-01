use std::collections::HashMap;

use util::{Day, aoc_main};

#[derive(Debug)]
struct FireWall(HashMap<u32, u32>);

impl FireWall {
    fn send_packet(&self, delay: u32) -> Vec<u32> {
        self.0
            .iter()
            .filter(|&(&layer, &range)| (layer + delay) % (2 * (range - 1)) == 0)
            .map(|(layer, range)| layer * range)
            .collect()
    }
}

impl From<&str> for FireWall {
    fn from(raw: &str) -> Self {
        let mut map = HashMap::new();
        raw.trim().lines().for_each(|line| {
            let vec = line
                .trim()
                .split(':')
                .filter_map(|l| l.trim().parse().ok())
                .collect::<Vec<_>>();

            map.insert(vec[0], vec[1]);
        });
        Self(map)
    }
}

struct Day13;

impl Day for Day13 {
    type Parsed = FireWall;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> u32 {
        input.send_packet(0).iter().sum()
    }

    fn part2(input: &Self::Parsed) -> u32 {
        let firewall = input;
        (1..)
            .find(|&delay| firewall.send_packet(delay).len() == 0)
            .unwrap()
    }
}

aoc_main!(Day13);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
0: 3
1: 2
4: 4
6: 4
";

    #[test]
    fn part1() {
        let parsed = Day13::parse(INPUT);
        assert_eq!(Day13::part1(&parsed), 24);
    }

    #[test]
    fn part2() {
        let parsed = Day13::parse(INPUT);
        assert_eq!(Day13::part2(&parsed), 10);
    }
}
