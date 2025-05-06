use std::collections::HashMap;

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

fn p1(input: &str) -> u32 {
    FireWall::from(input).send_packet(0).iter().sum()
}

fn p2(input: &str) -> u32 {
    let firewall = FireWall::from(input);
    (1..)
        .find(|&delay| firewall.send_packet(delay).len() == 0)
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
0: 3
1: 2
4: 4
6: 4
";

    #[test]
    fn p1e1() {
        assert_eq!(p1(INPUT), 24);
    }

    #[test]
    fn p2e1() {
        assert_eq!(p2(INPUT), 10);
    }
}
