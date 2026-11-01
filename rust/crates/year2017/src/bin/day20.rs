use std::collections::{HashMap, HashSet};

use util::{Day, Vec3, aoc_main};

type IVec3 = Vec3<isize>;

#[derive(Clone, Debug)]
struct Particles(HashMap<u16, Particle>);

impl Particles {
    #[must_use]
    fn left_after_collide(&self) -> usize {
        let mut collided = HashSet::new();
        let entries = self.0.clone().into_iter().collect::<Vec<_>>();

        let len = entries.len();
        for i in 0..len {
            for j in 1..len {
                if i == j {
                    continue;
                }

                let (k0, v0) = entries[i];
                let (k1, v1) = entries[j];
                if v0.collide_with(&v1, len as u16) {
                    collided.insert(k0);
                    collided.insert(k1);
                }
            }
        }

        len - collided.len()
    }

    #[must_use]
    fn at(&self, t: u16) -> HashMap<u16, IVec3> {
        self.0.iter().map(|(&k, v)| (k, v.at(t))).collect()
    }

    #[must_use]
    fn closest(&self) -> u16 {
        self.at(u16::MAX - 1)
            .iter()
            .min_by_key(|&(_, v)| v.abs().element_sum())
            .map(|(&k, _)| k)
            .unwrap()
    }
}

impl From<&str> for Particles {
    fn from(raw: &str) -> Self {
        let mut map = HashMap::new();
        raw.trim()
            .lines()
            .map(Into::into)
            .enumerate()
            .for_each(|(id, particle)| {
                map.insert(id as u16, particle);
            });
        Self(map)
    }
}

#[derive(Clone, Copy, Debug, Default)]
struct Particle {
    pos: IVec3,
    vel: IVec3,
    acc: IVec3,
}

impl Particle {
    #[must_use]
    fn collide_with(&self, other: &Self, limit: u16) -> bool {
        for t in 0..=limit {
            if self.at(t) == other.at(t) {
                return true;
            }
        }

        false
    }

    #[must_use]
    fn at(&self, t: u16) -> IVec3 {
        let x = t.try_into().unwrap();
        self.pos + self.vel * x + self.acc * x * (x + 1) / 2
    }
}

impl From<&str> for Particle {
    fn from(raw: &str) -> Self {
        let buf = raw
            .trim()
            .split(", ")
            .map(|s| {
                s.strip_suffix('>')
                    .unwrap()
                    .chars()
                    .skip_while(|&c| !c.is_numeric() && c != '-')
                    .collect::<String>()
                    .as_str()
                    .into()
            })
            .collect::<Vec<IVec3>>();

        Self {
            pos: buf[0],
            vel: buf[1],
            acc: buf[2],
        }
    }
}

struct Day20;

impl Day for Day20 {
    type Parsed = Particles;

    fn parse(input: &str) -> Self::Parsed {
        input.into()
    }

    fn part1(input: &Self::Parsed) -> u16 {
        input.closest()
    }

    fn part2(input: &Self::Parsed) -> usize {
        input.left_after_collide()
    }
}

aoc_main!(Day20);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]

    fn p1e1() {
        let input = "
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
";
        assert_eq!(Day20::part1(&Day20::parse(input)), 0);
    }

    #[test]
    fn p2e1() {
        let input = "
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
";
        assert_eq!(Day20::part2(&Day20::parse(input)), 1);
    }
}
