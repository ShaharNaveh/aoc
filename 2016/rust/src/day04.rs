use std::{cmp::Reverse, collections::HashMap};

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Room<'a> {
    name: &'a str,
    id: usize,
    checksum: &'a str,
}

impl<'a> From<&'a str> for Room<'a> {
    fn from(value: &'a str) -> Self {
        let (name, id_checksum) = value.trim().rsplit_once('-').unwrap();
        let (id, checksum) = id_checksum.trim_end_matches(']').split_once('[').unwrap();

        Self {
            name,
            id: id.parse().unwrap(),
            checksum,
        }
    }
}

impl Room<'_> {
    fn is_real(&self) -> bool {
        let mut counter = HashMap::new();
        let name = self.name.replace('-', "");

        for v in name.chars() {
            *counter.entry(v).or_insert(0) += 1;
        }

        let mut entries = counter.iter().collect::<Vec<_>>();

        entries.sort_unstable_by_key(|entry| (Reverse(entry.1), entry.0));

        let checksum = entries.iter().map(|&(c, _)| c).take(5).collect::<String>();
        checksum == self.checksum
    }

    fn decrypted_name(&self) -> String {
        const BASE: usize = b'a' as usize;

        self.name
            .chars()
            .map(|c| {
                if c == '-' {
                    ' '
                } else {
                    let offset = (c as usize - BASE + self.id) % 26;
                    u8::try_from(BASE + offset).unwrap() as char
                }
            })
            .collect()
    }
}

fn p1(input: &str) -> usize {
    input
        .lines()
        .map(Room::from)
        .filter(|room| room.is_real())
        .map(|room| room.id)
        .sum()
}

fn p2(input: &str) -> usize {
    input
        .lines()
        .map(Room::from)
        .find_map(|room| room.decrypted_name().contains("north").then_some(room.id))
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p1e1() {
        assert!(Room::from("aaaaa-bbb-z-y-x-123[abxyz]").is_real());
    }

    #[test]
    fn p1e2() {
        assert!(Room::from("a-b-c-d-e-f-g-h-987[abcde]").is_real());
    }

    #[test]
    fn p1e3() {
        assert!(Room::from("not-a-real-room-404[oarel]").is_real());
    }

    #[test]
    fn p1e4() {
        assert!(!Room::from("totally-real-room-200[decoy]").is_real());
    }

    #[test]
    fn p2e1() {
        assert_eq!(
            Room::from("qzmt-zixmtkozy-ivhz-343[...]").decrypted_name(),
            "very encrypted name"
        );
    }
}
