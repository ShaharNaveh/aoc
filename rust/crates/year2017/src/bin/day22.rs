use std::collections::HashMap;

use util::{Day, IVec2, aoc_main};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
enum NodeState {
    Clean,
    Weakened,
    Infected,
    Flagged,
}

#[derive(Clone, Debug)]
struct VirusState {
    node: IVec2,
    direction: IVec2,
    nodes: HashMap<IVec2, NodeState>,
    count: usize,
}

impl VirusState {
    #[inline]
    #[must_use]
    fn do_bursts(mut self, n: usize) -> usize {
        for _ in 0..n {
            self = self.burst();
        }
        self.count
    }

    #[must_use]
    fn burst(mut self) -> Self {
        let is_on_infected = matches!(
            self.nodes.get(&self.node).unwrap_or(&NodeState::Clean),
            NodeState::Infected
        );

        let rotation = if is_on_infected {
            IVec2::Y
        } else {
            IVec2::NEG_Y
        };

        self.direction = self.direction.rotate(rotation);

        if is_on_infected {
            self.nodes.remove(&self.node);
        } else {
            self.nodes.insert(self.node, NodeState::Infected);
            self.count += 1;
        }
        self.node += self.direction;

        self
    }

    #[must_use]
    fn evolved_burst(mut self) -> Self {
        let state = self.nodes.get(&self.node).unwrap_or(&NodeState::Clean);

        self.direction = match state {
            NodeState::Clean => self.direction.rotate(IVec2::NEG_Y),
            NodeState::Weakened => self.direction,
            NodeState::Infected => self.direction.rotate(IVec2::Y),
            NodeState::Flagged => -self.direction,
        };

        let nstate = match state {
            NodeState::Clean => NodeState::Weakened,
            NodeState::Weakened => NodeState::Infected,
            NodeState::Infected => NodeState::Flagged,
            NodeState::Flagged => NodeState::Clean,
        };

        match nstate {
            NodeState::Clean => {
                self.nodes.remove(&self.node);
            }
            NodeState::Infected => {
                self.nodes.insert(self.node, nstate);
                self.count += 1;
            }
            _ => {
                self.nodes.insert(self.node, nstate);
            }
        };

        self.node += self.direction;

        self
    }

    #[inline]
    #[must_use]
    fn do_evolved_bursts(mut self, n: usize) -> usize {
        for _ in 0..n {
            self = self.evolved_burst();
        }
        self.count
    }
}

impl From<&str> for VirusState {
    fn from(raw: &str) -> Self {
        let grid = raw
            .trim()
            .lines()
            .enumerate()
            .map(|(y, row)| {
                row.trim()
                    .chars()
                    .enumerate()
                    .map(|(x, c)| (IVec2::new(x as i32, y as i32), c))
                    .collect::<Vec<_>>()
            })
            .flatten()
            .collect::<HashMap<_, _>>();

        let max_node = grid
            .keys()
            .copied()
            .reduce(|acc, node| acc.max(node))
            .unwrap();

        let nodes = grid
            .iter()
            .filter(|&(_, &v)| v == '#')
            .map(|(&k, _)| (k, NodeState::Infected))
            .collect();

        VirusState {
            node: max_node / 2,
            direction: IVec2::NEG_Y,
            nodes,
            count: 0,
        }
    }
}

struct Day22;

impl Day for Day22 {
    type Parsed = VirusState;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> usize {
        input.clone().do_bursts(10_000)
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.clone().do_evolved_bursts(10_000_000)
    }
}

aoc_main!(Day22);

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
..#
#..
...
";

    #[test]
    fn p1e1() {
        let virus_state = VirusState::from(INPUT);
        for (n, expected) in [(7, 5), (70, 41)] {
            let result = virus_state.clone().do_bursts(n);
            assert_eq!(result, expected);
        }

        assert_eq!(Day22::part1(&Day22::parse(INPUT)), 5587);
    }

    #[test]
    fn p2e1() {
        assert_eq!(VirusState::from(INPUT).do_evolved_bursts(100), 26);
        assert_eq!(Day22::part2(&Day22::parse(INPUT)), 2511944);
    }
}
