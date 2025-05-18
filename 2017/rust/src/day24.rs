use std::{collections::HashSet, iter, ops::Deref};

#[derive(Clone, Copy, Debug, Eq, Hash, PartialEq)]
struct Componenet([u8; 2]);

impl From<&str> for Componenet {
    fn from(raw: &str) -> Self {
        let nums = raw
            .split('/')
            .filter_map(|x| x.parse().ok())
            .collect::<Vec<_>>()
            .try_into()
            .unwrap();
        Self(nums)
    }
}

impl Deref for Componenet {
    type Target = [u8; 2];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Debug, Default)]
struct Componenets(HashSet<Componenet>);

impl Componenets {
    #[must_use]
    const fn new(componenets: HashSet<Componenet>) -> Self {
        Self(componenets)
    }

    #[must_use]
    fn possible_bridges(&self) -> Vec<Bridge> {
        let mut bridges = vec![];
        let mut queue = vec![Bridge::default()];
        while let Some(bridge) = queue.pop() {
            let candidates = self
                .difference(&bridge.componenets)
                .filter(|&comp| comp.contains(&bridge.port))
                .collect::<Vec<_>>();

            if candidates.len() == 0 {
                bridges.push(bridge);
                continue;
            }

            for candidate in candidates {
                let nport = if candidate[0] == bridge.port {
                    candidate[1]
                } else {
                    candidate[0]
                };

                let ncomponenets = Componenets::new(
                    bridge
                        .componenets
                        .iter()
                        .cloned()
                        .chain(iter::once(*candidate))
                        .collect(),
                );
                queue.push(Bridge::new(ncomponenets, nport));
            }
        }
        bridges
    }
}

impl From<&str> for Componenets {
    fn from(raw: &str) -> Self {
        Self(raw.trim().lines().map(|l| l.trim().into()).collect())
    }
}

impl Deref for Componenets {
    type Target = HashSet<Componenet>;

    #[inline]
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

#[derive(Clone, Debug, Default)]
struct Bridge {
    componenets: Componenets,
    port: u8,
}

impl Bridge {
    #[must_use]
    const fn new(componenets: Componenets, port: u8) -> Self {
        Self { componenets, port }
    }

    #[inline]
    #[must_use]
    fn len(&self) -> usize {
        self.componenets.len()
    }

    #[must_use]
    fn strength(&self) -> u16 {
        self.componenets
            .iter()
            .map(|&comp| comp.iter().map(|&x| u16::from(x)).sum::<u16>())
            .sum()
    }
}

fn p1(input: &str) -> u16 {
    let bridges = Componenets::from(input).possible_bridges();
    bridges.iter().map(|b| b.strength()).max().unwrap()
}

fn p2(input: &str) -> u16 {
    let bridges = Componenets::from(input).possible_bridges();
    bridges
        .iter()
        .map(|b| (b.len(), b.strength()))
        .max_by(|a, b| a.0.cmp(&b.0).then_with(|| a.1.cmp(&b.1)))
        .map(|(_, s)| s)
        .unwrap()
}

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[cfg(test)]
mod tests {
    use super::*;

    const INPUT: &str = "
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 31);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 19);
    }
}
