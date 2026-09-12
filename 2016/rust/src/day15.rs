use core::ops::{Deref, DerefMut};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Disk {
    id: usize,
    position: usize,
    positions: usize,
}

impl From<&str> for Disk {
    fn from(value: &str) -> Self {
        let mut it = value.trim().trim_end_matches('.').split_ascii_whitespace();
        let id = it
            .find_map(|s| s.trim_start_matches('#').parse().ok())
            .unwrap();

        let positions = it.find_map(|s| s.parse().ok()).unwrap();

        let position = it.find_map(|s| s.parse().ok()).unwrap();

        Self {
            id,
            position,
            positions,
        }
    }
}

#[derive(Debug)]
struct Disks(Vec<Disk>);

impl Deref for Disks {
    type Target = Vec<Disk>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Disks {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl From<&str> for Disks {
    fn from(value: &str) -> Self {
        Self(value.trim().lines().map(Into::into).collect())
    }
}

impl Disks {
    fn solve(&self) -> usize {
        (usize::MIN..=usize::MAX)
            .find_map(|t| self.find(t))
            .unwrap()
            + 1
    }

    fn find(&self, t0: usize) -> Option<usize> {
        for disk in self.iter() {
            let Disk {
                id,
                position,
                positions,
            } = disk;

            let t = t0 + 1 + id;
            let p = (t + position) % positions;
            if p != 0 {
                return None;
            }
        }

        Some(t0)
    }
}

fn p1(input: &str) -> usize {
    let disks = Disks::from(input);
    disks.solve()
}

fn p2(input: &str) -> usize {
    let mut disks = Disks::from(input);
    let max_id = disks.iter().map(|disk| disk.id).max().unwrap();
    disks.push(Disk {
        id: max_id + 1,
        position: 0,
        positions: 11,
    });
    disks.solve()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert_eq!(
            p1("
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
                "
            .trim()),
            5
        );
    }
}
