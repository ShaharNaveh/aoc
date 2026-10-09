use std::{
    collections::{HashMap, VecDeque, hash_map::Entry},
    ops::{Deref, DerefMut},
};

use crate::utils::IVec2;

pub fn solve(input: &str) {
    println!("{}", p1(&input));
    println!("{}", p2(&input));
}

#[derive(Clone, Copy, Debug)]
struct Node {
    id: IVec2,
    used: usize,
    avail: usize,
}

impl From<&str> for Node {
    fn from(value: &str) -> Self {
        let mut parts = value.trim().split_ascii_whitespace();
        let id = parts
            .next()
            .unwrap()
            .split_once('-')
            .unwrap()
            .1
            .split_once('-')
            .map(|(x, y)| {
                IVec2::new(
                    x.trim_start_matches('x').parse().unwrap(),
                    y.trim_start_matches('y').parse().unwrap(),
                )
            })
            .unwrap();

        let used = parts
            .nth(1)
            .map(|s| s.trim_end_matches('T').parse().unwrap())
            .unwrap();

        let avail = parts
            .next()
            .map(|s| s.trim_end_matches('T').parse().unwrap())
            .unwrap();

        Self { id, used, avail }
    }
}

#[derive(Clone, Debug)]
struct Nodes(Box<[Node]>);

impl From<&str> for Nodes {
    fn from(value: &str) -> Self {
        Self(
            value
                .trim()
                .lines()
                .filter(|l| l.starts_with("/dev/"))
                .map(Into::into)
                .collect(),
        )
    }
}

impl Deref for Nodes {
    type Target = Box<[Node]>;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for Nodes {
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

fn p1(input: &str) -> usize {
    let nodes = Nodes::from(input);

    nodes
        .iter()
        .filter(|node_a| node_a.used > 0)
        .map(|node_a| {
            nodes
                .iter()
                .filter(|node_b| (node_a.id != node_b.id) && node_a.used <= node_b.avail)
                .count()
        })
        .sum()
}

fn p2(input: &str) -> usize {
    let nodes = Nodes::from(input);

    let max_id = nodes.iter().fold(IVec2::ZERO, |acc, node| acc.max(node.id));
    let empty = nodes.iter().find(|node| node.used == 0).unwrap();

    let blocked = {
        let mut map = nodes
            .iter()
            .map(|node| (node.id, node.used > empty.avail))
            .collect::<HashMap<_, _>>();

        map.insert(max_id.with_y(0), true);

        map
    };

    let target = IVec2::new(max_id.x - 1, 0); // top row, left to the data
    let mut dists = HashMap::from([(empty.id, 0)]);

    let mut queue = VecDeque::from([empty.id]);

    while let Some(pos) = queue.pop_front() {
        if pos == target {
            break;
        }

        let nsteps = dists[&pos] + 1;

        for npos in pos.neighbors_4() {
            if blocked.get(&npos).is_none_or(|b| *b) {
                continue;
            };

            let Entry::Vacant(entry) = dists.entry(npos) else {
                continue;
            };

            entry.insert(nsteps);
            queue.push_back(npos);
        }
    }

    let to_front = dists[&target];

    let width = max_id.x + 1;

    // move the empty spot 4 times around the data, then move data one to the left.
    // the `+ 1` is for transferring the data into the empty spot for the first time
    usize::try_from((to_front + 5 * (width - 2)) + 1).unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn p2e1() {
        assert_eq!(
            p2("
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
"),
            7
        );
    }
}
