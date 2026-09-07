use std::{
    collections::{BTreeSet, HashSet},
    num::NonZeroUsize,
    ops::{Deref, DerefMut, Index, IndexMut},
};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Name<'a>(&'a str);

impl<'a> From<&'a str> for Name<'a> {
    fn from(value: &'a str) -> Self {
        Self(value)
    }
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
enum Equipment<'a> {
    Rtg(Name<'a>),
    Chip(Name<'a>),
}

impl<'a> From<&'a str> for Equipment<'a> {
    fn from(raw: &'a str) -> Self {
        let (name, typ) = raw.split_once(' ').unwrap();
        match typ {
            "generator" => Self::Rtg(name.into()),
            "microchip" => {
                debug_assert!(name.ends_with("-compatible"));
                Self::Chip(name.trim_end_matches("-compatible").into())
            }
            other => unreachable!("unknown component type: {other}"),
        }
    }
}

#[derive(Clone, Copy, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd)]
enum Floor {
    #[default]
    First,
    Second,
    Third,
    Fourth,
}

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
enum Direction {
    Up,
    Down,
}

impl Floor {
    const ALL: [Self; 4] = [Self::First, Self::Second, Self::Third, Self::Fourth];

    const fn as_usize(self) -> NonZeroUsize {
        // SAFETY: can never be zero
        unsafe {
            NonZeroUsize::new_unchecked(match self {
                Self::First => 1,
                Self::Second => 2,
                Self::Third => 3,
                Self::Fourth => 4,
            })
        }
    }

    fn r#move(self, direction: Direction) -> Option<Self> {
        let val = self.as_usize().get();
        Self::try_from(match direction {
            Direction::Up => val + 1,
            Direction::Down => val - 1,
        })
        .ok()
    }
}

impl TryFrom<usize> for Floor {
    type Error = ();

    fn try_from(value: usize) -> Result<Self, Self::Error> {
        Ok(match value {
            1 => Self::First,
            2 => Self::Second,
            3 => Self::Third,
            4 => Self::Fourth,
            _ => return Err(()),
        })
    }
}

#[derive(Clone, Debug, Default, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Equipments<'eq>(BTreeSet<Equipment<'eq>>);

impl Equipments<'_> {
    fn is_fried(&self) -> bool {
        let mut gens = HashSet::new();
        let mut chips = HashSet::new();

        for eq in self.iter() {
            match eq {
                Equipment::Rtg(v) => gens.insert(v),
                Equipment::Chip(v) => chips.insert(v),
            };
        }

        !(gens.is_empty() || chips.is_subset(&gens))
    }
}

impl<'eq> From<&'eq str> for Equipments<'eq> {
    fn from(raw: &'eq str) -> Self {
        Self(
            raw.trim()
                .trim_end_matches(".")
                .split(" a ")
                .map(|s| {
                    s.trim()
                        .trim_end_matches(" and")
                        .trim_end_matches(',')
                        .trim_start_matches("a ")
                        .trim()
                })
                .filter(|&s| s != "nothing relevant")
                .map(Into::into)
                .collect(),
        )
    }
}

impl<'eq> Deref for Equipments<'eq> {
    type Target = BTreeSet<Equipment<'eq>>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Equipments<'_> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Floors<'eq, const N: usize>([Equipments<'eq>; N]);

impl<'eq, const N: usize> Default for Floors<'_, N> {
    fn default() -> Self {
        Self(std::array::from_fn(|_| Equipments::default()))
    }
}

impl<'eq, const N: usize> From<&'eq str> for Floors<'eq, N> {
    fn from(raw: &'eq str) -> Self {
        let mut floors = Self::default();

        for (i, line) in raw.trim().lines().enumerate() {
            let floor = Floor::try_from(i + 1).unwrap();
            let equipments = line.trim().split_once(" contains ").unwrap().1.into();

            floors[floor] = equipments;
        }

        floors
    }
}

impl<'eq, const N: usize> Deref for Floors<'eq, N> {
    type Target = [Equipments<'eq>; N];

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl<const N: usize> DerefMut for Floors<'_, N> {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl<'eq, const N: usize> Index<Floor> for Floors<'eq, N> {
    type Output = Equipments<'eq>;

    fn index(&self, floor: Floor) -> &Self::Output {
        let idx = floor.as_usize().get() - 1;
        &self.0[idx]
    }
}

impl<const N: usize> IndexMut<Floor> for Floors<'_, N> {
    fn index_mut(&mut self, floor: Floor) -> &mut Self::Output {
        let idx = floor.as_usize().get() - 1;
        &mut self.0[idx]
    }
}

#[derive(Clone, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
struct Facility<'eq> {
    /// Current floor.
    floor: Floor,
    /// Floors state.
    floors: Floors<'eq, 4>,
}

impl<'eq> Index<Floor> for Facility<'eq> {
    type Output = Equipments<'eq>;

    fn index(&self, floor: Floor) -> &Self::Output {
        &self.floors[floor]
    }
}

impl<'eq> Facility<'eq> {
    fn solve(start: Self) -> usize {
        let mut seen = HashSet::new();
        let mut states = BTreeSet::from([(0, start)]);

        while let Some((steps, facility)) = states.pop_first() {
            if !seen.insert(facility.clone()) {
                continue;
            }

            if facility.is_done() {
                return steps;
            }

            let nsteps = steps + 1;
            for nfacility in facility.next_facilities() {
                states.insert((nsteps, nfacility));
            }
        }

        panic!("could not solve");
    }

    fn try_traverse(&self, direction: Direction, grab: &Equipments<'eq>) -> Option<Self> {
        let src = self.floor;
        let dest = self.floor.r#move(direction)?;

        if grab.is_empty() {
            return None;
        }

        let new_src = Equipments(self[src].difference(grab).cloned().collect());
        if new_src.is_fried() {
            return None;
        }

        let new_dest = Equipments(self[dest].union(grab).cloned().collect());
        if new_dest.is_fried() {
            return None;
        }

        let mut nfloors = self.floors.clone();
        nfloors[src] = new_src;
        nfloors[dest] = new_dest;

        Some(Self {
            floor: dest,
            floors: nfloors,
        })
    }

    fn next_facilities(&self) -> HashSet<Self> {
        let mut out = HashSet::new();

        for direction in [Direction::Up, Direction::Down]
            .into_iter()
            .filter(|&direction| self.floor.r#move(direction).is_some())
        {
            for &eq0 in self.floors[self.floor].iter() {
                for &eq1 in self.floors[self.floor].iter() {
                    let grab = Equipments([eq0, eq1].into_iter().collect());

                    let Some(n) = self.try_traverse(direction, &grab) else {
                        continue;
                    };

                    out.insert(n);
                }
            }
        }

        out
    }

    fn is_done(&self) -> bool {
        if self.floor != Floor::Fourth {
            return false;
        }

        Floor::ALL
            .into_iter()
            .filter(|&floor| floor != Floor::Fourth)
            .all(|floor| self.floors[floor].is_empty())
    }
}

impl<'eq> From<&'eq str> for Facility<'eq> {
    fn from(raw: &'eq str) -> Self {
        Self {
            floor: Floor::default(),
            floors: raw.into(),
        }
    }
}

fn p1(input: &str) -> usize {
    Facility::solve(input.into())
}

fn p2(input: &str) -> usize {
    0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        let input = "
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
"
        .trim();
        assert_eq!(p1(input), 11);
    }
}
